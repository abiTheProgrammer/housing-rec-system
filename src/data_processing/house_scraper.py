import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pyspark.pandas as ps

class HouseScraper:
    def __init__(self, config_path: str) -> None:
        with open(config_path, 'r') as urls:
            self.__config = json.loads(urls.read())
        self.states = self.scrape_list_of_states()

    def scrape_list_of_states(self) -> list:
        states = []
        r = requests.get(self.__config['base_url'])
        soup = BeautifulSoup(r.content, 'html.parser')
        # with open('data/state_list.html', 'w') as file:
        #     file.write(soup.prettify())
        state_list = soup.find_all("select", "option", class_ = "form-control", id = "searchState")
        states = str(state_list[0]).split("\n")
        for i in range(2, len(states) - 1):
            # index 19 is when state names start
            state = states[i][19: states[i].find("</")]
            states[i - 2] = state.replace(" ", "-")
        # remove last 3 elements (because reusing states list)
        del states[-3:]
        return states
    
    # Return a dataframe from this function with data for state
    def scrape_state(self, state: str) -> pd.DataFrame:
        self.df = pd.DataFrame(columns=self.__config['df_columns'])
        # parse html content of main html page
        state_url = self.__config['base_url'] + self.__config['search_state'].format(state=state)
        r = requests.get(state_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        # pipe the soup_html content into local data file (remove once analysis of html content completed)
        # soup_content = soup.prettify()
        # with open(f"data/mls_listings_{state.lower()}.html", "w") as data_file:
        #     data_file.write(soup_content)
        # <ul class = "sub-section-list"> contains urls of each listings for each area
        rows = soup.find_all("ul", class_ = "sub-section-list")
        for ul_row in rows:
            # handle regular area listings
            if not ul_row.a:
                continue
            elif ul_row.a.get('class') == None:
                areas = ul_row.find_all("a")
                for area in areas:
                    # for each area: parse
                    self.scrape_area(area)
                print('\n', end="")
            else:
                foreclosures = ul_row.find_all("a")
                for fc in foreclosures:
                    # for each fc: parse
                    self.scrape_foreclosure(fc)
                print('\n', end="")
        return self.df
    
    def scrape_area(self, area_tag: str) -> None:
        cities = area_tag.text
        cities_url = area_tag.get('href')
        print("Metro Area: \"" + cities + '\"\n' + "Path: \"" + cities_url + "\"", end='\n\n')
        # parse the url of area to get listings in that area
        r = requests.get(self.__config['base_url'] + cities_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        # pipe the area content into local data file (remove once analysis of html content completed)
        # soup_content = soup.prettify()
        # temp: file name is "montana_c" because only this area is saved to file (remove once content is examined)
        # with open(f"data/mls_listings_montana_c.html", "w") as data_file:
        #     data_file.write(soup_content)
        # parse the content of each area page to get house data for each neighborhood
        rows = soup.find_all("ul", class_ = "sub-section-list")
        for ul_row in rows:
            # handle only listings that do not have the title "Foreclosure"
            if not ul_row.a:
                continue
            if 'Foreclosure' not in ul_row.a.text:
                home_links = ul_row.find_all("a")
                for link in home_links:
                    # for each home_link: parse
                    self.scrape_neighborhood(link)
    
    def scrape_foreclosure(self, foreclosure_tag: str) -> None:
        url = foreclosure_tag.get('href')
        print(url[url.find("ci=") + 3: url.find("&")].replace("+", " ") + " Foreclosures", end='\n\n')
        fc_url = url + self.__config['init_page_count'] + self.__config['init_page_number']
        self.scrape_page(fc_url, 1)

    def scrape_neighborhood(self, neighborhood_tag: str) -> None:
        neighborhood = neighborhood_tag.text
        link = neighborhood_tag.get('href')
        index = link.find("url=")
        # append all search elements to url
        neighborhood_url = link[index + 4:] + self.__config['init_page_count'] + self.__config['init_page_number']
        # change the url if it doesn't follow the pattern
        if (self.__config['base_listing_url'] + "/listing" not in neighborhood_url) \
            or (self.__config['base_listing_url'] + "/listings" in neighborhood_url):
            state = link[-link[::-1].find("-"): -1]
            city = link[-1 - link[::-1][1:].find("/"): -2 - len(state)]
            neighborhood_url = self.__config['base_listing_url'] + self.__config['listing_search_path'] \
                .format(city=city,state=state) + self.__config['init_page_count'] + self.__config['init_page_number']
        print("Neighborhood: \"" + neighborhood + '\"\n' + "Path: \"" + neighborhood_url + "\"")
        # scrape every page
        self.scrape_page(neighborhood_url, 1)

    def scrape_page(self, neighborhood_url: str, page_number: int) -> None:
        r = requests.get(neighborhood_url, headers=self.__config['browser_header'])
        soup = BeautifulSoup(r.content, 'html.parser')
        # If there are 0 listings => stop scraping
        print("Page Number: " + str(page_number))
        if self.scrape_listings(soup) > 0:
            neighborhood_url = neighborhood_url.replace(f"&pg={str(page_number)}", f"&pg={str(page_number + 1)}")
            self.scrape_page(neighborhood_url, page_number + 1)
    
    def scrape_listings(self, listings_data: BeautifulSoup) -> int:
        # rent estimates are stored as "per m" or "/m" Estimated Rental Value (ERV)
        prices = listings_data.find_all("div", class_ = "listingInfo")
        rent_estimates = listings_data.find_all("div", class_ = "rentEstimate")
        adresses = listings_data.find_all("div", class_ = "address")
        beds = listings_data.find_all("div", class_ = "fl bedroomsbox")
        baths = listings_data.find_all("div", class_ = "fl barhroomsbox")
        sq_areas = listings_data.find_all("div", class_ = "fl sizebox d-none d-sm-block")
        home_types = listings_data.find_all("div", class_ = "fl ptypebox")
        print("Number of House Listings in Page: " + str(len(prices)), end='\n\n')
        # retrieve info for each house
        for i in range(len(prices)):
            price = prices[i].strong
            if price:
                price = price.text
            address = adresses[i].a.get('title')
            rent_estimate = rent_estimates[i].text
            # indices repeat because of visible and hidden div elements (x2 to skip)
            bedrooms = beds[i*2].text.strip()
            bathrooms = baths[i*2].text.strip()
            area = sq_areas[i*2].text.strip()
            home_type = home_types[i*2].text.strip()
            if not bedrooms:
                bedrooms = None
            if not bathrooms:
                bathrooms = None
            if not area:
                area = None
            if not home_type:
                home_type = None
            print("Price: " + str(price) + "\nAddress: " + address + "\nRent Estimate: "
                   + str(rent_estimate) + "\nBeds: " + str(bedrooms) + "\nBaths: " + str(bathrooms)
                   + "\nSq Ft: " + str(area) + "\nHome Type: " + str(home_type), end='\n\n')
            house_df = pd.DataFrame(np.array([[price, address, rent_estimate, bedrooms, bathrooms, area, home_type]]),\
                                     columns=self.__config['df_columns'])
            self.df = pd.concat([self.df, house_df], ignore_index=True)
        return len(prices)

# to run the file using "python3 <relative-path-of-file>"
if __name__ == "__main__":
    hs = HouseScraper(config_path='config/config.json')
    scripted_df = None
    # If file already exists, create new version of file by incrementing file_handle (all_states_1.csv, all_states_2.csv)
    for state in hs.states:
        # change this line depending on what states to scrape for
        if state == 'District-of-Columbia' or state == 'Wyoming':
            hs.scrape_state(state)
            # convert pandas -> pandas-on-spark -> spark dataframe
            print(hs.df)
            if scripted_df is None:
                scripted_df = ps.from_pandas(hs.df)
            else:
                scripted_df = ps.concat([scripted_df, ps.from_pandas(hs.df)])
    # coalesce into 1 csv file (change mode based on how data to be stored)
    scripted_df.to_spark().coalesce(1).write.csv(f"data/uncleaned/data_all_states.csv", header=True, mode="overwrite")
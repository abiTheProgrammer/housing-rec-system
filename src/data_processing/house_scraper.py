import requests
import re
from bs4 import BeautifulSoup

class HouseScraper:
    def __init__(self) -> None:
        pass

    def scrape_state(self, state: str):
        # parse html content of main html page
        r = requests.get(f"https://www.mls.com/Search/{state}.mvc")
        soup = BeautifulSoup(r.content, 'html.parser')
        # pipe the soup_html content into local data file (remove once analysis of html content completed)
        soup_content = soup.prettify()
        with open(f"data/mls_listings_{state.lower()}.html", "w") as data_file:
            data_file.write(soup_content)
        # <ul class = "sub-section-list"> contains urls of each listings for each area
        rows = soup.find_all("ul", class_ = "sub-section-list")
        for ul_row in rows:
            # handle regular area listings
            if ul_row.a.get('class') == None:
                areas = ul_row.find_all("a")
                for area in areas:
                    # for each area: parse
                    HouseScraper.scrape_area(self, area)
                    # include break statement to analyze
                    break
                print('\n', end="")
            else:
                # TODO: handle foreclosure listings
                pass
            # include break statement to analyze
            break
    
    def scrape_area(self, area_tag: str):
        cities = area_tag.text
        cities_url = area_tag.get('href')
        print("Metro Area: \"" + cities + '\"\n' + "Path: \"" + cities_url + "\"", end='\n\n')
        # parse the url of area to get listings in that area
        r = requests.get("https://www.mls.com" + cities_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        # pipe the area content into local data file (remove once analysis of html content completed)
        # soup_content = soup.prettify()
        # temp: file name is "bakersfield" because only this area is saved to file (remove once content is examined)
        # with open(f"data/mls_listings_california_bakersfield.html", "w") as data_file:
        #     data_file.write(soup_content)
        # parse the content of each area page to get house data for each neighborhood
        rows = soup.find_all("ul", class_ = "sub-section-list")
        for ul_row in rows:
            # handle only listings that do not have the title "Foreclosure"
            if 'Foreclosure' not in ul_row.a.text:
                home_links = ul_row.find_all("a")
                for link in home_links:
                    # for each home_link: parse
                    HouseScraper.scrape_neighborhood(self, link)
                    # include break statement to analyze
                    # break
            # include break statement to analyze
            # break


    def scrape_neighborhood(self, neighborhood_tag: str):
        neighborhood = neighborhood_tag.text
        link = neighborhood_tag.get('href')
        index = link.find("url=")
        page_count = "&ps=100"
        # append all search elements to url
        neighborhood_url = link[index + 4:] + page_count + "&pg=1"
        # change the url if it doesn't follow the pattern
        if ("https://mls.foreclosure.com/listing" not in neighborhood_url) or ("https://mls.foreclosure.com/listings" in neighborhood_url):
            state = link[-link[::-1].find("-"): -1]
            city = link[-1 - link[::-1][1:].find("/"): -2 - len(state)]
            neighborhood_url = f"https://mls.foreclosure.com/listing/search.html?ci={city}&st={state}&utm_source=internal&utm_medium=link&utm_campaign=MLS_top_links{page_count}&pg=1"
        print("Neighborhood: \"" + neighborhood + '\"\n' + "Path: \"" + neighborhood_url + "\"")
        # scrape every page
        HouseScraper.scrape_page(self, neighborhood_url, 1)

    def scrape_page(self, neighborhood_url: str, page_number: int):
        # set user-agent in heaeder to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
        }
        r = requests.get(neighborhood_url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        # temp: file name is "bakersfield_arvin" because only this area is saved to file (remove once content is examined)
        # with open("data/mls_listings_california_bakersfield_arvin.html", "w") as data_file:
        #     data_file.write(soup.prettify())
        # If there are 0 listings => stop scraping
        print("Page Number: " + str(page_number))
        if HouseScraper.scrape_listings(self, soup) > 0:
            neighborhood_url = neighborhood_url.replace(f"&pg={str(page_number)}", f"&pg={str(page_number + 1)}")
            HouseScraper.scrape_page(self, neighborhood_url, page_number + 1)
    
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
            if price != None:
                price = price.text
            address = adresses[i].a.get('title')
            rent_estimate = rent_estimates[i].text
            bedrooms = beds[i].text.strip()
            bathrooms = baths[i].text.strip()
            area = sq_areas[i].text.strip()
            home_type = home_types[i].text.strip()
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

        return len(prices)

# to run the file using "python3 <relative-path-of-file>"
if __name__ == "__main__":
    h = HouseScraper()
    # TODO: update with a list of states
    h.scrape_state('California')

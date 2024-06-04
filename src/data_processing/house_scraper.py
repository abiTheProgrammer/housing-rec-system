import requests
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
    
    def scrape_area(self, area: str):
        metro_area = area.text
        metro_area_url = area.get('href')
        print("Metro Area: \"" + metro_area + '\"\n' + "Path: \"" + metro_area_url + "\"", end='\n\n')
        # parse the url of area to get listings in that area
        r = requests.get("https://www.mls.com" + metro_area_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        # pipe the area content into local data file (remove once analysis of html content completed)
        soup_content = soup.prettify()
        # temp: file name is "bakersfield" because only this area is saved to file (remove once content is examined)
        with open("data/mls_listings_california_bakersfield.html", "w") as data_file:
            data_file.write(soup_content)
        # TODO: parse the content of each area page to get house data for each neighborhood
        rows = soup.find_all("ul", class_ = "sub-section-list")
        for ul_row in rows:
            # handle only listings that do not have the title "Foreclosure"
            if 'Foreclosure' not in ul_row.a.text:
                home_links = ul_row.find_all("a")
                for link in home_links:
                    # for each home_link: parse
                    neighborhood = link.text
                    neighborhood_link = link.get('href')
                    print("Neighborhood: \"" + neighborhood + '\"\n' + "Path: \"" + neighborhood_link + "\"", end='\n\n')
    

# to run the file using "python3 <relative-path-of-file>"
if __name__ == "__main__":
    h = HouseScraper()
    # TODO: update with a list of states
    h.scrape_state('California')

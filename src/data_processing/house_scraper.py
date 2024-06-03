import requests
from bs4 import BeautifulSoup

class HouseScraper:
    def __init__(self) -> None:
        pass
    def housing_data_from_scrape(self) -> str:
        # parse html content of main html page
        r = requests.get("https://www.mls.com/Search/California.mvc")
        soup = BeautifulSoup(r.content, 'html.parser')
        soup_content = soup.prettify()
        # pipe the soup_html content into local data file (remove once analysis of html content completed)
        with open("data/mls_listings_california.html", "w") as data_file:
            data_file.write(soup_content)
        # <ul class = "sub-section-list"> contains urls of each listings for each area
        rows = soup.find_all("ul", class_ = "sub-section-list")
        for ul_row in rows:
            # handle regular area listings
            if ul_row.a.get('class') == None:
                areas = ul_row.find_all("a")
                for link in areas:
                    metro_area = link.text
                    metro_area_url = link.get('href')
                    print("Metro Area: \"" + metro_area + '\"\n' + "Path: \"" + metro_area_url + "\"")
                    # parse the url of each area to get listings in that area
                    r = requests.get("https://www.mls.com" + metro_area_url)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    soup_content = soup.prettify()
                    # pipe the area content into local data file (remove once analysis of html content completed)
                    # temp: file name is "north-coast" because only last area is saved to file (remove once content is examined)
                    with open("data/mls_listings_california_north_coast.html", "w") as data_file:
                        data_file.write(soup_content)
                    # TODO: parse the content of each area page to get house data for each neighborhood

                print('\n', end="")
            else:
                # TODO: handle foreclosure listings
                pass
        return "house data scraped"

# to run the file using "python3 <relative-path-of-file>"
if __name__ == "__main__":
    h = HouseScraper()
    h.housing_data_from_scrape()

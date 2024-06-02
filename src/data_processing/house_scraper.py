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
        # pipe the soup_html content into local data file
        with open("data/mls_listings_california.html", "w") as html_data_file:
            html_data_file.write(soup_content)
        # <ul class = "sub-section-list"> contains urls of each listing
        rows = soup.find_all("ul", class_ = "sub-section-list")
        for ul_row in rows:
            # handle regular house listings
            if ul_row.a.get('class') == None:
                listings = ul_row.find_all("a")
                for link in listings:
                    print(link.text)
                    print(link.get('href'))
                #     r = requests.get("https://www.mls.com" + link.get('href'))
                #     print(r.content)
                # break
                print('\n', end="")
            else:
                # handle foreclosure listings
                pass
        return "house data scraped"

# to run the file using "python3 <relative-path-of-file>"
if __name__ == "__main__":
    h = HouseScraper()
    h.housing_data_from_scrape()

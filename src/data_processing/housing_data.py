import requests
from bs4 import BeautifulSoup

def housing_data_from_scrape():
    html_text = requests.get("https://www.mls.com/Search/California.mvc").text
    soup = BeautifulSoup(html_text, "lxml").prettify()
    with open("mls_listings_html.txt", "w") as html_data_file:
        html_data_file.write(soup)
    return "house data scraped"

if __name__ == "__main__":
    housing_data_from_scrape()
import requests
from bs4 import BeautifulSoup

def housing_data_from_scrape():
    html_text = requests.get("https://www.mls.com/Search/California.mvc").text
    # soup has type <class 'bs4.BeautifulSoup'>
    soup = BeautifulSoup(html_text, "lxml")
    # soup has type <class 'str'>
    prettified = soup.prettify()
    with open("mls_listings_html.txt", "w") as html_data_file:
        html_data_file.write(prettified)
    listings = soup.find("div", class_ = "col-md-8 col-sm-7 col-xs-12")
    print(listings)
    return "house data scraped"

if __name__ == "__main__":
    housing_data_from_scrape()
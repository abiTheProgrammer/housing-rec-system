import requests
from bs4 import BeautifulSoup

def housing_data_from_scrape():
    r = requests.get("https://www.mls.com/Search/California.mvc")
    soup = BeautifulSoup(r.content, 'html.parser')
    soup_content = soup.prettify()
    # pipe the soup_html content into local data file
    with open("data/mls_listings_html.txt", "w") as html_data_file:
        html_data_file.write(soup_content)
    # TODO: parse the html content

    return "house data scraped"

# to run the file using "python3 housing_data.py"
if __name__ == "__main__":
    housing_data_from_scrape()
import requests
from bs4 import BeautifulSoup

def housing_data_from_scrape():
    r = requests.get("https://www.mls.com/Search/California.mvc")
    print(r.status_code)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    print(soup.prettify())
    # TODO: parse the html content

    return "house data scraped"

# to run the file using "python3 housing_data.py"
if __name__ == "__main__":
    housing_data_from_scrape()
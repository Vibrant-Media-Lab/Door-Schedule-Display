# the webpage I want to open https://vml.pitt.edu/#about

from urllib.request import urlopen
from bs4 import BeautifulSoup
# In order to execute this code you will have to first pip install beautifulsoup4
# then you should be able to run and test this code with the scrapetest.py file that simply calls the function scrape()

def scrape():
    # specify the url
    url = "https://docs.google.com/document/d/e/2PACX-1vQI6sOZt1i9eRKaXa5B3FiLgzjGktt9ymqVpUAswEVlbiNLb4shDFMN82DVsNsDd_6OboApnCzIrwDw/pub"

    # query the website and return the html to the variable ‘page’
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(html, "html.parser")
    text_content = [p.text for p in soup.find_all('p')]
    print(text_content)
    return text_content
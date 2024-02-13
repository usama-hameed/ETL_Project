import requests
from bs4 import BeautifulSoup


def crawl_data(url):
    response = requests.get(url)

    web_page_html = BeautifulSoup(response.text, 'html.parser')
    elements = web_page_html.find_all("div", class_="cell shrink show-for-large")

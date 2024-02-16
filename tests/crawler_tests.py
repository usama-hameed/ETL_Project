import requests
import requests_mock
from src.crawler import crawl_data

def test_url_success():
    with requests_mock.Mocker() as m:
        assert 200 == requests.get('https://www.lucernefestival.ch/en/program/summer-festival-24').status_code


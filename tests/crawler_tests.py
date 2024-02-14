import requests
import requests_mock


def test_url():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='data')
        assert 'data' == requests.get('http://test.com').text
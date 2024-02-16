import requests
import requests_mock
import types
from datetime import date, time
from bs4 import BeautifulSoup
from src.crawler import crawl_data, get_title, get_image, get_datetime_and_location, get_performers_and_songs

html_content = """
<div class="event-content">
    <span class="date-item h4">Tue 13.08.</span>
    <div class="grid-x grid-margin-x">
        <div class="cell shrink show-for-large">
            <a class="event-image-link" href="/en/program/youth-symphony-orchestra-of-ukraine-oksana-lyniv/2024" tabindex="-1">
                <figure>
                    <picture class="clr-sec">
                        <source media="(min-width: 1280px)" srcset="/media/thumbnails/filer_public/7e/8c/7e8cc114-18d2-4b2e-a504-686db42a430b/youth_symphony_orchestra_of_ukraine_lyniv2_c_mutesouvenir_kaibienert.jpg__300x200_q85_crop_subject_location-1470%2C847_subsampling-2_upscale.jpg"/>
                        <source media="(min-width: 1024px)" srcset="/media/thumbnails/filer_public/7e/8c/7e8cc114-18d2-4b2e-a504-686db42a430b/youth_symphony_orchestra_of_ukraine_lyniv2_c_mutesouvenir_kaibienert.jpg__200x133_q85_crop_subject_location-1470%2C847_subsampling-2_upscale.jpg"/>
                        <img alt="Youth Symphony Orchestra of Ukraine | Oksana Lyniv" loading="lazy" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="/>
                    </picture>
                </figure>
            </a>
        </div>
        <div class="event-text cell auto grow">
            <div class="body-small">Youth Symphony Orchestra of Ukraine</div>
            <p class="event-title h3">
                <a href="/en/program/youth-symphony-orchestra-of-ukraine-oksana-lyniv/2024">Youth Symphony Orchestra of Ukraine | Oksana Lyniv</a>
            </p>
            <div class="grid-x grid-margin-x">
                <div class="cell medium-7 xlarge-8">
                    <div class="grid-x grid-margin-x">
                        <div class="cell xlarge-6 body-small">
                            <strong>Date and Venue</strong><br/>
                            Tue 13.08. | 19.30 | KKL Luzern, Concert Hall
                        </div>
                        <div class="cell xlarge-6 body-small">
                            <strong>Program</strong><br/>
                            Debussy | Elgar | Ljatoschynskyj | Respighi
                        </div>
                    </div>
                </div>
                <div class="cell medium-5 xlarge-4 ticket-status">
                    <div class="body-small bold"""


def test_url_success():
    url = 'https://www.lucernefestival.ch/en/program/summer-festival-24'

    with requests_mock.Mocker() as m:
        m.get(url, status_code=200)

        response = requests.get(url)

        assert response.status_code == 200


def test_crawl_data_request_success():
    url = 'https://www.lucernefestival.ch/en/program/summer-festival-24'

    data = crawl_data(url)

    assert type(data) == types.GeneratorType

    for d in data:
        assert 'title' in d
        assert isinstance(d['title'], str)

        assert 'image_link' in d
        assert isinstance(d['image_link'], str)

        assert 'date' in d
        assert isinstance(d['date'], date)

        assert 'time' in d
        assert isinstance(d['time'], time)

        assert 'location' in d
        assert isinstance(d['location'], str)

        assert 'songs' in d
        assert isinstance(d['songs'], list)

        for song in d['songs']:
            assert 'song' in song
            assert 'composer' in song

        assert 'performers' in d
        assert isinstance(d['performers'], list)


def test_wrong_url():
    url = 'https://www.example.com'

    error = crawl_data(url)
    for e in error:
        assert e == 'No Content Found'


def test_title_exist():

    soup = BeautifulSoup(html_content, 'html.parser')

    title = get_title(soup)

    assert title == "Youth Symphony Orchestra of Ukraine"


def test_title_not_exist():
    html_content = """
    <div class="event-content">
        <span class="date-item h4">Tue 13.08.</span>
        <div class="grid-x grid-margin-x">
            <div class="cell shrink show-for-large">
                <a class="event-image-link" href="/en/program/youth-symphony-orchestra-of-ukraine-oksana-lyniv/2024" tabindex="-1">
                    <figure>
                        <picture class="clr-sec">
                            <source media="(min-width: 1280px)" srcset="/media/thumbnails/filer_public/7e/8c/7e8cc114-18d2-4b2e-a504-686db42a430b/youth_symphony_orchestra_of_ukraine_lyniv2_c_mutesouvenir_kaibienert.jpg__300x200_q85_crop_subject_location-1470%2C847_subsampling-2_upscale.jpg"/>
                            <source media="(min-width: 1024px)" srcset="/media/thumbnails/filer_public/7e/8c/7e8cc114-18d2-4b2e-a504-686db42a430b/youth_symphony_orchestra_of_ukraine_lyniv2_c_mutesouvenir_kaibienert.jpg__200x133_q85_crop_subject_location-1470%2C847_subsampling-2_upscale.jpg"/>
                            <img alt="Youth Symphony Orchestra of Ukraine | Oksana Lyniv" loading="lazy" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="/>
                        </picture>
                    </figure>
                </a>
            </div>"""

    soup = BeautifulSoup(html_content, 'html.parser')

    title = get_title(soup)

    assert title == None


def test_image():
    soup = BeautifulSoup(html_content, 'html.parser')

    image = get_image(soup)

    assert image == "/media/thumbnails/filer_public/7e/8c/7e8cc114-18d2-4b2e-a504-686db42a430b/youth_symphony_orchestra_of_ukraine_lyniv2_c_mutesouvenir_kaibienert.jpg__300x200_q85_crop_subject_location-1470%2C847_subsampling-2_upscale.jpg"


def test_no_image():
    html_content = """
    <div class="event-content">
        <span class="date-item h4">Tue 13.08.</span>
        <div class="grid-x grid-margin-x">
            <div class="event-text cell auto grow">
                <div class="body-small">Youth Symphony Orchestra of Ukraine</div>
                <p class="event-title h3">
                    <a href="/en/program/youth-symphony-orchestra-of-ukraine-oksana-lyniv/2024">Youth Symphony Orchestra of Ukraine | Oksana Lyniv</a>
                </p>
                <div class="grid-x grid-margin-x">
                    <div class="cell medium-7 xlarge-8">
                        <div class="grid-x grid-margin-x">
                            <div class="cell xlarge-6 body-small">
                                <strong>Date and Venue</strong><br/>
                                Tue 13.08. | 19.30 | KKL Luzern, Concert Hall
                            </div>
                            <div class="cell xlarge-6 body-small">
                                <strong>Program</strong><br/>
                                Debussy | Elgar | Ljatoschynskyj | Respighi
                            </div>
                        </div>
                    </div>
                    <div class="cell medium-5 xlarge-4 ticket-status">
                        <div class="body-small bold"""

    soup = BeautifulSoup(html_content, 'html.parser')

    image = get_image(soup)

    assert image == None


def test_date():
    soup = BeautifulSoup(html_content, 'html.parser')

    result_data = get_datetime_and_location(soup)[0]

    assert type(result_data) == date


def test_time():
    soup = BeautifulSoup(html_content, 'html.parser')

    result_time = get_datetime_and_location(soup)[1]

    assert type(result_time) == time


def test_location():
    soup = BeautifulSoup(html_content, 'html.parser')

    result_location = get_datetime_and_location(soup)[-1]

    assert result_location == ' KKL Luzern, Concert Hall'

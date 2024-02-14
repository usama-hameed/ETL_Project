import requests
from bs4 import BeautifulSoup


def cleaning_datetime_location(raw_text):
    raw_text = raw_text.replace('Date and Venue', '').split('|')
    datetime = ' '.join(raw_text[0:2]).strip()
    return datetime, raw_text[-1]


def get_title(event):
    title_details = event.find("div", class_="event-text cell auto grow")
    if title_details:
        title = title_details.find("div", class_="body-small").text
        return title
    else:
        return None


def get_image(event):
    image_details = event.find("div", class_='cell shrink show-for-large').find("picture", class_="clr-sec")
    if image_details:
        image_link = image_details.find('source')['srcset']
        return image_link
    return None


def get_datetime_and_location(event):
    outer_tag = event.find("div", class_="event-text cell auto grow")
    inner_tags = outer_tag.find("div", class_="grid-x grid-margin-x").find("div", class_='cell medium-7 xlarge-8')
    get_datetime_and_location_tag = inner_tags.find("div",
                                                    class_="grid-x grid-margin-x").find("div",
                                                                                        "cell xlarge-6 body-small")
    datetime_location_raw = get_datetime_and_location_tag.get_text(strip=True)

    datetime, location = cleaning_datetime_location(datetime_location_raw)

    return datetime, location


def crawl_data(url):
    events_data = {}
    try:
        response = requests.get(url)
    except requests.RequestException as error:
        return "Request Failed, Error:{error}".format(error=error)

    if response.status_code == 200:
        web_page_html = BeautifulSoup(response.text, 'html.parser')
        events_content = web_page_html.find_all("div", class_="event-content")

        for event in events_content:
            events_data['title'] = get_title(event)
            events_data['image_link'] = get_image(event)
            events_data['datetime'], events_data['location'] = get_datetime_and_location(event)

    else:
        return "Request failed, Error:{error}, status:{status}".format(error=response.text, status=response.status_code)

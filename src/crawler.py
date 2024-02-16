import requests
from bs4 import BeautifulSoup
from src.cleaning_text import cleaning_datetime_location


def get_title(event):
    title_details = event.find("div", class_="event-text cell auto grow")
    if title_details:
        title = title_details.find("div", class_="body-small").text
        return title
    return None


def get_image(event):
    image_details = event.find("div", class_='cell shrink show-for-large')
    if image_details:
        picture = image_details.find("picture", class_="clr-sec")
        if picture:
            return picture.find('source').get('srcset', None)
    return None


def get_datetime_and_location(event):
    outer_tag = event.find("div", class_="event-text cell auto grow")
    inner_tags = outer_tag.find("div", class_="grid-x grid-margin-x").find("div", class_='cell medium-7 xlarge-8')
    datetime_and_location_tag = inner_tags.find("div",
                                                class_="grid-x grid-margin-x").find("div",
                                                                                    "cell xlarge-6 body-small")

    if datetime_and_location_tag:
        raw_text = datetime_and_location_tag.get_text(strip=True)
        if raw_text:
            date, time, location = cleaning_datetime_location(raw_text)
            return date, time, location
    return None, None, None


def get_songs(all_content):
    songs_data = {'song': None, 'composer': None}
    all_songs_data = []
    program_section = all_content.find("section", class_="grid-container program-description").find("div",
                                                                                                    class_="grid-x grid-margin-x align-center")
    inner_tag = program_section.find("div", class_="cell medium-10 large-8").find("div",
                                                                                  class_="grid-x grid-margin-x align-right")
    songs_tag = inner_tag.find("div", class_="cell medium-9")
    if songs_tag:
        all_songs = songs_tag.find_all("div", class_="program-item p")
        for songs in all_songs:
            if songs.find('strong') is not None:
                songs_data['composer'] = songs.find('strong').text
            if songs.find('em') is None:
                div_text = songs.text.strip()
                desired_text = div_text.split('\n')[-1].strip()
                if 'composer' in songs_data:
                    songs_data['song'] = desired_text
            else:
                songs_data['song'] = songs.find('em').text
            # songs_data['composer'], songs_data['song'] = cleaning_songs(songs.get_text(strip=True))
            all_songs_data.append(songs_data)
            songs_data = {'song': None, 'composer': None}
        return all_songs_data
    else:
        return None


def get_performers_and_songs(event):
    title_details = event.find("div", class_="event-text cell auto grow")
    url = title_details.find("p", class_="event-title h3").find('a').get('href')
    performers = title_details.find("p", class_="event-title h3").find('a').text.split('|')

    url = 'https://www.lucernefestival.ch' + url
    try:
        response = requests.get(url)
    except requests.RequestException as error:

        raise Exception("Request Failed, Error:{error}".format(error=error))

    next_web_page = BeautifulSoup(response.text, 'html.parser')
    all_content = next_web_page.find("div", class_="page-container event-detail-pages event-detail-page")

    songs = get_songs(all_content)
    return songs, performers


def crawl_data(url):
    events_data = {}

    try:
        response = requests.get(url)
    except requests.RequestException as error:
        yield "Request Failed, Error:{error}".format(error=error)
        return

    if response.status_code == 200:
        web_page_html = BeautifulSoup(response.text, 'html.parser')
        events_content = web_page_html.find_all("div", class_="event-content")
        if events_content:
            for event in events_content:
                events_data['title'] = get_title(event)
                events_data['image_link'] = get_image(event)
                events_data['date'], events_data['time'], events_data['location'] = get_datetime_and_location(event)
                events_data['songs'], events_data['performers'] = get_performers_and_songs(event)
                yield events_data
        else:
            yield "No Content Found"

    else:
        yield "Request failed, status:{status}".format(status=response.status_code)

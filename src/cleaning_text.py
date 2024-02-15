import re
import html
from datetime import datetime


def cleaning_datetime_location(raw_text):

    raw_text = raw_text.replace('Date and Venue', '').split('|')
    date_and_time = ' '.join(raw_text[0:2]).strip()
    parts = date_and_time.split()
    date_part = parts[1].replace('.', '-')+'2024'
    time_part = parts[2].replace('.', ':')+':00'

    date_object = datetime.strptime(date_part, "%d-%m-%Y").date()
    time_obj = datetime.strptime(time_part, "%H:%M:%S").time()

    return date_object, time_obj, raw_text[-1]


def cleaning_songs(raw_text):

    pattern = r'\s*\([^)]*\)'

    cleaned_text = re.sub(pattern, '@', raw_text).split('@')
    cleaned_text = html.unescape(cleaned_text)
    if cleaned_text[-1] == 'Sergei Rachmaninoff':
        print(raw_text)
    if len(cleaned_text) > 1:
        return cleaned_text[0], cleaned_text[-1]
    return None, None

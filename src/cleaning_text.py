import re


def cleaning_datetime_location(raw_text):
    raw_text = raw_text.replace('Date and Venue', '').split('|')
    datetime = ' '.join(raw_text[0:2]).strip()
    return datetime, raw_text[-1]


def cleaning_songs(raw_text):
    pattern = r'\s*\([^)]*\)'

    cleaned_text = re.sub(pattern, '@', raw_text).split('@')

    return cleaned_text[0], cleaned_text[-1]

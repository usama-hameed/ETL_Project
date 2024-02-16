from src.crawler import crawl_data
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from db.models import Event, Song, Performers
from db.connection import engine


Session = sessionmaker(bind=engine)
session = Session()

URL = 'https://www.lucernefestival.ch/en/program/summer-festival-24'


def save_data(data):
    song_obj_list = []
    try:
        event = Event(title=data.get('title', None), date=data.get('date', None), time=data.get('time', None),
                      location=data.get('location', None), image_url=data.get('image_link', None))
        session.add(event)

        for song_info in data['songs']:
            song_obj = Song(name=song_info.get('song', None), composer=song_info.get('composer', None), event=event)
            session.add(song_obj)
            song_obj_list.append(song_obj)

        for performer, song_obj in zip(data['performers'], song_obj_list):
            performers = Performers(name=performer, event=event, song=song_obj)
            session.add(performers)

        session.commit()

    except IntegrityError as e:
        session.rollback()
        print("Error:", e, "Title:", data['title'])
    finally:
        session.close()


print("Scraping Started")
events_data = crawl_data(url=URL)
print("Scraping Done")

if type(events_data) == str:
    print(events_data)
    exit()

print("Saving Data in Database")
for data in events_data:
    if isinstance(data, dict):
        save_data(data)

print("Data Saved in Database")

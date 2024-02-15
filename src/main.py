from crawler import crawl_data
from sqlalchemy.orm import sessionmaker
from db.models import Event, Song
from db.connection import engine


Session = sessionmaker(bind=engine)
session = Session()

URL = 'https://www.lucernefestival.ch/en/program/summer-festival-24'


def save_data(data):
    event = Event(title=data.get('title', None), date=data.get('date', None), time=data.get('time', None),
                  location=data.get('location', None), image_url=data.get('image_link', None))
    session.add(event)

    if 'songs' in data:
        for song_info in data['songs']:
            song = Song(name=song_info.get('song', None), composer=song_info.get('composer', None), event=event)
            session.add(song)

    session.commit()
    session.close()


events_data = crawl_data(url=URL)

for data in events_data:
    save_data(data)

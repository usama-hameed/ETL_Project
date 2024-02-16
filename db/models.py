from sqlalchemy import Column, Integer, String, DATE, Time, ForeignKey
from sqlalchemy.orm import relationship
from .connection import Base, engine


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    date = Column(DATE)
    time = Column(Time)
    location = Column(String)
    image_url = Column(String)
    songs = relationship('Song',  back_populates='event', cascade='all, delete-orphan')
    performers = relationship('Performers',  back_populates='event', cascade='all, delete-orphan')


class Song(Base):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    composer = Column(String)
    event_id = Column(Integer, ForeignKey('event.id'))
    event = relationship('Event', back_populates='songs')
    performers = relationship('Performers', back_populates='song', cascade='all, delete-orphan')


class Performers(Base):
    __tablename__ = 'performers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    event_id = Column(Integer, ForeignKey('event.id'))
    song_id = Column(Integer, ForeignKey('song.id'))
    event = relationship('Event', back_populates='performers')
    song = relationship('Song', back_populates='performers')


Base.metadata.create_all(engine)

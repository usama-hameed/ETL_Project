import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.connection import Base, engine, SessionLocal
from src.main import save_data, Session
from db.models import Event, Song, Performers
from sqlalchemy.exc import IntegrityError


@pytest.fixture(scope="module")
def test_db():
    test_engine = create_engine('postgresql://postgres:admin123@localhost:5432/Events2024')
    Base.metadata.create_all(bind=test_engine)
    test_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    yield test_SessionLocal
    Base.metadata.drop_all(bind=test_engine)


def test_session(test_db):
    session = test_db()
    assert session is not None


class TestEvents:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        self.valid_event = Event(
            title="sample title",
            date="2024-03-12",
            time="12:45:00",
            location="cottbus",
            image_url="/media/image.jpg"
        )
        self.valid_song = Song(
            name='aadat',
            composer='Gohar',
            event=self.valid_event

        )
        self.valid_performer = Performers(
            name='sam',
            song=self.valid_song,
            event=self.valid_event
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_event_insertion(self):
        self.session.add(self.valid_event)
        self.session.commit()
        event = self.session.query(Event).filter_by(title="sample title").first()
        assert event.location == "cottbus"
        assert event.image_url == "/media/image.jpg"
        assert event.title == "sample title"

    def test_evet_insertion_faliure(self):
        self.session.add(self.valid_event)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def test_song_insertion(self):
        self.session.add(self.valid_song)
        self.session.commit()
        song = self.session.query(Song).filter_by(name="aadat").first()
        assert song.name == "aadat"
        assert song.composer == "Gohar"
        assert song.event == self.valid_event

    def test_performer_insertion(self):
        self.session.add(self.valid_performer)
        self.session.commit()
        performer = self.session.query(Performers).filter_by(name="sam").first()
        assert performer.name == "sam"
        assert performer.event == self.valid_event
        assert performer.song == self.valid_song

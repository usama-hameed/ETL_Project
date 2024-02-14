from crawler import crawl_data
# from sqlalchemy.orm import sessionmaker
# from db.models import Event
# from db.connection import engine
#
# Session = sessionmaker(bind=engine)
# session = Session()

URL = 'https://www.lucernefestival.ch/en/program/summer-festival-24'


# def save_data(data):
#     event = Event(title=data['title'], date=data['date'], time=data['time'],
#                   location=data['time'], image_url=data['image_url'])
#     session.add(event)
#     session.commit()
#     session.close()


events_data = crawl_data(url=URL)

# for data in events_data:
#     print("------------------------------------------------------------")
#     print(data)
#     print("------------------------------------------------------------")

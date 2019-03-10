import sqlalchemy
from sqlalchemy.orm import sessionmaker


def start_session():
    engine = sqlalchemy.create_engine('mysql+pymysql://hound-user:Hound-password9@localhost:3306/HOUNDSPLOIT')
    Session = sessionmaker(bind=engine)
    return Session()

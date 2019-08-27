import sqlalchemy
from sqlalchemy.orm import sessionmaker


def start_session():
    """
    Start a new database session.
    :return: a new database session.
    """
    # engine = sqlalchemy.create_engine('mysql+pymysql://hound-user:Hound-password9@localhost:3306/HOUNDSPLOIT')
    engine = sqlalchemy.create_engine('sqlite:///hound_db.sqlite3')
    Session = sessionmaker(bind=engine)
    return Session()

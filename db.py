from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine('sqlite:///db.sqlite3', echo=True)
Base = declarative_base()


class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True)
    autor = Column(String)
    name = Column(String)
    len = Column(String)

    def __str__(self):
        return self.name


Base.metadata.create_all(engine)

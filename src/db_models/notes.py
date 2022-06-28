import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from dateutil.tz import gettz

Base = declarative_base()


class Notes(Base):
    __tablename__ = "notes"
    notes_id = Column(Integer, primary_key=True)
    details = Column(String, nullable=False)
    note_type = Column(String, nullable=False)
    created_time = Column(DateTime, default=datetime.datetime.now(tz=gettz('Asia/Kolkata')))
    modified_time = Column(DateTime, default=datetime.datetime.now(tz=gettz('Asia/Kolkata')))
    
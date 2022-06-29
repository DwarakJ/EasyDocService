import os
import logging

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.db_models.notes import Notes, Base
from sqlalchemy.sql.expression import update
import json



log = logging.getLogger(__name__)


curr_dir = os.getcwd()

with open(os.path.join(curr_dir,"config.json")) as f:
    config_data = json.load(f)


def engine(url):
    return create_engine(url, echo=True)


def session(cfg):
    """
        Return sqlalchemy session to database using QueuePool.
    """
    return Session(bind=engine(cfg), expire_on_commit=False)


@contextmanager
def terminating_sn(sn_or_cfg):
    """ A contextlib which closes session and db connections after use. """
    sn = session(sn_or_cfg)
    try:
        yield sn
    finally:
        sn.close()
        sn.bind.dispose()


def db_exists(url):
    """ Given a session to a db, return True if db is already created. """
    if(os.path.exists(url)):
        return True
    return False


def create_db(url):
    """
    @return True if DB was created successfully, False if DB exists,
            raises exception for other errors
    """
    if db_exists(url):
        return False

    # This should create DB and tables
    with terminating_sn(url) as sn:
        Base.metadata.create_all(bind=sn.bind)
    log.info('Provisioned db:%s', url)
    return True


def drop_db():
    db_url = os.path.join(curr_dir, config_data["DB_NAME"])

    if not db_exists(db_url):
        print(db_url)
        return False

    os.remove(db_url)
    return True

def insert_notes(url, data):
    
    notes_data = []
    for d in data:
        notes_data.append(Notes(name = d.name, details = d.note, note_type = d.note_type, created_time = d.created_time, modified_time = d.modified_time))
    
    with terminating_sn(url) as sn:
        sn.add_all(notes_data)
        sn.commit()
        
def query_notes(url):

    result = None

    with terminating_sn(url) as sn:
        result = sn.query(Notes).all()
    
    return result

    
def query_notes_with_filter(url, note_id):

    result = None

    with terminating_sn(url) as sn:
        result = sn.query(Notes).filter(Notes.notes_id == note_id)
    
    return result



def update_note(url, note_id, data):
    note = query_notes_with_filter(url, note_id)
    
    if note:
        note.update({'note_type': data.note_type, 'name': data.name, 'details': data.note, 'modified_time': data.modified_time})
        note.session.commit()
        return True
    else:
        return False
    

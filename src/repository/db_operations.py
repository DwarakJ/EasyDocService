import os
import logging

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.db_models.notes import Notes, Base


log = logging.getLogger(__name__)


SQLITE_URL = 'sqlite:///foo.db'


def engine(url, serialize=False):
    # if serialize:
    #     return create_engine(url, isolation_level="SERIALIZABLE",
    #                          client_encoding='utf8', echo=True)
    # else:
    #     return create_engine(url, client_encoding='utf8', echo=True)
    
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


def drop_db(url):
    if not db_exists(url):
        return False

    os.remove(url)
    return True

def insert_notes(url, data):
    
    n = Notes(details = data.note, note_type = data.note_type, created_time = data.created_time, modified_time = data.modified_time)
    
    with terminating_sn(url) as sn:
        sn.add(n)
        sn.commit()
        
def query_notes(url):

    result = None

    with terminating_sn(url) as sn:
        result = sn.query(Notes).all()
    
    return result

    
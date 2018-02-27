import pytest

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.model import Base

@pytest.fixture(scope='module')
def engine():

    path = Path('test_loader.db').resolve()
    engine = create_engine(f'sqlite:///{path}')

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)    

    return engine

@pytest.fixture(scope='function')
def session(engine):

    connection = engine.connect()
    transaction = connection.begin()
    SessionMaker = sessionmaker(bind=connection)

    session = SessionMaker()

    yield session

    session.close()
    transaction.rollback()
    connection.close()    


def test_ray_date_loader_0(session):

    assert True

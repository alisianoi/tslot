import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.model import Base

@pytest.fixture(scope='module')
def engine(tmpdir_factory):

    path = tmpdir_factory.mktemp(
        'db', numbered=True
    ).join('__file__' + '.db')

    print(f'Will create database at {path}')

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

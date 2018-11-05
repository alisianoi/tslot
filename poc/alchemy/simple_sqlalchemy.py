#!/usr/bin/env python

from pathlib import Path

from sqlalchemy import Column, ForeignKey
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.types import Integer, String

Base = declarative_base()


class Tim(Base):

    __tablename__ = 'tims'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f'Tim({self.id}, {self.name})'

if __name__ == '__main__':

    engine = create_engine(
        f'sqlite:///{Path(Path.cwd(), Path("simple_sqlalchemy.db"))}'
        , echo=True, echo_pool=True
    )

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    SessionMaker = sessionmaker(bind=engine)

    session = SessionMaker()

    tim = Tim()
    tim.name = "Brady"

    session.add(tim)
    session.commit()
    session.close()

    session = SessionMaker()

    tom = Tim()
    tom.id = 1
    tom.name = "Doctor Brady Haran"

    session.query(Tim).filter(Tim.id == tom.id).update({'name': tom.name})
    session.commit()

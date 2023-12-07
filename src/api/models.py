from enum import Enum

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# SQLAlchemy ORM
Base = declarative_base()
engine = create_engine(
    "sqlite:///C:\\Users\\guilh\\pet_monitor_server\\database\\petmonitor.db",
    echo=True,
)


class EventType(Enum):
    START = 0
    END = 1


class Pet(Base):
    __tablename__ = "pet"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    image = Column(String(50), nullable=True)

    def __repr__(self):
        return "<Pet(name='%s', age='%s', weight='%s', image='%s')>" % (
            self.name,
            self.age,
            self.weight,
            self.image,
        )

    def __str__(self):
        return "<Pet(name='%s', age='%s', weight='%s', image='%s')>" % (
            self.name,
            self.age,
            self.weight,
            self.image,
        )


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pet.id"), nullable=True)
    type = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    timestamp = Column(Integer, nullable=False)
    image = Column(String(50), nullable=False, index=True)

    def __repr__(self):
        return "<Event(pet_id='%s', type='%s', timestamp='%s')>" % (
            self.pet_id,
            self.type,
            self.timestamp,
        )

    def __str__(self):
        return "<Event(pet_id='%s', type='%s', timestamp='%s')>" % (
            self.pet_id,
            self.type,
            self.timestamp,
        )


Base.metadata.create_all(engine)


def populate_pets():
    Session = sessionmaker(bind=engine)
    session = Session()

    if session.query(Pet).count() > 0:
        return

    session.add(Pet(name="Batima", age=1, weight=1.3, image="batima.jpg"))
    session.add(Pet(name="Botinha", age=2, weight=1.0, image="botinha.jpg"))
    session.add(Pet(name="Linco", age=3, weight=1.2, image="linco.jpg"))
    session.add(Pet(name="Nico", age=5, weight=1.8, image="nico.jpg"))
    session.add(Pet(name="Peto", age=5, weight=2.3, image="peto.jpg"))

    session.commit()
    session.close()

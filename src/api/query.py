from typing import List

from .models import Pet, Event, engine
from typing import List
from .models import Pet, Event, engine, populate_pets
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

populate_pets()


def create_pet(name: str, age: int, weight: float, image: str) -> int:
    pet = Pet(name=str(name), age=str(age), weight=float(weight), image=str(image))
    session.add(pet)
    session.commit()
    return pet.id


def get_pet(pet_id: int) -> Pet:
    pet = session.query(Pet).filter_by(id=pet_id).first()
    p = pet.__dict__
    del p["_sa_instance_state"]
    return p


def get_pets() -> List[Pet]:
    pets = session.query(Pet).all()
    response = []
    for pet in pets:
        p = pet.__dict__
        del p["_sa_instance_state"]
        response.append(p)
    # return as a list of dictionaries
    return response


def update_pet(pet_id: int, name: str, age: int, weight: float, image: str) -> None:
    pet = get_pet(pet_id)
    pet.name = name
    pet.age = age
    pet.weight = weight
    pet.image = image
    session.commit()


def delete_pet(pet_id: int) -> None:
    pet = get_pet(pet_id)
    session.delete(pet)


def create_event(event_type: int, weight: float, timestamp: int, image: str) -> int:
    event = Event(
        type=int(event_type),
        weight=float(weight),
        timestamp=int(timestamp),
        image=str(image),
    )
    session.add(event)
    session.commit()
    return event.id


def get_event(event_id: int) -> Event:
    event = session.query(Event).filter_by(id=event_id).first()
    if event is None:
        print(event_id)
    e = event.__dict__
    del e["_sa_instance_state"]
    return e


def get_event_by_image(image: str) -> Event:
    event = session.query(Event).filter_by(image=image).first()
    return event


def get_events(pet: int) -> List[Event]:
    events = session.query(Event).filter_by(pet_id=pet).all()
    response = []
    for event in events:
        e = event.__dict__
        del e["_sa_instance_state"]
        response.append(e)
    # return as a list of dictionaries
    return response


def update_event(image: str, pet_id: int) -> None:
    event = get_event_by_image(image)
    event.pet_id = pet_id
    session.commit()


def get_latest_pet_data():
    # query all pets and the latest event for each pet
    # return as a list of dictionaries
    pets = session.query(Pet).all()
    response = []
    for pet in pets:
        p = pet.__dict__
        del p["_sa_instance_state"]
        p["latest_event"] = get_latest_event(p["id"])
        response.append(p)
    return response


def get_latest_event(pet_id: int) -> Event:
    # query all events for a pet and return the latest event
    events = session.query(Event).filter_by(pet_id=pet_id).all()
    latest_event = None
    for event in events:
        e = event.__dict__
        del e["_sa_instance_state"]
        if latest_event is None:
            latest_event = e
        elif e["timestamp"] > latest_event["timestamp"]:
            latest_event = e
    return latest_event

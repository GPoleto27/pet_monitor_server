from enum import Enum

import graphene
import uuid


class EventType(Enum):
    STARTED_EATING = 0
    STOPPED_EATING = 1


class Pet(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    image = graphene.String()
    target_weight = graphene.Float()
    current_weight = graphene.Float()
    last_feeding = graphene.DateTime()
    last_feeding_amount = graphene.Float()


pet_schema = graphene.Schema(query=Pet)


class Event(graphene.ObjectType):
    id = graphene.String()
    type = graphene.Enum.from_enum(EventType)
    timestamp = graphene.DateTime()
    weight = graphene.Float()
    pet = graphene.Field(Pet)


event_schema = graphene.Schema(query=Event)

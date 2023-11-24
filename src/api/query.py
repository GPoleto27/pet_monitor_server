from graphene import ObjectType


class Query(ObjectType):
    def resolve_get_pet(root, info, id):
        return list(filter(lambda pet: pet.id == id, pets)[0])

    def resolve_get_pets(root, info):
        return pets

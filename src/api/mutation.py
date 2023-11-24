import graphene
from type import Pet
from query import Query


class CreatePet(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        image = graphene.String(required=False)
        target_weight = graphene.Float(required=True)
        current_weight = graphene.Float(required=True)
        last_feeding = graphene.DateTime(required=False)
        last_feeding_amount = graphene.Float(required=False)

    pet = graphene.Field(lambda: Pet)

    def mutate(
        self,
        info,
        id,
        name,
        image,
        target_weight,
        current_weight,
        last_feeding,
        last_feeding_amount,
    ):
        pet = Pet(
            id=id,
            name=name,
            image=image,
            target_weight=target_weight,
            current_weight=current_weight,
            last_feeding=last_feeding,
            last_feeding_amount=last_feeding_amount,
        )
        # Here you would normally save the pet to your database
        return CreatePet(pet=pet)


class Mutations(graphene.ObjectType):
    create_pet = CreatePet.Field()


pet_schema = graphene.Schema(query=Pet, mutation=Mutations)

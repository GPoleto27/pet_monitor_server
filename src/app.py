from graphql_server.flask import GraphQLView

from api import app, db
from api.type import event_schema, pet_schema


app.add_url_rule(
    "/graphql/events",
    view_func=GraphQLView.as_view("events", schema=event_schema, graphiql=True),
)
app.add_url_rule(
    "/graphql/pets",
    view_func=GraphQLView.as_view("pets", schema=pet_schema, graphiql=True),
)


def main():
    print("Creating database...")
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    main()

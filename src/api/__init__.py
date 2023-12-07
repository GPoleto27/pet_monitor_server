from os.path import join as path_join

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename

from .models import engine
from .query import (
    create_pet,
    get_pet,
    get_pets,
    update_pet,
    delete_pet,
    create_event,
    get_event,
    get_events,
    update_event,
    get_latest_pet_data,
)
from .model_run import add_to_inference_queue, run_inference


UPLOAD_FOLDER = "C:\\Users\\guilh\\pet_monitor_server\\images"
ALLOWED_EXTENSIONS = {"png"}

app = Flask(__name__)
CORS(app)

# Create a session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

import requests

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/image", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # get file name in a variable
        filename = request.args.get("filename")
        # receive a jpeg image
        image = request.data
        # save the image
        filename = secure_filename(filename)
        with open(path_join(app.config["UPLOAD_FOLDER"], filename), "wb") as f:
            f.write(image)
        # run inference
        pet_id, pet_name = run_inference(
            path_join(app.config["UPLOAD_FOLDER"], filename)
        )

        update_event(filename, pet_id)

        # send the prediction to the frontend
        return str(pet_name), 200
    return "OK", 200


# params: prediction
@app.route("/prediction", methods=["GET"])
def prediction():
    prediction = request.args.get("prediction")
    return prediction, 200


@app.route("/pet", methods=["GET", "POST"])
def pet():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        weight = request.form["weight"]
        image = request.form["image"]
        pet_id = create_pet(name, age, weight, image)
        return str(pet_id), 201
    else:
        pet_id = request.args.get("id")
        if pet_id:
            pet = get_pet(pet_id)
            return pet
        else:
            pets = get_latest_pet_data()
            return pets


@app.route("/pet/<pet_id>", methods=["DELETE"])
def pet_id(pet_id):
    delete_pet(pet_id)
    return "Pet deleted successfully"


@app.route("/event", methods=["GET", "POST"])
def event():
    if request.method == "POST":
        event_type = request.form["type"]
        weight = request.form["weight"]
        timestamp = request.form["timestamp"]
        image = request.form["image"]
        event_id = create_event(event_type, weight, timestamp, image)
        return str(event_id), 201
    else:
        pet_id = request.args.get("pet_id")
        if pet_id:
            events = get_events(pet_id)
            return events, 200
        else:
            event_id = request.args.get("id")
            if event_id:
                event = get_event(event_id)
                return event, 200
            else:
                events = get_events()
                return events, 200
        return "WTF", 400


@app.route("/event/<event_id>", methods=["PUT"])
def event_id(event_id):
    pet_id = request.form["pet_id"]
    event_type = request.form["type"]
    weight = request.form["weight"]
    timestamp = request.form["timestamp"]
    event_id = create_event(pet_id, event_type, weight, timestamp)
    return "Event updated successfully"


@app.route("/")
def hello():
    return "Pet Monitor Server is running!"

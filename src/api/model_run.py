from multiprocessing import Queue
import tensorflow as tf
import numpy as np
from time import time

from .query import get_event_by_image, update_event, get_pet

image_queue = Queue()

model = tf.keras.models.load_model("C:\\Users\\guilh\\pet_monitor_server\\model.h5")


def run_inference(image: str) -> tuple:
    image_queue.put(image)
    # Load the image
    img = tf.keras.preprocessing.image.load_img(image, target_size=(40, 30))
    # Convert the image to a numpy array
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    # Expand the dimensions of the image
    img_array = tf.expand_dims(img_array, 0)

    # Run the inference
    predictions = model.predict(img_array)
    prediction = np.argmax(predictions[0])

    pet_id = int(prediction + 1)

    pet = get_pet(pet_id)

    return pet_id, pet.get("name", f"Unknown: {pet_id}")


def inference_worker():
    time_since_last_inference = time()
    while True:
        images = []
        while not image_queue.empty():
            images.append(image_queue.get())
        if len(images) > 9 or (
            time() - time_since_last_inference > 1 and len(images) > 0
        ):
            time_since_last_inference = time()
            pet_id, _ = run_inference(images)

            for image in images:
                update_event(image, pet_id)


def add_to_inference_queue(image: str):
    image_queue.put(image)

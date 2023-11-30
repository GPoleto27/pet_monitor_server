from multiprocessing import Queue
import tensorflow as tf
import numpy as np
from time import time

from .query import get_event_by_image

image_queue = Queue()

model = tf.keras.models.load_model("/models/model.h5")


def run_inference(image: str) -> int:
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

    return prediction + 1  # database is 1-indexed while model is 0-indexed


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
            predictions = run_inference(images)

            for i, image in enumerate(images):
                filename = "/" + image.split("/")[-1]
                event = get_event_by_image(filename)
                event.pet = predictions[i]
                event.save()


def add_to_inference_queue(image: str):
    image_queue.put(image)

from multiprocessing import Process, Queue

from api.model_run import inference_worker


def main():
    # inference_worker_process = Process(target=inference_worker)
    # inference_worker_process.start()

    # start flask app
    from api import app

    app.run(host="0.0.0.0", port=5000, debug=True)
    # inference_worker_process.join()


if __name__ == "__main__":
    main()

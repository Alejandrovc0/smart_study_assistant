from multiprocessing import Process
from flask_cors import CORS
from flask import Flask, send_from_directory
from dotenv import load_dotenv
from backend.server import backend_app

load_dotenv()
CORS(backend_app)

frontend_app = Flask(__name__, static_folder="frontend")


@frontend_app.route("/")
def index():
    return send_from_directory("frontend", "index.html")


@frontend_app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory("frontend", path)


@frontend_app.route("/outputs/<path:path>")
def serve_outputs(path):
    return send_from_directory("outputs", path)


def run_frontend():
    try:
        frontend_app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        print(f"Error running frontend server: {e}")


def run_backend():
    try:
        backend_app.run(host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"Error running backend server: {e}")


if __name__ == "__main__":
    try:
        # Start the backend server
        backend_process = Process(target=run_backend)
        backend_process.start()

        # Start the frontend server
        frontend_process = Process(target=run_frontend)
        frontend_process.start()

        # Join the processes so that the main process waits for them to complete
        backend_process.join()
        frontend_process.join()
    except Exception as e:
        print(f"Error starting servers: {e}")

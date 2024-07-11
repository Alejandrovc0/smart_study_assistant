from flask import Flask, jsonify, request
from backend.langgraph_agent import MainAgent

backend_app = Flask(__name__)


@backend_app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "Running"}), 200


@backend_app.route("/smart_study_assistant", methods=["POST"])
def generate_newspaper():
    data = request.json
    main_agent = MainAgent()
    study_assistant = main_agent.run(data["topic"])
    return jsonify({"path": study_assistant}), 200

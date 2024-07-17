from flask import Flask, jsonify, request
from backend.langgraph_agent import MainAgent
from backend.agents.website_agent import WebsiteAgent
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

backend_app = Flask(__name__)

outputs_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(outputs_dir, exist_ok=True)


@backend_app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "Running"}), 200


@backend_app.route("/smart_study_assistant", methods=["POST"])
def run_agents():
    data = request.json

    if "topic" not in data:
        return jsonify({"error": "Missing 'topic' in request"}), 400

    main_agent = MainAgent()
    try:
        study_plan = main_agent.run([data["topic"]])
        return jsonify({"path": study_plan}), 200

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

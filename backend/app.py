from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from typing import Any

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

def load_data() -> list[dict[str, Any]]:
    """Load user data from a JSON file."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        app.logger.error(f"Error loading data: {e}")
        return []

def save_data(data: list[dict[str, Any]]) -> None:
    """Save user data to a JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception as e:
        app.logger.error(f"Error saving data: {e}")

@app.route("/api/users", methods=["GET"])
def get_users():
    """Get all users."""
    users = load_data()
    return jsonify(users)

@app.route("/api/users", methods=["POST"])
def add_user():
    """Add a new user."""
    try:
        data = request.get_json()
        if not data or "name" not in data:
            return jsonify({"error": "Missing user name"}), 400
        users = load_data()
        new_id = max((user['id'] for user in users), default=0) + 1
        new_user = {"id": new_id, "name": data["name"]}
        users.append(new_user)
        save_data(users)
        return jsonify(new_user), 201
    except Exception as e:
        return jsonify({"error": "Failed to add user", "details": str(e)}), 500

# Add PUT and DELETE as needed for full CRUD...

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["todo_database"]

todos = db["todos"]


@app.route("/")
def home():
    return "Flask Backend is running!"


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():

    data = request.get_json()

    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({
            "success": False,
            "message": "itemName and itemDescription are required"
        }), 400

    todo = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    result = todos.insert_one(todo)

    return jsonify({
        "success": True,
        "message": "To-do item saved successfully",
        "id": str(result.inserted_id)
    }), 201


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
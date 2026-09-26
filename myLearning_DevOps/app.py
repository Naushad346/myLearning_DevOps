import json
import os
from pathlib import Path
from urllib.parse import quote_plus, unquote_plus, urlsplit, urlunsplit

from flask import Flask, flash, redirect, render_template, request, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "items.json"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "development-only-secret")XPPP[[[[[[-]]]]]]


def get_collection():
    """Return the configured MongoDB Atlas collection."""
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        raise RuntimeError("MONGODB_URI is not configured.")

    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    parsed_uri = urlsplit(mongodb_uri)
    if username is None and password is None:
        username = parsed_uri.username
        password = parsed_uri.password
        if username is not None and password is not None:
            username = unquote_plus(username)
            password = unquote_plus(password)

    if username is not None and password is not None:
        if not parsed_uri.hostname:
            raise RuntimeError("MONGODB_URI must include a MongoDB host.")

        host = parsed_uri.hostname
        if parsed_uri.port:
            host = f"{host}:{parsed_uri.port}"
        credentials = f"{quote_plus(username)}:{quote_plus(password)}"
        mongodb_uri = urlunsplit(
            parsed_uri._replace(netloc=f"{credentials}@{host}")
        )

    client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
    database_name = os.getenv("MONGODB_DATABASE", "form_app")
    collection_name = os.getenv("MONGODB_COLLECTION", "submissions")
    return client[database_name][collection_name]


def load_items():
    with DATA_FILE.open(encoding="utf-8") as data_file:
        return json.load(data_file)


@app.get("/api")
def api_items():
    return load_items()


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/submit")
def submit_form():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Name, email, and message are required.", "error")
        return render_template("index.html", form=request.form), 400

    try:
        get_collection().insert_one(
            {"name": name, "email": email, "message": message}
        )
    except (PyMongoError, RuntimeError) as error:
        flash(f"Unable to submit data: {error}", "error")
        return render_template("index.html", form=request.form), 500

    return redirect(url_for("success"))


@app.get("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)

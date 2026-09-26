# Flask Form and MongoDB Atlas Example

A small Flask application with:

- `GET /api`, which returns the list stored in `data/items.json`.
- A frontend form at `/` that inserts submissions into MongoDB Atlas.
- An error state that stays on the form.
- A success redirect to `/success` displaying `Data submitted successfully`.

## Setup

1. Create and activate a virtual environment:

	```bash
	python3.13 -m venv .venv
	source .venv/bin/activate
	```

Use Python 3.10 or newer. Older macOS Python builds may use an outdated
LibreSSL version that cannot complete the TLS handshake with MongoDB Atlas.

2. Install dependencies:

	```bash
	pip install -r requirements.txt
	```

3. In MongoDB Atlas, create a database user, allow the development machine's IP address in Network Access, and copy the cluster connection string.

4. Export the application settings. Use `.env.example` as a template and replace the placeholders:

	```bash
	export FLASK_SECRET_KEY="replace-with-a-random-secret"
	export MONGODB_URI="mongodb+srv://<cluster>.mongodb.net/?retryWrites=true&w=majority"
	export MONGODB_USERNAME="<username>"
	export MONGODB_PASSWORD="<password>"
	export MONGODB_DATABASE="form_app"
	export MONGODB_COLLECTION="submissions"
	```

5. Start the application:

	```bash
	flask --app app run --debug
	```

Open `http://127.0.0.1:5000/` for the form. The JSON API is available at `http://127.0.0.1:5000/api`.

## Validation

The form requires a name, email, and message. Missing fields return HTTP 400 and render the form with an error. MongoDB connection or insert failures return HTTP 500 and render the submitted values with the database error.

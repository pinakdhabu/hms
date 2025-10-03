# Backend — Hotel Management System

This folder contains a Flask backend exposing REST endpoints for the Hotel Management System.

Setup
1. Copy `.env.example` to `.env` and fill DB connection values.
2. Create a virtualenv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Ensure MySQL database `hotel_ms` exists and run `../sql/ddl.sql` and `../sql/seed_data.sql`.
4. Start the server:

```bash
export FLASK_APP=app.py
flask run
```

Notes
- The app uses `db/mysql_db.py` and `db/mongo_db.py` to obtain DB connections. Edit `.env` as necessary.
- Tests in `tests/` are minimal; for full DB testing use a separate test database or mocking.

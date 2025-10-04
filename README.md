# Hotel Management System (Mini Project)

This is my mini project for the Database Management Systems course. I built this project manually to learn how a web app uses both relational and NoSQL databases, and to practice building a small full-stack application from scratch.

Short summary
- A Flask backend (Python) provides REST APIs for rooms, customers, reservations and payments.
- MySQL is used as the primary relational database for core data (customers, rooms, reservations, payments).
- MongoDB is used for optional logs/reviews storage in the project (demoed with a simple collection).
- A lightweight static frontend (HTML/CSS/vanilla JS + Bootstrap) demonstrates booking, viewing/cancelling reservations, making payments and leaving feedback.

What I did (student notes)
- Wrote the backend routes and small business logic in `backend/` using `mysql-connector-python` and `pymongo`.
- Created SQL DDL and seed data in `sql/ddl.sql` and `sql/seed_data.sql` and applied them to a local MySQL server.
- Built simple frontend pages in `frontend/` and a single `frontend/app.js` file to wire the UI to the API.
- Added basic validation and friendly error responses for reservation creation (checks for customer/room and avoids raw DB errors).
- Improved accessibility a little (skip link, focus outlines, ARIA attributes) and basic styling in `frontend/styles.css`.

Quick run instructions (local, no Docker)
1. Install system dependencies: Python 3, MySQL server, MongoDB (optional for reviews).
2. Start MySQL and MongoDB services.
3. Create a Python virtual environment and install backend requirements:

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
```

4. Create the database and apply schema and seed data (adjust user/password as needed):

```sql
-- in your MySQL client as a user with CREATE DATABASE privileges
CREATE DATABASE IF NOT EXISTS hotel_ms;
USE hotel_ms;
SOURCE sql/ddl.sql;
SOURCE sql/seed_data.sql;
```

5. Create a `backend/.env` file with connection settings, for example:

```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=root@2231
MYSQL_DB=hotel_ms
MOCK_MODE=0
```

6. Run the Flask backend (from repository root):

```bash
source backend/.venv/bin/activate
python -m backend.app
# Backend serves APIs and static frontend files on port 5000 by default
```

7. Open a browser and visit: http://127.0.0.1:5000/frontend/index.html

Testing
- Backend unit tests are in `backend/tests/`. Run them with `pytest` while the virtualenv is active.

Notes / caveats
- I used the root MySQL user for development convenience; for production you should create a least-privileged DB user and update `backend/.env`.
- MongoDB is optional in this project—if you don't have it available the backend can fall back to a mock for testing.
- This repo includes sample SQL routines, triggers and a small demo dataset; use the SQL files in `sql/` to rebuild the schema.

If you have questions about any file or want me to walk through the code, ask and I can explain specific parts step-by-step.

Good luck grading!
# Hotel Management System — Mini Project

This repository contains a complete mini-project implementing a Hotel Management System that demonstrates both relational (MySQL) and NoSQL (MongoDB) database features. It is intended as an academic deliverable covering SDLC stages: requirements, design, implementation, testing, and documentation.

Contents
- docs/: Project report, SRS, Design, Testing Plan
- sql/: MySQL DDL, seeds, queries, stored routines (procedures, triggers, cursor examples)
- mongodb/: MongoDB seeds and example scripts (CRUD, aggregations, indexing)
- backend/: Flask backend exposing REST endpoints and unit tests
- frontend/: Simple Bootstrap UI demonstrating booking and feedback flows
- tests/: Manual test cases and automation scaffolding

Requirements (software)
- Python 3.8+
- MySQL 8.x (or compatible 8+ server)
- MongoDB 6.x
- Node.js 18+ (optional for frontend tooling or MongoDB connectivity samples)

Quick setup (developer)
1. Install and start MySQL and MongoDB.
2. Create a MySQL database (e.g., `hotel_ms`) and run `sql/ddl.sql` then `sql/seed_data.sql`.
3. Seed MongoDB by running `node mongodb/mongo_seed.js` (requires `npm i mongodb`).
4. Create a Python virtualenv and install backend dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

5. Configure database connection strings in `backend/.env` (see `backend/README.md` for examples).
6. Run the Flask backend:

```bash
cd backend
flask run --port 5000
```

7. Open `frontend/index.html` in a browser for the UI.

Testing
- Unit tests for backend are in `backend/tests/` and can be run with `pytest`.
- Manual and automation test cases are in `tests/`.

Notes for instructors
- All relational SQL uses MySQL-compatible syntax. Stored routines use MySQL stored procedure syntax and include DECLARE HANDLER for error handling.
- NoSQL examples target MongoDB 6.x APIs and aggregation framework.

License
- MIT

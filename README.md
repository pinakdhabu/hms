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

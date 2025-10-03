# System Design — Hotel Management System

This document describes the high-level design and module decomposition for the Hotel Management System mini-project. It focuses on components, responsibilities, data flows, and reasons behind key structural decisions.

1. Architectural Overview

- Architecture style: Modular, layered MVC-like separation adapted for a small project.
  - Frontend: static single-page UI (HTML + Bootstrap) for demonstrations.
  - Backend: Python Flask REST API (presentation & application logic).
  - Persistence: MySQL for core transactional data (customers, rooms, reservations, payments); MongoDB for semi-structured data (reviews, logs, feedback).

Why this split
- Relational DB (MySQL) ensures ACID properties for bookings/payments where consistency is essential.
- NoSQL (MongoDB) stores reviews and logs because they are schema-flexible and benefit from fast aggregation and indexing for analytics.

2. Major Components

- API Layer (Flask)
  - Responsibility: Expose REST endpoints, validate input, orchestrate transactions between MySQL and MongoDB, handle authentication stubs (future work).
  - Files: `backend/app.py`, `backend/routes/*.py`, `backend/db/mysql.py`, `backend/db/mongo.py`.

- Data Layer
  - MySQL schema: `Customer`, `Room`, `Reservation`, `Payment`, `Staff`. Stored routines implement business calculations (billing, categorization).
  - MongoDB collections: `reviews`, `feedback`, `logs` for analytics and audit.

- Frontend
  - Simple HTML pages and scripts that call REST endpoints. Focus on clarity for instructors rather than production-grade UX.

3. Data Flows

- Booking flow (create reservation): Frontend → POST `/reservations` → Backend validates, opens transaction, inserts `Reservation` in MySQL; upon success write a log in MongoDB `logs` collection.
- Check-in/out flow: Backend updates `Reservation` and `Room` availability; payments recorded in `Payment` table; `proc_CalculateBill` routine used to compute totals.
- Reviews: Frontend submits review → POST `/reviews` → Backend writes to MongoDB `reviews` collection. Aggregation pipelines compute average scores per room type.

4. Transactions and Consistency

- MySQL transactions (BEGIN/COMMIT/ROLLBACK) protect reservation + payment sequences.
- MongoDB writes for logs/reviews are eventually consistent with MySQL state; critical operations log a reference id (`reservation_id`) to correlate.

5. Security and Best Practices

- Parameterized SQL queries (using prepared statements) to avoid injection.
- Input validation at the API boundary.
- Secrets and connection strings are stored in `.env` (not committed); sample `.env.example` included in `backend/`.

6. Extensibility

- The project separates DB access via `backend/db/*` modules to allow swapping databases or adding caching layers.
- Stored procedures encapsulate business logic close to the data for clear demonstration and academic evaluation.

7. Limitations

- Authentication and authorization are out-of-scope for this mini-project but hooks are left in the API layer.
- The frontend is intentionally minimal to emphasize backend and database features.

End of Design document.

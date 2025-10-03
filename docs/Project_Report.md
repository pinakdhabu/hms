# Project Report — Hotel Management System

## Title
Hotel Management System — Mini Project (Relational + NoSQL demonstration)

## Abstract
This project implements a compact Hotel Management System (HMS) that demonstrates the complementary use of relational (MySQL) and NoSQL (MongoDB) databases. The system supports typical hotel operations: room management, reservations, check-ins/check-outs, billing, and guest feedback. The academic scope includes schema design, stored procedures, triggers, and MongoDB aggregation and indexing. The deliverable includes frontend, backend, testing artifacts, and documentation suitable for instructor evaluation.

## Introduction
This mini-project models key operations required by a mid-sized hotel and aims to illustrate how transactional data and semi-structured data coexist in a real application. MySQL stores the core transactional entities (customers, rooms, reservations, payments) ensuring ACID semantics. MongoDB stores reviews, feedback, and application logs enabling flexible schema and fast analytics.

## Objectives
- Design a normalized MySQL schema for hotel operations.
- Implement stored procedures, triggers, and cursor usage for server-side business logic.
- Demonstrate MongoDB CRUD, indexing, and aggregation for analytics and logging.
- Build a Flask backend exposing REST APIs with secure, parameterized queries.
- Provide a simple frontend to showcase booking and feedback flows.
- Create test artifacts and a testing plan for functional verification.

## Scope
In-scope:
- Reservation lifecycle (book, cancel, check-in, check-out)
- Billing computations using stored procedures
- Basic staff management
- Reviews and feedback stored in MongoDB

Out-of-scope:
- Full authentication/authorization
- Payment gateway integration
- Production-grade deployment concerns


## Conclusion
This project is an academic showcase of database features and backend integration patterns. It is written to be easy to set up locally for evaluation and experimentation.

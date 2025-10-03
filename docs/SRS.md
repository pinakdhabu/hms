# Software Requirements Specification (SRS)

## System Overview
The Hotel Management System (HMS) enables customers to book rooms, check in/out, and view billing details. Staff can manage rooms, reservations, and guest information. The system uses MySQL for transactional data and MongoDB for logs, reviews, and feedback.

## Functional Requirements
1. Customer Management
   - FR1.1: Add a new customer with contact details.
   - FR1.2: List customers and search by name or email.

2. Room Management
   - FR2.1: Add rooms with type and rate.
   - FR2.2: Update room availability and rate.
   - FR2.3: List rooms and filter by type or availability.

3. Reservations
   - FR3.1: Create a reservation (customer selects room, check-in/out dates).
   - FR3.2: Cancel reservation (status change to CANCELLED).
   - FR3.3: Check-in and check-out operations.

4. Payments and Billing
   - FR4.1: Record payment for a reservation.
   - FR4.2: Compute bill using stored routine (room rate × nights + tax).
   - FR4.3: Retrieve payment history for a reservation/customer.

5. Reviews and Feedback (MongoDB)
   - FR5.1: Submit review/feedback referencing customer and reservation.
   - FR5.2: Aggregate average review score by room type.

6. Logging and Auditing
   - FR6.1: Log reservation changes to `Reservation_Audit` (MySQL) and `logs` (MongoDB).

## Non-functional Requirements
- NFR1: The system should run on Linux and Windows with minimal adjustments.
- NFR2: Use parameterized queries to prevent SQL injection.
- NFR3: Backend API should respond within 200ms for basic CRUD operations on local dev hardware.
- NFR4: Data durability for reservations and payments (ACID via MySQL).

## Constraints
- Use MySQL for relational artifacts; use MongoDB for NoSQL artifacts.
- Avoid external payment gateways; payments are recorded as simple records.

## Acceptance Criteria
- Endpoints for customers/rooms/reservations/payments/reviews are implemented and tested.
- MySQL scripts (DDL and stored procedures) execute without errors.
- MongoDB sample scripts run and demonstrate aggregation and indexing.

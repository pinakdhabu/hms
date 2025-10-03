# Testing Plan

This testing plan covers functional test cases and NoSQL logging/aggregation checks for the Hotel Management System.

Test objectives
- Validate booking lifecycle (book → check-in → checkout → payment)
- Validate cancellation paths and audit logging
- Validate billing calculation via stored procedure
- Validate MongoDB CRUD and aggregation examples

Test cases (high level)

1. Book a room (happy path)
   - Steps: Create customer → find available room → create reservation → verify `Reservation` created with status BOOKED
   - Expected: Reservation record exists; room availability remains unchanged until check-in

2. Check-in and checkout
   - Steps: Update reservation status to CHECKED_IN → later mark COMPLETED and create Payment
   - Expected: Payment record exists; `proc_CalculateBill` returns expected amount

3. Cancel reservation
   - Steps: Set reservation status to CANCELLED
   - Expected: Reservation_Audit has an entry; reservation no longer appears in active views

4. Billing calculation
   - Steps: Use `proc_CalculateBill` for known reservation
   - Expected: Total equals nights × rate × 1.10 (10% tax)

5. MongoDB reviews aggregation
   - Steps: Insert several reviews for multiple room types; run aggregation pipeline
   - Expected: Average scores per room type computed correctly

6. Log rotation/deletion (MongoDB)
   - Steps: Create logs older than 90 days and run deletion script
   - Expected: Old logs removed

Automation scope
- Basic backend unit tests with pytest cover endpoints and DB functions.
- End-to-end automation (optional) using Cypress to simulate a booking flow and submitting feedback.

Reporting
- Test results recorded in `tests/` and a brief summary is included in `docs/Testing_Plan.md` after execution.

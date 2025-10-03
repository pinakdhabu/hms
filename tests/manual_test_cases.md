# Manual Test Cases

1. End-to-end booking
   - Create customer via POST /customers
   - Note customer_id
   - Use frontend booking form to create reservation
   - Verify reservation via GET /reservations/{id}
   - On checkout, POST payment and verify record in /payments/reservation/{id}

2. Cancel reservation
   - Create or choose an existing reservation
   - POST /reservations/{id}/cancel
   - Check Reservation_Audit table in MySQL for an audit entry

3. Review/Feedback
   - Submit feedback via frontend
   - Verify document present in MongoDB `feedback` collection

4. Billing calculation
   - Use MySQL proc_CalculateBill to compute expected bill for a reservation and compare with Payment amount

5. MongoDB log cleanup
   - Insert logs with old timestamps and run `mongo_crud_examples.js` deletion logic

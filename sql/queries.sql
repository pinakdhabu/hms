-- Useful queries for Hotel Management System (MySQL)
USE hotel_ms;

-- 1) List customers with their reservations and payment totals
SELECT c.customer_id, c.first_name, c.last_name, r.reservation_id, ro.room_number, r.check_in, r.check_out,
  IFNULL(p.amount, 0) AS payment_amount
FROM Customer c
LEFT JOIN Reservation r ON c.customer_id = r.customer_id
LEFT JOIN Room ro ON r.room_id = ro.room_id
LEFT JOIN Payment p ON r.reservation_id = p.reservation_id;

-- 2) Rooms not reserved this week
SELECT * FROM Room WHERE room_id NOT IN (
  SELECT room_id FROM Reservation WHERE check_in BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
);

-- 3) Monthly revenue (payments grouped by month)
SELECT DATE_FORMAT(paid_at, '%Y-%m') AS month, SUM(amount) AS revenue
FROM Payment
GROUP BY month
ORDER BY month DESC;

-- 4) Current active reservations
SELECT * FROM vw_active_reservations;

-- 5) Customers with no reservations
SELECT * FROM Customer WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM Reservation);

-- 6) Top spending customers
SELECT c.customer_id, c.first_name, c.last_name, SUM(p.amount) AS total_spent
FROM Customer c
JOIN Reservation r ON c.customer_id = r.customer_id
JOIN Payment p ON r.reservation_id = p.reservation_id
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- 7) Set operator example: rooms available today vs tomorrow (UNION)
SELECT room_id, room_number, 'today' as day FROM Room WHERE room_id NOT IN (
  SELECT room_id FROM Reservation WHERE check_in <= CURDATE() AND check_out > CURDATE()
)
UNION
SELECT room_id, room_number, 'tomorrow' as day FROM Room WHERE room_id NOT IN (
  SELECT room_id FROM Reservation WHERE check_in <= DATE_ADD(CURDATE(), INTERVAL 1 DAY) AND check_out > DATE_ADD(CURDATE(), INTERVAL 1 DAY)
);

-- 8) Aggregation: average stay length by room type
SELECT ro.room_type, AVG(DATEDIFF(r.check_out, r.check_in)) AS avg_nights
FROM Reservation r
JOIN Room ro ON r.room_id = ro.room_id
GROUP BY ro.room_type;

-- 9) Reservations per day (simple time series)
SELECT check_in AS day, COUNT(*) AS reservations FROM Reservation GROUP BY check_in ORDER BY check_in;

-- 10) Show reservations with no payments
SELECT r.* FROM Reservation r LEFT JOIN Payment p ON r.reservation_id = p.reservation_id WHERE p.payment_id IS NULL;

-- End of queries

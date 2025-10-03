-- Seed sample data for Hotel Management System
USE hotel_ms;

-- Customers
INSERT INTO Customer (first_name, last_name, email, phone) VALUES
('Alice', 'Johnson', 'alice.j@example.com', '555-0101'),
('Bob', 'Smith', 'bob.smith@example.com', '555-0102'),
('Carol', 'Ng', 'carol.ng@example.com', '555-0103'),
('David', 'Lee', 'david.lee@example.com', '555-0104'),
('Eva', 'Khan', 'eva.khan@example.com', '555-0105');

-- Staff
INSERT INTO Staff (name, role, email, phone, hired_at) VALUES
('Raj Patel', 'Manager', 'raj.patel@hotel.com', '555-0201', '2020-02-15'),
('Maya Rao', 'Reception', 'maya.recep@hotel.com', '555-0202', '2021-05-10');

-- Rooms
INSERT INTO Room (room_number, room_type, rate, is_available) VALUES
('101', 'Single', 50.00, TRUE),
('102', 'Single', 55.00, TRUE),
('201', 'Double', 80.00, TRUE),
('202', 'Double', 85.00, TRUE),
('301', 'Suite', 150.00, TRUE);

-- Reservations (3)
INSERT INTO Reservation (customer_id, room_id, check_in, check_out, status) VALUES
(1, 1, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'BOOKED'),
(2, 3, DATE_ADD(CURDATE(), INTERVAL 1 DAY), DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'BOOKED'),
(3, 5, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'BOOKED');

-- Payments (none yet; payments created on checkout)

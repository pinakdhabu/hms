-- MySQL DDL for Hotel Management System

DROP DATABASE IF EXISTS hotel_ms;
CREATE DATABASE hotel_ms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hotel_ms;

-- Customer table
CREATE TABLE Customer (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE,
  phone VARCHAR(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Staff table
CREATE TABLE Staff (
  staff_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  role VARCHAR(50) NOT NULL,
  email VARCHAR(255),
  phone VARCHAR(20),
  hired_at DATE
) ENGINE=InnoDB;

-- Room table
CREATE TABLE Room (
  room_id INT AUTO_INCREMENT PRIMARY KEY,
  room_number VARCHAR(10) UNIQUE NOT NULL,
  room_type VARCHAR(50) NOT NULL,
  rate DECIMAL(8,2) NOT NULL,
  is_available BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Reservation table
CREATE TABLE Reservation (
  reservation_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  room_id INT NOT NULL,
  check_in DATE NOT NULL,
  check_out DATE NOT NULL,
  status ENUM('BOOKED','CANCELLED','CHECKED_IN','COMPLETED') DEFAULT 'BOOKED',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_res_customer FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
  CONSTRAINT fk_res_room FOREIGN KEY (room_id) REFERENCES Room(room_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Payment table
CREATE TABLE Payment (
  payment_id INT AUTO_INCREMENT PRIMARY KEY,
  reservation_id INT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  paid_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  method VARCHAR(50),
  CONSTRAINT fk_pay_res FOREIGN KEY (reservation_id) REFERENCES Reservation(reservation_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Reservation audit table for trigger
CREATE TABLE Reservation_Audit (
  audit_id INT AUTO_INCREMENT PRIMARY KEY,
  reservation_id INT,
  old_status VARCHAR(50),
  new_status VARCHAR(50),
  changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Indexes and views
CREATE INDEX idx_customer_email ON Customer(email);
CREATE INDEX idx_room_type ON Room(room_type);
CREATE INDEX idx_reservation_status ON Reservation(status);

CREATE VIEW vw_active_reservations AS
SELECT r.reservation_id, c.first_name, c.last_name, ro.room_number, r.check_in, r.check_out, r.status
FROM Reservation r
JOIN Customer c ON r.customer_id = c.customer_id
JOIN Room ro ON r.room_id = ro.room_id
WHERE r.status IN ('BOOKED','CHECKED_IN');

-- Sample stored function placeholder (calculations will be in plsql_examples.sql)

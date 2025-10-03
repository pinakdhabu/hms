-- MySQL stored procedures, triggers, and cursor examples for Hotel Management System
USE hotel_ms;

DELIMITER $$

-- Procedure: Calculate total bill (room rate * nights + tax 10%)
DROP PROCEDURE IF EXISTS proc_CalculateBill$$
CREATE PROCEDURE proc_CalculateBill(IN p_reservation_id INT, OUT p_total DECIMAL(10,2))
BEGIN
  DECLARE v_rate DECIMAL(8,2);
  DECLARE v_nights INT;
  DECLARE v_checkin DATE;
  DECLARE v_checkout DATE;
  DECLARE v_base DECIMAL(10,2);
  SET p_total = 0.00;

  SELECT ro.rate, r.check_in, r.check_out INTO v_rate, v_checkin, v_checkout
  FROM Reservation r
  JOIN Room ro ON r.room_id = ro.room_id
  WHERE r.reservation_id = p_reservation_id;

  SET v_nights = GREATEST(DATEDIFF(v_checkout, v_checkin), 1);
  SET v_base = v_rate * v_nights;
  SET p_total = ROUND(v_base * 1.10, 2); -- 10% tax

END$$

-- Procedure: Classify customer by total spending
DROP PROCEDURE IF EXISTS proc_CustomerCategory$$
CREATE PROCEDURE proc_CustomerCategory(IN p_customer_id INT, OUT p_category VARCHAR(20))
BEGIN
  DECLARE v_total_spent DECIMAL(12,2);
  SELECT IFNULL(SUM(p.amount), 0) INTO v_total_spent
  FROM Payment p
  JOIN Reservation r ON p.reservation_id = r.reservation_id
  WHERE r.customer_id = p_customer_id;

  IF v_total_spent >= 5000 THEN
    SET p_category = 'Premium';
  ELSEIF v_total_spent >= 1000 THEN
    SET p_category = 'Regular';
  ELSE
    SET p_category = 'New';
  END IF;
END$$

-- Trigger: log reservation status changes into Reservation_Audit
DROP TRIGGER IF EXISTS reservation_audit_trigger$$
CREATE TRIGGER reservation_audit_trigger
AFTER UPDATE ON Reservation
FOR EACH ROW
BEGIN
  IF OLD.status <> NEW.status THEN
    INSERT INTO Reservation_Audit(reservation_id, old_status, new_status) VALUES (OLD.reservation_id, OLD.status, NEW.status);
  END IF;
END$$

-- Cursor example: compute daily occupancy percentage (simple iteration)
DROP PROCEDURE IF EXISTS proc_ComputeOccupancy$$
CREATE PROCEDURE proc_ComputeOccupancy()
BEGIN
  DECLARE done INT DEFAULT FALSE;
  DECLARE v_room_count INT DEFAULT 0;
  DECLARE v_reservation_count INT;
  DECLARE cur_date DATE;

  DECLARE cur CURSOR FOR SELECT DISTINCT check_in FROM Reservation WHERE status IN ('BOOKED','CHECKED_IN');
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  SELECT COUNT(*) INTO v_room_count FROM Room;
  OPEN cur;
  read_loop: LOOP
    FETCH cur INTO cur_date;
    IF done THEN
      LEAVE read_loop;
    END IF;
    SELECT COUNT(*) INTO v_reservation_count FROM Reservation WHERE check_in = cur_date AND status IN ('BOOKED','CHECKED_IN');
    -- For demonstration we'll insert into Reservation_Audit a note with occupancy in old_status field
    INSERT INTO Reservation_Audit(reservation_id, old_status, new_status) VALUES (NULL, CONCAT('occupancy:', v_reservation_count), CONCAT('rooms:', v_room_count));
  END LOOP;
  CLOSE cur;
END$$

DELIMITER ;

-- Exception handling example (handler) in a procedure
DELIMITER $$
DROP PROCEDURE IF EXISTS proc_SafeInsertCustomer$$
CREATE PROCEDURE proc_SafeInsertCustomer(IN p_first VARCHAR(100), IN p_last VARCHAR(100), IN p_email VARCHAR(255))
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    -- On error, rollback and return
    ROLLBACK;
  END;

  START TRANSACTION;
  INSERT INTO Customer(first_name, last_name, email) VALUES (p_first, p_last, p_email);
  COMMIT;
END$$
DELIMITER ;

-- End of plsql_examples.sql

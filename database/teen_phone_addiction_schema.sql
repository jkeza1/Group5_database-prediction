
-- Step 2: Teen Phone Addiction and Lifestyle Survey - MySQL Schema

-- Table: Teens
CREATE TABLE Teens (
    Teen_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Age INT,
    Gender ENUM('Male', 'Female', 'Other'),
    Location VARCHAR(100),
    School_Grade VARCHAR(50)
);

-- Table: Phone_Usage
CREATE TABLE Phone_Usage (
    Usage_ID INT AUTO_INCREMENT PRIMARY KEY,
    Teen_ID INT,
    Daily_Usage_Hours FLOAT,
    Sleep_Hours FLOAT,
    FOREIGN KEY (Teen_ID) REFERENCES Teens(Teen_ID) ON DELETE CASCADE
);

-- Table: Performance_Stats
CREATE TABLE Performance_Stats (
    Stats_ID INT AUTO_INCREMENT PRIMARY KEY,
    Teen_ID INT,
    Academic_Performance INT,
    Social_Interactions INT,
    FOREIGN KEY (Teen_ID) REFERENCES Teens(Teen_ID) ON DELETE CASCADE
);

-- Stored Procedure: AddPerformanceStats
DELIMITER //

CREATE PROCEDURE AddPerformanceStats(
    IN p_teen_id INT,
    IN p_academic_perf INT,
    IN p_social_interactions INT
)
BEGIN
    INSERT INTO Performance_Stats(Teen_ID, Academic_Performance, Social_Interactions)
    VALUES (p_teen_id, p_academic_perf, p_social_interactions);
END //

DELIMITER ;

-- Trigger: Prevent inserting underage teens
DELIMITER //

CREATE TRIGGER check_age_before_insert
BEFORE INSERT ON Teens
FOR EACH ROW
BEGIN
    IF NEW.Age < 10 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Teen must be at least 10 years old.';
    END IF;
END //

DELIMITER ;

-- Sample Data
INSERT INTO Teens (Name, Age, Gender, Location, School_Grade)
VALUES ('Alice', 15, 'Female', 'NYC', '10th');

INSERT INTO Phone_Usage (Teen_ID, Daily_Usage_Hours, Sleep_Hours)
VALUES (1, 6.5, 7.2);

CALL AddPerformanceStats(1, 85, 78);

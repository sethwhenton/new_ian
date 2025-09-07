-- Create test database + user if doesn't exist
CREATE DATABASE IF NOT EXISTS obj_detect_test_db;
CREATE USER IF NOT EXISTS 'obj_detect_test'@'localhost';
SET PASSWORD FOR 'obj_detect_test'@'localhost' = 'obj_detect_test_pwd';
GRANT ALL ON obj_detect_test_db.* TO 'obj_detect_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'obj_detect_test'@'localhost';
FLUSH PRIVILEGES;

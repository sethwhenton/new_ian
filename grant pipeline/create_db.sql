-- Create database + user if doesn't exist
CREATE DATABASE IF NOT EXISTS obj_detect_dev_db;
CREATE USER IF NOT EXISTS 'obj_detect_dev'@'localhost';
SET PASSWORD FOR 'obj_detect_dev'@'localhost' = 'obj_detect_dev_pwd';
GRANT ALL ON obj_detect_dev_db.* TO 'obj_detect_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'obj_detect_dev'@'localhost';
FLUSH PRIVILEGES;

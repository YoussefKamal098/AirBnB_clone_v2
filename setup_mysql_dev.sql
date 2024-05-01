-- this script prepares a MySQL server for the project
-- Creates a database named hbnb_dev_db if it doesn't already exist.
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
 -- Creates a user named hbnb_dev with the password hbnb_dev_pwd if the user doesn't already exist.
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grants all privileges on the hbnb_dev_db database to the user hbnb_dev when connecting from localhost.
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
-- Reloads the grant tables and applies changes immediately.
FLUSH PRIVILEGES;
-- Grants the SELECT privilege on all tables in the performance_schema database to the user hbnb_dev when connecting from localhost.
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
-- Reloads the grant tables and applies changes immediately.
FLUSH PRIVILEGES;

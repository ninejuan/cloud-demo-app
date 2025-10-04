CREATE DATABASE IF NOT EXISTS userdb 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE userdb;

CREATE TABLE IF NOT EXISTS user (
  id              VARCHAR(255) NOT NULL,
  username        VARCHAR(255) NOT NULL,
  email           VARCHAR(255) NOT NULL,
  status_message  VARCHAR(255) NOT NULL,

  PRIMARY KEY (id),                                
  UNIQUE KEY uk_username (username),               
  KEY idx_email (email)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  ROW_FORMAT=COMPRESSED;

CREATE INDEX idx_email_status ON user(email, status_message(50));

ANALYZE TABLE user;

CREATE USER IF NOT EXISTS 'userapp'@'%' IDENTIFIED BY 'UserApp2025!';
GRANT SELECT, INSERT, UPDATE ON userdb.user TO 'userapp'@'%';

FLUSH PRIVILEGES;

CREATE DATABASE users;
CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
  	username VARCHAR(255) UNIQUE NOT NULL,
   	password VARCHAR(255) NOT NULL
);
CREATE INDEX users
ON users (username);
CREATE INDEX passwords
ON users (password);
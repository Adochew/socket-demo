CREATE DATABASE socket_db;
USE socket_db;

CREATE TABLE `sessions` (
    `session_id` VARCHAR(255) NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `messages` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `session_id` VARCHAR(255) NOT NULL,
    `role` VARCHAR(255),
    `content` TEXT,
    `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_messages_sessions` FOREIGN KEY (`session_id`) REFERENCES `sessions`(`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO sessions (session_id) VALUES ('10001');
INSERT INTO messages (session_id, role, content) VALUES ('10001','user','user test');
INSERT INTO messages (session_id, role, content) VALUES ('10001','assistant','assistant test');
CREATE DATABASE IF NOT EXISTS log_analysis;
USE log_analysis;

CREATE TABLE IF NOT EXISTS system_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  timestamp VARCHAR(64),
  process VARCHAR(128),
  message TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

USE MyLib;
CREATE USER IF NOT EXISTS 'user02'@'localhost' IDENTIFIED BY 'user02pwd';
GRANT ALL PRIVILEGES ON *.* TO 'user02'@'localhost';

-- create table books
USE MyLib;
CREATE TABLE IF NOT EXISTS Books(
   ISBN INT NOT NULL PRIMARY KEY,
   title VARCHAR(256) NOT NULL,
   author VARCHAR(50) NOT NULL,
   editor VARCHAR(50) NOT NULL,
   release_date VARCHAR(50) NOT NULL,
   couverture VARCHAR(256)
);

USE MyLib;
CREATE TABLE User_books(
   user_ID INT,
   book_ID VARCHAR(25),
   status_ID INT,
   FOREIGN KEY(user_ID) REFERENCES Users(ID),
   FOREIGN KEY(book_ID) REFERENCES Books(ISBN),
   FOREIGN KEY(status_ID) REFERENCES Status(ID)
);

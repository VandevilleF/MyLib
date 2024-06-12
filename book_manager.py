#!/usr/bin/python3
from mysql import connector
from utils import popup_error, popup_success


class AddBook:
    """Handle the addition of books to the user's library"""
    @staticmethod
    def add_book(user_id, book_info):
        """Add a book to the user's library if it's not already present"""
        conn = connector.connect(
            host='localhost',
            user='user02',
            password='user02pwd',
            database='MyLib'
            )
        cursor = conn.cursor()

        # Check if the book is already in the user's library
        cursor.execute("SELECT * FROM User_books WHERE user_ID = %s", (user_id,))
        result = cursor.fetchall()
        for book in result:
            if book_info[0] == book[1]:
                popup_error("Livre déjà enregistré")
                return

        # Insert the new book into the user's library
        query = ("INSERT INTO User_books (user_ID, book_ID, status_ID)\
                VALUES (%s, %s, 2);")
        value = (user_id, book_info[0])
        cursor.execute(query, value)
        popup_success("Ajout réussi")

        # Commit the transaction and close connection to the DDb
        conn.commit()
        cursor.close()
        conn.close()

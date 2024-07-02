#!/usr/bin/python3
from utils import popup_error, popup_success, conn_to_ddb


class BookManagement:
    """Handle the addition of books to the user's library"""
    @staticmethod
    def add_book(user_id, book_info):
        """Add a book to the user's library if it's not already present"""
        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Check if the book is already in the user's library
        cursor.execute("SELECT * FROM User_books WHERE user_ID = %s", (user_id,))
        result = cursor.fetchall()
        for book in result:
            if book_info == book[1]:
                popup_error("Livre déjà enregistré")
                return

        # Insert the new book into the user's library
        query = ("INSERT INTO User_books (user_ID, book_ID, status_ID)\
                VALUES (%s, %s, 2);")
        value = (user_id, book_info)
        cursor.execute(query, value)
        popup_success("Ajout réussi")

        # Commit the transaction and close connection to the DDb
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def user_owns_book(user_id, book_id):
        """Check if the user already has the book in their library"""
        conn = conn_to_ddb()
        cursor = conn.cursor()

        query = "SELECT * FROM User_books WHERE user_ID = %s AND book_ID = %s"
        value = (user_id, book_id)
        cursor.execute(query, value)
        result = cursor.fetchone()
        print("Result dans la classe addbook", result)

        cursor.close()
        conn.close()

        return result is not None

    @staticmethod
    def delete_book(user_id, book_info):
        """Delete book to the list of the current user"""
        conn = conn_to_ddb()
        cursor = conn.cursor()

        query = "DELETE FROM User_books WHERE user_ID = %s AND book_ID = %s"
        cursor.execute(query, (user_id, book_info))

        conn.commit()
        cursor.close()
        conn.close()

        popup_success("Livre supprimé")

#!/usr/bin/python3
from kivy.uix.screenmanager import Screen
from utils import get_user_id_jwt, conn_to_ddb


class UserProfile(Screen):
    def on_pre_enter(self):
        """Load user's info on profile page"""
        self.profile()

    def profile(self):
        """Open the user's profile"""
        user_id = get_user_id_jwt()

        conn = conn_to_ddb()
        cursor = conn.cursor()

        query = "SELECT username, mail FROM Users WHERE ID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        print(result)
        if not result or result[0] is None:
            print("Pas d'utilisateur")
            return

        self.ids.nom.text = result[0]
        self.ids.mail.text = result[1]

        cursor.close()
        conn.close()

        self.number_of_books()
        self.book_read()
        self.book_unread()
        self.percent_read()

    def number_of_books(self):
        """Counts the number of books"""
        user_id = get_user_id_jwt()

        conn = conn_to_ddb()
        cursor = conn.cursor()

        query = "SELECT COUNT(book_ID) FROM User_books WHERE user_ID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        print(result)
        if not result or result[0] is None:
            print("Pas de livres")
            return
        self.ids.books_number.text = str(result[0])

    def book_read(self):
        """Count the number of books is read on the user's list"""
        user_id = get_user_id_jwt()

        conn = conn_to_ddb()
        cursor = conn.cursor()

        query = "SELECT COUNT(book_ID) FROM User_books WHERE user_ID = %s AND status_ID = 1"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        print(result)
        if not result or result[0] is None:
            print("Pas de livres lu")
            return 0
        self.ids.books_read.text = str(result[0])

        return result[0]

    def book_unread(self):
        """Count the number of books is unread on the user's list"""
        user_id = get_user_id_jwt()

        conn = conn_to_ddb()
        cursor = conn.cursor()

        query = "SELECT COUNT(book_ID) FROM User_books WHERE user_ID = %s AND status_ID = 2 OR status_ID = 3"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        print(result)
        if not result or result[0] is None:
            print("Pas de livres non lu")
            return 0
        self.ids.books_unread.text = str(result[0])

        return result[0]

    def percent_read(self):
        """Calculate the percent of books read in the user's list"""
        read = self.book_read()
        unread = self.book_unread()

        total = read + unread
        if total == 0:
            return

        percent_r = (read / total) * 100
        print(f"{percent_r: .2f}%")
        self.ids.percent_read.text = f"{percent_r: .2f}%"

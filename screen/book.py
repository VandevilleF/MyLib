#!/usr/bin/python3
from kivy.uix.screenmanager import Screen
from utils import conn_to_ddb, get_user_id_jwt, popup_success


class Book(Screen):
    def display_book(self, book_info):
        """Display info for clicked book"""
        self.book_info = book_info
        conn = conn_to_ddb()
        cursor = conn.cursor()

        query = "SELECT * FROM Books WHERE ISBN = %s"
        cursor.execute(query, (book_info,))
        result = cursor.fetchone()

        if result:
            cover = result[5]
            title = result[1]
            author = result[2]
            editor = result [3]
            release_d = result[4]

        self.ids.cover.source = cover
        self.ids.title.text = title
        self.ids.author.text = author
        self.ids.editor.text = editor
        self.ids.release_d.text = release_d

        cursor.close()
        conn.close()

    def delete_book(self):
        """Delete book to the list of the current user"""
        user_id = get_user_id_jwt()

        conn = conn_to_ddb()
        cursor = conn.cursor()

        query = "DELETE FROM User_books WHERE user_ID = %s AND book_ID = %s"
        cursor.execute(query, (user_id, self.book_info))
        conn.commit()
        popup_success("Livre supprimé")
        self.manager.current = 'UserLib'



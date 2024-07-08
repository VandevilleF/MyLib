#!/usr/bin/python3
from kivy.uix.screenmanager import Screen
from utils import conn_to_ddb, get_user_id_jwt, popup_success
from book_manager import BookManagement


class Book(Screen):
    def on_pre_enter(self):
        """Load status of the user's book"""
        self.load_status()
        self.display_note()

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
            editor = result[3]
            release_d = result[4]
            summary = result[6]

        # Retrieve book info
        self.ids.cover.source = cover
        self.ids.title.text = title
        self.ids.author.text = author
        self.ids.editor.text = editor
        self.ids.release_d.text = release_d
        self.ids.summary.text = summary

        cursor.close()
        conn.close()

    def call_delete(self):
        """Delete book to the list of the current user"""
        user_id = get_user_id_jwt()
        book_info = self.book_info

        BookManagement.delete_book(user_id, book_info)
        self.manager.current = 'UserLib'

    def load_status(self):
        """Checkbox to see the current status of the user's book"""
        user_id = get_user_id_jwt()

        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Load status of the current user's book
        query = "SELECT status_ID FROM User_books WHERE user_ID = %s AND book_ID = %s"
        cursor.execute(query, (user_id, self.book_info))
        result = cursor.fetchone()
        read_status = result[0]

        self.check_box(read_status)

    def checkbox_status(self, instance):
        """Handles the change in checkbox status"""
        # if box is check update the right status
        if instance == self.ids.check_read:
            self.check_box(1)
            self.update_db_status(1)
        elif instance == self.ids.check_unread:
            self.check_box(2)
            self.update_db_status(2)
        elif instance == self.ids.check_in_progress:
            self.check_box(3)
            self.update_db_status(3)

    def check_box(self, value):
        """Check the right box"""
        # Check the right box according to the book's status
        if value == 1:
            # Read status
            self.ids.check_read.active = True
            self.ids.check_unread.active = False
            self.ids.check_in_progress.active = False
        if value == 2:
            # Unread status
            self.ids.check_unread.active = True
            self.ids.check_read.active = False
            self.ids.check_in_progress.active = False
        if value == 3:
            # In progress status
            self.ids.check_in_progress.active = True
            self.ids.check_read.active = False
            self.ids.check_unread.active = False

    def update_db_status(self, status):
        """Update status on the db"""
        user_id = get_user_id_jwt()
        print(user_id)
        print(self.book_info)
        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Update status of the current user's book
        query = "UPDATE User_books SET status_ID = %s WHERE user_ID = %s AND book_ID = %s"
        cursor.execute(query, (status, user_id, self.book_info))

        conn.commit()

        cursor.close()
        conn.close()

    def save_note(self):
        """Save note for the current user's book"""
        user_id = get_user_id_jwt()
        new_note = f"Note : {self.ids.new_note.text}"

        if not new_note:
            return
        else:
            conn = conn_to_ddb()
            cursor = conn.cursor()

            query = "UPDATE User_books SET note = %s WHERE user_ID = %s AND book_ID = %s"
            cursor.execute(query, (new_note, user_id, self.book_info))

            conn.commit()

            # Display content of note in Label on tab book info
            self.display_note()
            popup_success("Note enregistrée")

            cursor.close()
            conn.close()

        self.ids.new_note.text = ""

    def delete_note(self):
        """Delete the current note to the user's book"""
        user_id = get_user_id_jwt()
        note_to_delete = self.ids.user_note.text

        if not note_to_delete:
            return
        else:
            conn = conn_to_ddb()
            cursor = conn.cursor()

            query = "UPDATE User_books SET note = NULL WHERE user_ID = %s AND book_ID = %s"
            cursor.execute(query, (user_id, self.book_info))

            conn.commit()

            self.display_note()
            popup_success("Note supprimée")

            cursor.close()
            conn.close()

    def display_note(self):
        """Display note of the current user's book"""
        user_id = get_user_id_jwt()

        conn = conn_to_ddb()
        cursor = conn.cursor()

        query = "SELECT note FROM User_books WHERE user_ID = %s AND book_ID = %s"
        cursor.execute(query, (user_id, self.book_info))
        result = cursor.fetchone()

        # Check if a note is save on the db
        if result[0] is not None:
            self.ids.user_note.text = result[0]
        else:
            self.ids.user_note.text = ""
            return

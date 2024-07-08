#!/usr/bin/python3
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from screen.book import Book
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from utils import popup_error, conn_to_ddb, get_user_id_jwt


class UserLib(Screen):
    """User library screen"""
    def on_pre_enter(self):
        """Event fired when the screen is about to be used"""
        self.userlib()

    def userlib(self):
        """First display of user's list"""
        self.sort_by_date_added()

    def display_books(self, result):
        """Display the user's books in their library"""
        container = self.ids.container
        container.clear_widgets()

        if all(row == (None, None, None, None) for row in result):
            self.ids.n_element.text = "Pas de livre"
            return

        def update_rect(instance, value):
            """Update the rounded rectangle size and position"""
            instance.canvas.before.children[-1].size = instance.size
            instance.canvas.before.children[-1].pos = instance.pos

        # Display the books in the user's library
        for book in result:
            box_lay = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5, padding=5)

            with box_lay.canvas.before:
                Color(1, 1, 1, 0.55)
                RoundedRectangle(size=box_lay.size, pos=box_lay.pos)
            # Ensure the rounded rectangle resizes with the BoxLayout
            box_lay.bind(size=update_rect)
            box_lay.bind(pos=update_rect)

            image = AsyncImage(source=book[0], size_hint=(1, None), height=50)
            lab_title = Label(text=f"[color=#000000]{book[1]}[/color]",
                              text_size=(container.width, None), font_size=14,
                              halign='center', valign='middle', shorten=True,
                              shorten_from='right', bold=True, markup=True)
            lab_author = Label(text=f"[color=#000000]{book[2]}[/color]",
                               text_size=(container.width, None), font_size=14,
                               halign='center', valign='middle', shorten=True,
                               shorten_from='right', markup=True)
            detail = Button(text="[color=#000000]Détails[/color]", font_size=10, size_hint=(0.5, 1),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            background_color=(0, 0, 0, 0), italic=True, markup=True)
            # Add the book information to the boxlayout
            box_lay.add_widget(image)
            box_lay.add_widget(lab_title)
            box_lay.add_widget(lab_author)
            box_lay.add_widget(detail)

            # Schedule the update_label_properties function to be called after 0.2 seconds
            Clock.schedule_once(lambda dt, label=lab_title: self.update_label_properties(label), 0.2)
            Clock.schedule_once(lambda dt, label=lab_author: self.update_label_properties(label), 0.2)

            book_isbn = book[3]
            detail.bind(on_press=lambda instance,
                        book_info=book_isbn: self.send_book_info(instance, book_info))

            # Add the boxlayout containing the book information to the container
            container.add_widget(box_lay)

        # Update the label showing the number of books
        self.ids.n_element.text = f"Nombre de livres {len(result)}"

    def update_label_properties(self, label):
        """Update label properties like text_size and text truncation"""
        label.text_size = (label.parent.width, None)
        label.shorten = True
        label.shorten_from = 'right'
        label.texture_update()

    def send_book_info(self, instance, book_info):
        """Navigate to Book screen and pass book_info"""
        self.manager.get_screen('Book').display_book(book_info)
        self.manager.current = 'Book'

    def sort_book(self, value):
        """Selected the right sorting method"""
        if value == "Alphabétique":
            self.sort_alphabetically()

        elif value == "Auteur":
            self.sort_by_author()

        elif value == "Date d'ajout":
            self.sort_by_date_added()

    def sort_alphabetically(self):
        """Sorts current user list alphabetically"""
        user_id = get_user_id_jwt()

        if not user_id:
            popup_error("L'utilisateur n'est pas connecté")

        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Fetch the user's books from the DDB order alphabetically
        query = ("SELECT couverture, title, author, ISBN FROM Users LEFT JOIN User_books\
                 ON ID = user_ID LEFT JOIN Books ON ISBN = book_ID WHERE ID = %s\
                     ORDER BY title")
        value = (user_id,)
        cursor.execute(query, value)
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        self.display_books(result)

    def sort_by_author(self):
        """Sorts current user list by authors"""
        user_id = get_user_id_jwt()

        if not user_id:
            popup_error("L'utilisateur n'est pas connecté")

        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Fetch the user's books from the DDB order by author
        query = ("SELECT couverture, title, author, ISBN FROM Users LEFT JOIN User_books\
                 ON ID = user_ID LEFT JOIN Books ON ISBN = book_ID WHERE ID = %s\
                     ORDER BY author, title")
        value = (user_id,)
        cursor.execute(query, value)
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        self.display_books(result)

    def sort_by_date_added(self):
        """Sorts current user list by date added"""
        user_id = get_user_id_jwt()

        if not user_id:
            popup_error("L'utilisateur n'est pas connecté")

        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Fetch the user's books from the DDB order by date added
        query = ("SELECT couverture, title, author, ISBN FROM Users LEFT JOIN User_books\
                 ON ID = user_ID LEFT JOIN Books ON ISBN = book_ID WHERE ID = %s")
        value = (user_id,)
        cursor.execute(query, value)
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        self.display_books(result)

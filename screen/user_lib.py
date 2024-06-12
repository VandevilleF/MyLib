#!/usr/bin/python3
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.app import App
from mysql import connector
from utils import popup_error


class UserLib(Screen):
    """User library screen"""
    def on_pre_enter(self):
        """Event fired when the screen is about to be used"""
        self.userlib()

    def userlib(self):
        """Display the user's books in their library"""
        # Retrieve the user ID from the current running instance of the application
        user_id = App.get_running_app().user_id

        if not user_id:
            popup_error("L'utilisateur n'est pas connecté")

        conn = connector.connect(
            host='localhost',
            user='user02',
            password='user02pwd',
            database='MyLib'
        )
        cursor = conn.cursor()

        # Fetch the user's books from the DDB
        query = ("SELECT couverture, title, author FROM Users LEFT JOIN User_books\
                 ON ID = user_ID LEFT JOIN Books ON ISBN = book_ID WHERE ID = %s")
        value = (user_id,)
        cursor.execute(query, value)
        result = cursor.fetchall()

        container = self.ids.container
        container.clear_widgets()

        # Display the books in the user's library
        for book in result:
            box_lay = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
            image = AsyncImage(source=book[0], size_hint=(1, None), height=50)
            lab_info = Label(text=f"{book[1]}\n{book[2]}",
                             text_size=(container.width, None), font_size=14,
                             halign='center', valign='middle')

            # Add the book information to the boxlayout
            box_lay.add_widget(image)
            box_lay.add_widget(lab_info)

            # Add the boxlayout containing the book information to the container
            container.add_widget(box_lay)

        cursor.close()
        conn.close()

        # Update the label showing the number of books
        self.ids.n_element.text = f"Nombre de livres {len(result)}"


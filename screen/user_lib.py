#!/usr/bin/python3
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from utils import popup_error, conn_to_ddb, get_user_id_jwt


class UserLib(Screen):
    """User library screen"""
    def on_pre_enter(self):
        """Event fired when the screen is about to be used"""
        self.userlib()

    def userlib(self):
        """Display the user's books in their library"""
        # Retrieve the user ID from the current running instance of the application
        user_id = get_user_id_jwt()

        if not user_id:
            popup_error("L'utilisateur n'est pas connecté")

        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Fetch the user's books from the DDB
        query = ("SELECT couverture, title, author FROM Users LEFT JOIN User_books\
                 ON ID = user_ID LEFT JOIN Books ON ISBN = book_ID WHERE ID = %s")
        value = (user_id,)
        cursor.execute(query, value)
        result = cursor.fetchall()

        container = self.ids.container
        container.clear_widgets()

        if all(row == (None, None, None) for row in result):
            self.ids.n_element.text = "Pas de livre"
            return
        # Display the books in the user's library
        for book in result:
            box_lay = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
            image = AsyncImage(source=book[0], size_hint=(1, None), height=50)
            lab_title = Label(text=f"{book[1]}",
                              text_size=(container.width, None), font_size=14,
                              halign='center', valign='middle', shorten=True,
                              shorten_from='right')
            lab_author = Label(text=f"{book[2]}",
                               text_size=(container.width, None), font_size=14,
                               halign='center', valign='middle', shorten=True,
                               shorten_from='right')
            detail = Button(text="Détails", font_size=10, size_hint=(0.5, 1),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            background_color=(0, 0, 0, 0))
            # Add the book information to the boxlayout
            box_lay.add_widget(image)
            box_lay.add_widget(lab_title)
            box_lay.add_widget(lab_author)
            box_lay.add_widget(detail)
            detail.bind(on_press=self.button_click)

            # Add the boxlayout containing the book information to the container
            container.add_widget(box_lay)

        cursor.close()
        conn.close()

        # Update the label showing the number of books
        self.ids.n_element.text = f"Nombre de livres {len(result)}"

    def button_click(self, instance):
        """Open the book screen when the button is clicked"""
        self.manager.current = 'Book'

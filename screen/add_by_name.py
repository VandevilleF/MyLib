#!/usr/bin/python3
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.app import App
from utils import popup_error, conn_to_ddb, get_user_id_jwt
from book_manager import BookManagement


class AddByName(Screen):
    """Adding a book by name or author"""
    def search_book(self):
        """Search for a book by name or author"""
        # Retrieve info from the input fields
        book_name = self.ids.book_name.text
        author_name = self.ids.author_name.text

        # Check if fields are filled in
        if not book_name and not author_name:
            popup_error("Un champ de recherche obligatoire")
            return

        # Check if both fields are filled in
        if book_name and author_name:
            popup_error("Un seul champ de recherche")
            return

        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Search by name
        if book_name:
            query = "SELECT * FROM Books WHERE title LIKE %s"
            value = ('%' + book_name + '%',)
            cursor.execute(query, value)
            result = cursor.fetchall()

            if not result:
                popup_error("Aucun titre trouvé")
                return

        # Search by author
        if author_name:
            query = "SELECT * FROM Books WHERE author LIKE %s"
            value = ('%' + author_name + '%',)
            cursor.execute(query, value)
            result = cursor.fetchall()

            if not result:
                popup_error("Aucun auteur trouvé")
                return

        # Close connection to the DDB
        cursor.close()
        conn.close()
        # Display the search results
        self.display_result(result)

    def display_result(self, result):
        """Display the search results in a popup"""
        user_id = get_user_id_jwt()
        # Initialize layout of popup
        boxpopup = BoxLayout(orientation='vertical')
        button = Button(text="Fermer", size_hint=(0.8, 0.05),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5})
        scroll = ScrollView(size_hint=(1, 1))
        grid_lay = GridLayout(size_hint_y=None, cols=1)
        grid_lay.bind(minimum_height=grid_lay.setter('height'))

        # Create a layout for each book in the search result
        for book in result:
            box_lay = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
            image = AsyncImage(source=book[5], size_hint=(0.2, 1), height=100)
            box_lab = BoxLayout(orientation='vertical', spacing=-30)
            lab_title = Label(text=f"{book[1]}", text_size=(None, None), font_size=14,
                              halign='center', valign='middle', shorten=True,
                              shorten_from='right')
            lab_author = Label(text=f"{book[2]}", text_size=(None, None), font_size=14,
                               halign='center', valign='middle', shorten=True,
                               shorten_from='right')
            lab_info = Label(text=f"{book[3]} / {book[4]}",
                             text_size=(None, None), font_size=14, halign='center',
                             valign='middle', shorten=True, shorten_from='right')

            lab_title.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
            lab_author.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
            lab_info.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))

            # Check if the user already has the book
            has_book = BookManagement.user_owns_book(user_id, book[0])

            checkbox = CheckBox(size_hint=(0.1, 0.2),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                active=has_book)

            # Lambda expression, an anonymous function,
            # used here for a temporary and simple function
            checkbox.bind(active=lambda instance, value,
                          book_info=book[0]: BookManagement.add_book(user_id, book_info)
                          if value else BookManagement.delete_book(user_id, book_info))

            # Add book info to the grid layout
            box_lay.add_widget(image)
            box_lab.add_widget(lab_title)
            box_lab.add_widget(lab_author)
            box_lab.add_widget(lab_info)
            box_lay.add_widget(box_lab)
            box_lay.add_widget(checkbox)
            grid_lay.add_widget(box_lay)

        # Add grid layout to the scroll view
        scroll.add_widget(grid_lay)
        # add the scroll view and close button to the box layout
        boxpopup.add_widget(scroll)
        boxpopup.add_widget(button)

        # Create and open popup
        popup = Popup(title='Résultat de la recherche', content=boxpopup,
                      size_hint=(0.8, 0.8), auto_dismiss=False)
        button.bind(on_press=popup.dismiss)
        popup.open()

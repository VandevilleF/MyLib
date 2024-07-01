#!/usr/bin/python3
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from kivy.app import App
from pyzbar.pyzbar import decode
from PIL import Image
from utils import popup_error, conn_to_ddb, get_user_id_jwt
from book_manager import BookManagement


class AddByBarcode(Screen):
    """Adding a book by ISBN"""
    def search_book_by_isbn(self):
        """Search for a book by ISBN"""
        # Retrieve info from input fields
        text_isbn = self.ids.isbn_book.text

        # Check for ISBN in the DDB
        if text_isbn:
            self.search_isbn(text_isbn)
        else:
            self.scan_isbn()

    def search_isbn(self, text_isbn):
        """Search by a given ISBN """
        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Check if ISBN exits in the DDB
        cursor.execute("SELECT * FROM Books WHERE ISBN = %s", (text_isbn,))
        result = cursor.fetchone()
        # If no book found
        if not result:
            popup_error("Livre non trouvé")

        # Display the search result
        self.display_book(result)

    def scan_isbn(self):
        """Search ISBN by camera"""
        # Retrieve a capture from camera
        self.ids.camera.export_to_png("isbn.png")
        image = Image.open("isbn.png")

        # Decode the ISBN data from the barcode
        decoded_objects = decode(image)

        for obj in decoded_objects:
            # Check if is not a EAN13
            if obj.type != 'EAN13':
                popup_error("Mauvais code barre")
                return
            # Decode the ISBN data
            isbn = obj.data.decode('utf-8')
            print("ISBN Scanné :", isbn)

        # Display the search result
        self.display_book(isbn)

    def display_book(self, result):
        """Display the search result in a popup"""
        user_id = get_user_id_jwt()

        # Initialize layout of popup
        boxpopup = BoxLayout(orientation='vertical')
        button = Button(text="Fermer", size_hint=(0.8, 0.05),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Create a layout for each book in the search result
        box_lay = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
        image = AsyncImage(source=result[5], size_hint=(0.2, 1), height=100)
        box_lab = BoxLayout(orientation='vertical', spacing=-30)
        lab_title = Label(text=f"{result[1]}", text_size=(None, None), font_size=14,
                          halign='center', valign='middle', shorten=True,
                          shorten_from='right')
        lab_author = Label(text=f"{result[2]}", text_size=(None, None), font_size=14,
                           halign='center', valign='middle', shorten=True,
                           shorten_from='right')
        lab_info = Label(text=f"{result[3]} / {result[4]}",
                         text_size=(None, None), font_size=14, halign='center',
                         valign='middle', shorten=True, shorten_from='right')

        lab_title.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        lab_author.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        lab_info.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))

        # Check if the user already has the book
        has_book = BookManagement.user_owns_book(user_id, result[0])

        checkbox = CheckBox(size_hint=(0.1, 0.2),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            active=has_book, disabled=has_book)

        # Lambda expression, an anonymous function,
        # used here for a temporary and simple function
        checkbox.bind(active=lambda instance, value,
                      book_info=result: BookManagement.add_book(user_id, book_info)
                      if value else BookManagement.delete_book(user_id, book_info))

        # Add book info to the layout
        box_lay.add_widget(image)
        box_lab.add_widget(lab_title)
        box_lab.add_widget(lab_author)
        box_lab.add_widget(lab_info)
        box_lay.add_widget(box_lab)
        box_lay.add_widget(checkbox)

        boxpopup.add_widget(box_lay)
        boxpopup.add_widget(button)

        # Create and open popup
        popup = Popup(title='Résultat de la recherche', content=boxpopup,
                      size_hint=(0.8, 0.3), auto_dismiss=False)
        button.bind(on_press=popup.dismiss)
        popup.open()

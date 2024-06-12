#!/usr/bin/python3
import hashlib
import kivy
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from mysql import connector
from pyzbar.pyzbar import decode
from PIL import Image

Window.size = (360, 640)

kivy.require('2.3.0')


def popup_success(message):
    popup = Popup(title='Succès', content=Label(text=message),
                  size_hint=(None, None), size=(350, 100))
    popup.open()


def popup_error(message):
    popup = Popup(title='Erreur', content=Label(text=message),
                  size_hint=(None, None), size=(350, 100))
    popup.open()


def hash_pwd(password):
    hash_obj = hashlib.sha256()
    hash_obj.update(password.encode())
    return hash_obj.hexdigest()


class CreateAccompte(Screen):
    def register_user(self):
        username = self.ids.nom.text
        mail = self.ids.mail.text
        password = hash_pwd(self.ids.mdp.text)
        confirm = hash_pwd(self.ids.confir_mdp.text)

        if not username or not mail or not password or not confirm:
            popup_error("Tous les champs doivent être remplis")
            return

        if password != confirm:
            popup_error("La confirmation est différente du mot de passe")
            return

        conn = connector.connect(
            host='localhost',
            user='user02',
            password='user02pwd',
            database='MyLib'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        username_result = cursor.fetchone()
        if username_result:
            popup_error("Nom déjà utilisé")
            return

        cursor.execute("SELECT * FROM Users WHERE mail = %s", (mail,))
        mail_result = cursor.fetchone()
        if mail_result:
            popup_error("Mail déjà utilisé")
            return

        else:
            query = "INSERT INTO Users (username, mail, password) VALUES (%s, %s, %s)"
            values = (username, mail, password)
            cursor.execute(query, values)
            conn.commit()
            popup_success("Compte créé avec succès")
        # clear input
        self.ids.nom.text = ""
        self.ids.mail.text = ""
        self.ids.mdp.text = ""
        self.ids.confir_mdp.text = ""
        cursor.close()
        conn.close()


class LoginPage(Screen):
    def login_user(self):
        log_user = self.ids.login_user.text
        log_pwd = hash_pwd(self.ids.login_pwd.text)

        conn = connector.connect(
            host='localhost',
            user='user02',
            password='user02pwd',
            database='MyLib'
        )
        cursor = conn.cursor()
        query = "SELECT * FROM Users WHERE username = %s"
        value = (log_user,)
        cursor.execute(query, value)
        result = cursor.fetchone()
        if result:
            if log_pwd == result[3]:
                popup_success("Connection réussie")
                App.get_running_app().user_id = result[0]
                self.manager.current = "UserHome"
            else:
                popup_error("Mot de passe incorrect")
                App.get_running_app().user_id = None
        else:
            popup_error("Nom d'utilisateur incorrect")
            App.get_running_app().user_id = None
        # clear input
        self.ids.login_user.text = ""
        self.ids.login_pwd.text = ""
        conn.close()


class UserHome(Screen):
    pass


class UserLib(Screen):
    def on_pre_enter(self):
        self.userlib()

    def userlib(self):

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
        query = ("SELECT couverture, title, author FROM Users LEFT JOIN User_books\
                 ON ID = user_ID LEFT JOIN Books ON ISBN = book_ID WHERE ID = %s")
        value = (user_id,)
        cursor.execute(query, value)
        result = cursor.fetchall()
        container = self.ids.container
        container.clear_widgets()

        for book in result:
            box_lay = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
            image = AsyncImage(source=book[0], size_hint=(1, None), height=50)
            lab_info = Label(text=f"{book[1]}\n{book[2]}",
                             text_size=(container.width, None), font_size=14,
                             halign='center', valign='middle')

            box_lay.add_widget(image)
            box_lay.add_widget(lab_info)
            container.add_widget(box_lay)
        conn.close()

        self.ids.n_element.text = f"Nombre de livres {len(result)}"
        pass


class AddBookHome(Screen):
    pass


class AddBook:
    @staticmethod
    def add_book(user_id, book_info):
        conn = connector.connect(
            host='localhost',
            user='user02',
            password='user02pwd',
            database='MyLib'
            )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User_books WHERE user_ID = %s", (user_id,))
        result = cursor.fetchall()

        for book in result:
            if book_info[0] == book[1]:
                popup_error("Livre déjà enregistré")
                return

        query = ("INSERT INTO User_books (user_ID, book_ID, status_ID)\
                VALUES (%s, %s, 2);")
        value = (user_id, book_info[0])
        cursor.execute(query, value)
        popup_success("Ajout réussi")

        conn.commit()
        cursor.close()
        conn.close()


class AddByName(Screen):
    def search_book(self):
        book_name = self.ids.book_name.text
        author_name = self.ids.author_name.text

        if not book_name and not author_name:
            popup_error("Un champ de recherche obligatoire")
            return

        if book_name and author_name:
            popup_error("Un seul champ de recherche")
            return

        conn = connector.connect(
            host='localhost',
            user='user02',
            password='user02pwd',
            database='MyLib'
        )
        cursor = conn.cursor()

        if book_name:
            query = "SELECT * FROM Books WHERE title LIKE %s"
            value = ('%' + book_name + '%',)
            cursor.execute(query, value)
            result = cursor.fetchall()

            if not result:
                popup_error("Aucun titre trouvé")
                return

        if author_name:
            query = "SELECT * FROM Books WHERE author LIKE %s"
            value = ('%' + author_name + '%',)
            cursor.execute(query, value)
            result = cursor.fetchall()

            if not result:
                popup_error("Aucun auteur trouvé")
                return

        cursor.close()
        conn.close()
        self.display_result(result)

    def display_result(self, result):
        boxpopup = BoxLayout(orientation='vertical')
        button = Button(text="Fermer", size_hint=(0.8, 0.05),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5})
        scroll = ScrollView(size_hint=(1, 1))
        grid_lay = GridLayout(size_hint_y=None, cols=1)
        grid_lay.bind(minimum_height=grid_lay.setter('height'))

        for book in result:
            box_lay = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
            image = AsyncImage(source=book[5], size_hint=(0.2, 1), height=100)
            lab_info = Label(text=f"{book[1]}\n{book[2]}\n{book[3]} / {book[4]}",
                             text_size=(None, None), font_size=14,
                             halign='center', valign='middle')
            add_button = Button(size_hint=(0.1, 0.2),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
            # Expression lambda, une fonction anonyme,
            # utilisée par besoin d'une fonction temporaire et simple
            add_button.bind(on_press=lambda instance,
                            book_info=book: AddBook.add_book(App.get_running_app().user_id, book_info))
            box_lay.add_widget(image)
            box_lay.add_widget(lab_info)
            box_lay.add_widget(add_button)
            grid_lay.add_widget(box_lay)

        scroll.add_widget(grid_lay)
        boxpopup.add_widget(scroll)
        boxpopup.add_widget(button)

        popup = Popup(title='Résultat de la recherche', content=boxpopup,
                      size_hint=(0.8, 0.8), auto_dismiss=False)
        button.bind(on_press=popup.dismiss)
        popup.open()


class AddByBarcode(Screen):
    def search_book_by_isbn(self):
        text_isbn = self.ids.isbn_book.text

        if text_isbn:
            self.search_isbn(text_isbn)
        else:
            self.scan_isbn()

    def search_isbn(self, text_isbn):
        conn = connector.connect(
            host='localhost',
            user='user02',
            password='user02pwd',
            database='MyLib'
            )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books WHERE ISBN = %s", (text_isbn,))
        result = cursor.fetchone()
        if not result:
            popup_error("Livre non trouvé")

        self.display_book(result)

    def scan_isbn(self):
        self.ids.camera.export_to_png("isbn.png")
        image = Image.open("isbn.png")

        decoded_objects = decode(image)

        for obj in decoded_objects:
            if obj.type != 'EAN13':
                popup_error("Mauvais code barre")
            isbn = obj.data.decode('utf-8')
            print("ISBN Scanné :", isbn)

        self.search_isbn(isbn)

    def display_book(self, result):
        boxpopup = BoxLayout(orientation='vertical')
        button = Button(text="Fermer", size_hint=(0.8, 0.05),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5})

        box_lay = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
        image = AsyncImage(source=result[5], size_hint=(0.2, 1), height=100)
        lab_info = Label(text=f"{result[1]}\n{result[2]}\n{result[3]} / {result[4]}",
                         text_size=(None, None), font_size=14,
                         halign='center', valign='middle')
        add_button = Button(size_hint=(0.1, 0.2),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5})
        # Expression lambda, une fonction anonyme,
        # utilisée par besoin d'une fonction temporaire et simple
        add_button.bind(on_press=lambda instance,
                        book_info=result: AddBook.add_book(App.get_running_app().user_id, book_info))

        box_lay.add_widget(image)
        box_lay.add_widget(lab_info)
        box_lay.add_widget(add_button)

        boxpopup.add_widget(box_lay)
        boxpopup.add_widget(button)

        popup = Popup(title='Résultat de la recherche', content=boxpopup,
                      size_hint=(0.8, 0.3), auto_dismiss=False)
        button.bind(on_press=popup.dismiss)
        popup.open()


class HomePage(Screen):
    pass


class MyLibApp(App):
    user_id = None

    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomePage(name='HomePage'))
        sm.add_widget(CreateAccompte(name='CreateAccompte'))
        sm.add_widget(LoginPage(name='LoginPage'))
        sm.add_widget(UserHome(name='UserHome'))
        sm.add_widget(UserLib(name='UserLib'))
        sm.add_widget(AddBookHome(name='AddBookHome'))
        sm.add_widget(AddByName(name='AddByName'))
        sm.add_widget(AddByBarcode(name='AddByBarcode'))
        return sm


if __name__ == '__main__':
    MyLibApp().run()
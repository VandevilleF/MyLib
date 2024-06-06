#!/usr/bin/python3
import hashlib
import kivy
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from mysql import connector

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
            self.user_id = result[0]
            if log_pwd == result[3]:
                popup_success("Connection réussie")
                self.manager.current = "UserHome"
            else:
                popup_error("Mot de passe incorrect")
                self.user_id = None
        else:
            popup_error("Nom d'utilisateur incorrect")
            self.user_id = None
        # clear input
        self.ids.login_user.text = ""
        self.ids.login_pwd.text = ""
        conn.close()

        return self.user_id


class UserHome(Screen):
    pass


class UserLib(Screen):
    def on_pre_enter(self):
        self.login_page = self.manager.get_screen("LoginPage")
        self.userlib()

    def userlib(self):

        user_id = self.login_page.user_id
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


class HomePage(Screen):
    pass


class MyLibApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomePage(name='HomePage'))
        sm.add_widget(CreateAccompte(name='CreateAccompte'))
        sm.add_widget(LoginPage(name='LoginPage'))
        sm.add_widget(UserHome(name='UserHome'))
        sm.add_widget(UserLib(name='UserLib'))
        return sm


if __name__ == '__main__':
    MyLibApp().run()

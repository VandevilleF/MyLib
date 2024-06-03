#!/usr/bin/python3
import hashlib
import kivy
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
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
        conn.close()
        pass


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
                print("Success")
            else:
                popup_error("Mot de passe incorrect")
        else:
            popup_error("Nom d'utilisateur incorrect")
        return result[0]


class HomePage(Screen):
    pass


class MyLibApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomePage(name='HomePage'))
        sm.add_widget(CreateAccompte(name='CreateAccompte'))
        sm.add_widget(LoginPage(name='LoginPage'))
        return sm


if __name__ == '__main__':
    MyLibApp().run()

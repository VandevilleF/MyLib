#!/usr/bin/python3
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from screen.home_page import HomePage
from screen.create_account import CreateAccount
from screen.login_page import LoginPage
from screen.user_home import UserHome
from screen.user_lib import UserLib
from screen.add_book_home import AddBookHome
from screen.add_by_name import AddByName
from screen.add_by_barcode import AddByBarcode
from utils import get_user_id_jwt, conn_to_ddb


Builder.load_file("screen/HomePage.kv")
Builder.load_file("screen/CreateAccount.kv")
Builder.load_file("screen/LoginPage.kv")
Builder.load_file("screen/UserHome.kv")
Builder.load_file("screen/UserLib.kv")
Builder.load_file("screen/AddBookHome.kv")
Builder.load_file("screen/AddByName.kv")
Builder.load_file("screen/AddByBarcode.kv")

Window.size = (360, 640)

kivy.require('2.3.0')


class MyLibApp(App):
    def build(self):
        self.jwt_token = None
        sm = ScreenManager()
        sm.add_widget(HomePage(name='HomePage'))
        sm.add_widget(CreateAccount(name='CreateAccompte'))
        sm.add_widget(LoginPage(name='LoginPage'))
        sm.add_widget(UserHome(name='UserHome'))
        sm.add_widget(UserLib(name='UserLib'))
        sm.add_widget(AddBookHome(name='AddBookHome'))
        sm.add_widget(AddByName(name='AddByName'))
        sm.add_widget(AddByBarcode(name='AddByBarcode'))

        # Check is a user is logged
        self.check_logged_user(sm)
        return sm

    def check_logged_user(self, sm):
        """Check if a user is logged to the application"""
        conn = conn_to_ddb()
        cursor = conn.cursor()

        query = "SELECT jwt_token FROM Users WHERE jwt_token IS NOT NULL"
        cursor.execute(query)
        result = cursor.fetchone()

        if result and result[0]:
            self.jwt_token = result[0]
            print(f"jwt loaded: {self.jwt_token}")
            sm.current = 'UserHome'
        else:
            print("pas de jwt valide")
            sm.current = 'HomePage'

        cursor.close()
        conn.close()


if __name__ == '__main__':
    MyLibApp().run()

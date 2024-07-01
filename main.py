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
from screen.book import Book
from screen.user_profile import UserProfile
from screen.change_profile import ChangeProfile
from utils import conn_to_ddb, decode_jwt
from dropdown_handlers import handle_menu_selection, handle_profile_selection, reset_dropdown


Builder.load_file("screen/HomePage.kv")
Builder.load_file("screen/CreateAccount.kv")
Builder.load_file("screen/LoginPage.kv")
Builder.load_file("screen/UserHome.kv")
Builder.load_file("screen/UserLib.kv")
Builder.load_file("screen/AddBookHome.kv")
Builder.load_file("screen/AddByName.kv")
Builder.load_file("screen/AddByBarcode.kv")
Builder.load_file("screen/Book.kv")
Builder.load_file("screen/UserProfile.kv")
Builder.load_file("screen/ChangeProfile.kv")

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
        sm.add_widget(Book(name='Book'))
        sm.add_widget(UserProfile(name='UserProfile'))
        sm.add_widget(ChangeProfile(name='ChangeProfile'))

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
            token = result[0]
            decoded_token = decode_jwt(token)
            if decoded_token:
                self.jwt_token = token
                sm.current = 'UserHome'
            else:
                print("pas de jwt valide")
                sm.current = 'HomePage'

        cursor.close()
        conn.close()

    def handle_menu_selection(self, text):
        """Handle the menu selection from the dropdown
        This function is called when an item from the menu dropdown is selected"""
        handle_menu_selection(text)
        reset_dropdown()

    def handle_profile_selection(self, text):
        """Handle the profile selection from the dropdown
        This function is called when an item from the profile dropdown is selected"""
        handle_profile_selection(text)
        reset_dropdown()


if __name__ == '__main__':
    MyLibApp().run()

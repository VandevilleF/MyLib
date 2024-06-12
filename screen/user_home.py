#!/usr/bin/python3
from kivy.uix.screenmanager import Screen
from kivy.app import App
from utils import get_user_id_jwt, conn_to_ddb


class UserHome(Screen):
    """User Home screen"""
    def logout_user(self):
        """log out the current user"""
        user_id = get_user_id_jwt()
        if user_id:
            App.get_running_app().jwt_token = None

            conn = conn_to_ddb()
            cursor = conn.cursor()

            update = "UPDATE Users SET jwt_token = NULL WHERE id = %s"
            cursor.execute(update, (user_id,))

            conn.commit()
            cursor.close()
            conn.close()

        # Redirect to login page
        self.manager.current = 'LoginPage'

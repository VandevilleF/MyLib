#!/usr/bin/python3
from kivy.app import App
from utils import get_user_id_jwt, conn_to_ddb


def handle_menu_selection(text):
    """Handle the menu selection from the dropdown"""
    print("Dropdown menu cliqué")
    pass


def handle_profile_selection(text):
    """Handle the profile selection from the dropdown"""
    if text == "Mon Profil":
        print("Profil ouvert")
        App.get_running_app().root.current = 'UserProfile'
    elif text == "Modifier":
        print("Modification de profil")
        App.get_running_app().root.current = 'ChangeProfile'
    elif text == "Déconnexion":
        print("Déconnexion du profil")
        logout()
        pass


def logout():
    """Log out the current user"""
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
    App.get_running_app().root.current = 'LoginPage'

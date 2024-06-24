#!/usr/bin/python3
from kivy.app import App
from utils import get_user_id_jwt, conn_to_ddb


def handle_menu_selection(text):
    """Handle the menu selection from the dropdown"""
    if text == "Accueil":
        App.get_running_app().root.current = 'UserHome'
    elif text == "Bibliothèque":
        App.get_running_app().root.current = 'UserLib'
    elif text == "Ajout":
        App.get_running_app().root.current = 'AddBookHome'


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


def reset_dropdown():
    """Reset the text of the dropdown spinners to their default values"""
    screen_names = ["UserHome", "UserLib", "UserProfile", "ChangeProfile",
                    "AddByName", "AddByBarcode", "AddBookHome"]

    app = App.get_running_app()

    for screen_n in screen_names:
        screen = app.root.get_screen(screen_n)
        if 'menu_spinner' in screen.ids:
            screen.ids.menu_spinner.text = 'Menu'
        if 'profile_spinner' in screen.ids:
            screen.ids.profile_spinner.text = 'Profil'

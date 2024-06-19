#!/usr/bin/python3
from kivy.uix.screenmanager import Screen
from utils import get_user_id_jwt, conn_to_ddb, hash_pwd, popup_error, popup_success


class ChangeProfile(Screen):
    def on_pre_enter(self):
        self.load_username()
        pass

    def load_username(self):
        """Load the current user's name"""
        user_id = get_user_id_jwt()

        conn = conn_to_ddb()
        cursor = conn.cursor()

        query = "SELECT username FROM Users WHERE ID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if not result or result[0] is None:
            print("Utilisateur inconnu")
            return

        # Display a welcome message
        self.ids.load_username.text = f"Bonjour {result[0]} !"

    def change_username(self):
        """Change username of the current user's"""
        user_id = get_user_id_jwt()
        username = self.ids.new_name.text
        password = hash_pwd(self.ids.pwd.text)

        if not username or not password:
            popup_error("Tous les champs doivent être remplis")
            return

        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Retrieve the password of the current user's
        cursor.execute("SELECT password FROM Users WHERE ID = %s", (user_id,))
        pwd_result = cursor.fetchone()
        pwd_confirm = pwd_result[0]

        if password != pwd_confirm:
            popup_error("Mot de passe incorrect")
            return

        # Check if the username is already in use
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        username_result = cursor.fetchone()
        if username_result:
            popup_error("Nom déjà utilisé")
            return

        query = "UPDATE Users SET username = %s WHERE ID = %s"
        cursor.execute(query, (username, user_id))
        popup_success("Nom changé")

        conn.commit()

        cursor.close()
        conn.close()

        self.ids.new_name.text = ""
        self.ids.pwd.text = ""

        self.load_username()

    def change_mail(self):
        """Change username of the current user's"""
        user_id = get_user_id_jwt()
        mail = self.ids.new_mail.text
        password = hash_pwd(self.ids.pwd_mail.text)

        if not mail or not password:
            popup_error("Tous les champs doivent être remplis")
            return

        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Retrieve the password of the current user's
        cursor.execute("SELECT password FROM Users WHERE ID = %s", (user_id,))
        pwd_result = cursor.fetchone()
        pwd_confirm = pwd_result[0]

        if password != pwd_confirm:
            popup_error("Mot de passe incorrect")
            return

        # Check if the mail is already in use
        cursor.execute("SELECT * FROM Users WHERE mail = %s", (mail,))
        mail_result = cursor.fetchone()
        if mail_result:
            popup_error("Adresse mail déjà utilisée")
            return

        query = "UPDATE Users SET mail = %s WHERE ID = %s"
        cursor.execute(query, (mail, user_id))
        popup_success("Adresse mail changée")

        conn.commit()

        cursor.close()
        conn.close()

        self.ids.new_mail.text = ""
        self.ids.pwd_mail.text = ""

    def change_pwd(self):
        """Change username of the current user's"""
        user_id = get_user_id_jwt()
        old_pwd = hash_pwd(self.ids.old_pwd.text)
        new_pwd = hash_pwd(self.ids.new_pwd.text)
        confirm = hash_pwd(self.ids.confirm.text)

        if not old_pwd or not new_pwd or not confirm:
            popup_error("Tous les champs doivent être remplis")
            return

        if new_pwd != confirm:
            popup_error("La confirmation est différente du mot de passe")
            return

        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Retrieve the password of the current user's
        cursor.execute("SELECT password FROM Users WHERE ID = %s", (user_id,))
        pwd_result = cursor.fetchone()
        pwd_confirm = pwd_result[0]

        if old_pwd != pwd_confirm:
            popup_error("Mot de passe incorrect")
            return

        cursor.execute("SELECT username FROM Users WHERE ID = %s", (user_id,))
        result = cursor.fetchone()
        username = result[0]

        if new_pwd == hash_pwd(username):
            popup_error("Le mot de passe et le nom doivent être différents")
            return

        query = "UPDATE Users SET password = %s WHERE ID = %s"
        cursor.execute(query, (new_pwd, user_id))
        popup_success("Mot de passe changée")

        conn.commit()

        cursor.close()
        conn.close()

        self.ids.old_pwd.text = ""
        self.ids.new_pwd.text = ""
        self.ids.confirm.text = ""

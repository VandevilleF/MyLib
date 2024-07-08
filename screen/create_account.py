#!/usr/bin/python3
from kivy.uix.screenmanager import Screen
from utils import popup_error, popup_success, hash_pwd, conn_to_ddb


class CreateAccount(Screen):
    """Account creation screen"""
    def register_user(self):
        """Register a new user in the DDB"""
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

        if password == hash_pwd(username):
            popup_error("Le mot de passe et le nom doivent être différents")
            return

        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Check if the username is already in use
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        username_result = cursor.fetchone()
        if username_result:
            popup_error("Nom déjà utilisé")
            return

        # Check if the mail is already in use
        cursor.execute("SELECT * FROM Users WHERE mail = %s", (mail,))
        mail_result = cursor.fetchone()
        if mail_result:
            popup_error("Mail déjà utilisé")
            return

        # Insert the new user in the DDB
        else:
            query = "INSERT INTO Users (username, mail, password) VALUES (%s, %s, %s)"
            values = (username, mail, password)
            cursor.execute(query, values)
            conn.commit()
            popup_success("Compte créé avec succès")
            self.manager.current = 'LoginPage'

        # clear input fields
        self.ids.nom.text = ""
        self.ids.mail.text = ""
        self.ids.mdp.text = ""
        self.ids.confir_mdp.text = ""

        # close connection to DDB
        cursor.close()
        conn.close()

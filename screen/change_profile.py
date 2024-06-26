#!/usr/bin/python3
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from utils import get_user_id_jwt, conn_to_ddb, hash_pwd
from utils import popup_error, popup_success


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

    def show_popup(self):
        "Display a confirm popup"
        self.popup_confirm("Voulez vous surpprimer le compte ?")

    def popup_confirm(self, message):
        """Display a confirm popup with a given message"""
        content = BoxLayout(orientation='vertical')
        label = Label(text=message, color=(0, 0, 0, 1))
        content.add_widget(label)

        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.5)
        btn_yes = Button(text="Oui")
        btn_no = Button(text="Non")

        btn_layout.add_widget(btn_yes)
        btn_layout.add_widget(btn_no)
        content.add_widget(btn_layout)

        popup = Popup(title='Attention', title_color=(0, 0, 0, 1), title_align='center',
                      separator_color=(96/255, 96/255, 96/255, 1), content=content,
                      size_hint=(0.8, 0.2), background='images/popup.png')
        popup.open()

        btn_yes.bind(on_release=lambda x: (self.delete_user(), popup.dismiss()))
        btn_no.bind(on_release=popup.dismiss)

    def delete_user(self):
        """Delete the current user"""
        print("utilisateur supprimé")
        user_id = get_user_id_jwt()

        conn = conn_to_ddb()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Users WHERE ID = %s", (user_id,))

        conn.commit()

        popup_success("Compte supprimé")
        self.manager.current = 'HomePage'

        cursor.close()
        conn.close()

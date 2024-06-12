#!/usr/bin/python3
from kivy.uix.screenmanager import Screen
from kivy.app import App
from utils import popup_error, popup_success, hash_pwd, conn_to_ddb, generate_jwt


class LoginPage(Screen):
    """Login screen"""
    def login_user(self):
        """Log user to their account"""
        # Retrieves id values for text fields
        log_user = self.ids.login_user.text
        log_pwd = hash_pwd(self.ids.login_pwd.text)

        conn = conn_to_ddb()
        cursor = conn.cursor()

        # Search for the user in the DDB
        query = "SELECT * FROM Users WHERE username = %s"
        value = (log_user,)
        cursor.execute(query, value)
        result = cursor.fetchone()

        if result:
            # Check if it's the right password
            if log_pwd == result[3]:
                popup_success("Connection réussie")
                # Generate jwt for the user login
                jwt_token = generate_jwt(result[0])

                # Store jwt in the DDB
                update = "UPDATE Users SET jwt_token = %s WHERE username = %s"
                cursor.execute(update, (jwt_token, log_user))
                conn.commit()

                # Store the ID of the logged-in user in the application
                App.get_running_app().jwt_token = jwt_token
                self.manager.current = "UserHome"

            else:
                popup_error("Mot de passe incorrect")
                App.get_running_app().user_id = None

        else:
            popup_error("Nom d'utilisateur incorrect")
            App.get_running_app().user_id = None

        # clear input fields
        self.ids.login_user.text = ""
        self.ids.login_pwd.text = ""

        # Close connection to DDB
        cursor.close()
        conn.close()

#!/usr/bin/python3
import hashlib
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
from mysql import connector
from config import ddb_config, secrete_key
import jwt
from datetime import datetime, timedelta


def popup_success(message):
    """Display a success popup with a given message"""
    popup = Popup(title='Succès', content=Label(text=message),
                  size_hint=(None, None), size=(350, 100))
    popup.open()


def popup_error(message):
    """Display a error popup with a given message"""
    popup = Popup(title='Erreur', content=Label(text=message),
                  size_hint=(None, None), size=(350, 100))
    popup.open()


def hash_pwd(password):
    """Hash a password using the sha256 algorithm"""
    hash_obj = hashlib.sha256()
    hash_obj.update(password.encode())
    return hash_obj.hexdigest()


def conn_to_ddb():
    return connector.connect(
        host=ddb_config['host'],
        user=ddb_config['user'],
        password=ddb_config['password'],
        database=ddb_config['database']
    )


def generate_jwt(user_id):
    """Generate a token on user login"""
    payload = {
        'user_id': user_id,
        'exp': datetime.now() + timedelta(days=1)
    }
    token = jwt.encode(payload, secrete_key, algorithm='HS256')
    return token


def decode_jwt(token):
    """Check and decode token"""
    try:
        decoded_token = jwt.decode(token, secrete_key, algorithms='HS256')
        return decoded_token
    except jwt.ExpiredSignatureError:
        popup_error("Session expiré")
        return None
    except jwt.InvalidTokenError:
        print("Token invalide")
        return None


def get_user_id_jwt():
    """Retrieve the user id from jwt token"""
    jwt_token = App.get_running_app().jwt_token
    if jwt_token:
        decoded_token = decode_jwt(jwt_token)
        if decoded_token:
            return decoded_token.get('user_id')
    return None

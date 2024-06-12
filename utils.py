#!/usr/bin/python3
import hashlib
from kivy.uix.popup import Popup
from kivy.uix.label import Label


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

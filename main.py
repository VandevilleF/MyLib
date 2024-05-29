#!/usr/bin/python3

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

Window.size = (360, 640)

kivy.require('2.3.0')


class CreateAccompte(Screen):
    pass


class LoginPage(Screen):
    pass


class HomePage(Screen):
    pass


class MyLibApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomePage(name='HomePage'))
        sm.add_widget(CreateAccompte(name='CreateAccompte'))
        sm.add_widget(LoginPage(name='LoginPage'))
        return sm


if __name__ == '__main__':
    MyLibApp().run()

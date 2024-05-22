#!/usr/bin/python3

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

kivy.require('2.3.0')


class GameView(BoxLayout):
    def __init__(self):
        super(GameView, self).__init__()


class TestApp(App):
    def build(self):
        return GameView()


if __name__ == '__main__':
    TestApp().run()

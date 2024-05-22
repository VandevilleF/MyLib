#!/usr/bin/python3

import kivy
from kivy.app import App
from kivy.uix.image import Image
kivy.require('2.3.0')


class MyApp(App):
    def build(self):
        return Image(source='logo.jpg')


if __name__ == '__main__':
    MyApp().run()


# https://stackoverflow.com/questions/23651781/how-to-display-an-image-using-kivy

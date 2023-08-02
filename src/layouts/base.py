import kivy

kivy.require("2.2.1")

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button, ButtonBehavior
from kivy.properties import ListProperty

Builder.load_file("src/dl/base.kv")


class CustomButton(Button, ButtonBehavior):
    background = ListProperty((3 / 255, 35 / 255, 61 / 255, 1))

    def on_enter(self):
        self.background = (134 / 255, 187 / 255, 240 / 255, 1)

    def on_leave(self):
        self.background = (3 / 255, 35 / 255, 61 / 255, 1)


class BaseWidget(Widget):
    pass

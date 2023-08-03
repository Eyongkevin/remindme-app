import kivy

kivy.require("2.2.1")

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button, ButtonBehavior

from src.layouts.tabs import TabLayout

Builder.load_file("src/dl/base.kv")


class CustomButton(Button, ButtonBehavior):
    pass


class BaseWidget(Widget):
    pass

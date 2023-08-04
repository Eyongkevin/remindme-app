import kivy

kivy.require("2.2.1")

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button, ButtonBehavior

from src.layouts.tabs import TabLayout  # needed
from src.utils import ROOT_DIR

Builder.load_file(str(ROOT_DIR / "src" / "dl" / "base.kv"))


class CustomButton(Button, ButtonBehavior):
    pass


class BaseWidget(Widget):
    pass

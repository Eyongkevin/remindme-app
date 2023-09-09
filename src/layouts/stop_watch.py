from typing import List, Optional
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class SetStopWatchPopup(Popup):
    def dismiss(self, *_args, **kwargs):
        _args[0].sw_started = True
        return super().dismiss(*_args, **kwargs)


class StopWatchBoxLayout(BoxLayout):
    stopwatch_chosen_mins = ObjectProperty(None)
    label_ins = None

    def get_chosen_min(self, inst):
        StopWatchBoxLayout.label_ins = inst
        return ""

    def pause(self, app):
        app.sw_started = False


class StopWatchLabel(Label):
    label_ins = None

    def set_instance(self, inst):
        StopWatchLabel.label_ins = inst
        return ""


class StopWatchInputText(TextInput):
    def on_text(self, instance, value):
        if StopWatchLabel.label_ins is not None:
            StopWatchLabel.label_ins.text = value + " mins"

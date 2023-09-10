from typing import List, Optional
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class SetStopWatchPopup(Popup):
    def dismiss(self, *_args, **kwargs):
        _args[0].sw_state = "start"
        return super().dismiss(*_args, **kwargs)


class RequestStartPopup(Popup):
    pass


class StopWatchBoxLayout(BoxLayout):
    stopwatch_chosen_mins = ObjectProperty(None)
    label_ins = None

    def get_chosen_min(self, inst):
        StopWatchBoxLayout.label_ins = inst
        return ""

    def pause(self, ins, app):
        if app.sw_state in ["start", "pause"] and app.sw_stop_time is not False:
            if ins.text == "Resume":
                app.sw_state = "start"
                ins.text = "Pause"
            else:
                app.sw_state = "pause"
                ins.text = "Resume"
        else:
            RequestStartPopup().open()

    def reset(self, app):
        app.sw_state = "reset"
        if StopWatchLabel.label_ins is not None:
            StopWatchLabel.label_ins.text = ""


class StopWatchLabel(Label):
    label_ins = None

    def set_instance(self, inst):
        StopWatchLabel.label_ins = inst
        return ""


class StopWatchInputText(TextInput):
    def __init__(self, **kwargs):
        self.root_app = None
        super().__init__(**kwargs)

    def on_text(self, instance, value):
        if StopWatchLabel.label_ins is not None:
            StopWatchLabel.label_ins.text = value + " mins"
            if self.root_app is not None:
                try:
                    self.root_app.sw_stop_time = int(value)
                except ValueError:
                    self.root_app.sw_stop_time = False

from typing import List, Optional
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from src.db.models.remindme import RemindMe
from kivy.properties import ObjectProperty


class UpcominigBoxLayout(BoxLayout):
    upcoming = RemindMe.get_upcoming_reminder()

    def get_upcoming_label(self):
        # breakpoint()
        return self.upcoming.label

    def get_upcoming_alert_time(self):
        return str(self.upcoming.alert_time)

    def get_upcoming_left_time(self):
        # TODO: get left time.
        pass

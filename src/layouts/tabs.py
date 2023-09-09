from typing import List, Optional
from datetime import time
import json
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from src.utils import sort_dict
from src.db.models.remindme import RemindMe
from src.db.schema import DaysEnum, AlertDataType
from src.scheduler import Scheduler
from src.utils import ROOT_DIR
from src.layouts.homeList import RemainderListView, ReminderState
from src.layouts.stop_watch import *

Builder.load_file(str(ROOT_DIR / "src" / "dl" / "tab.kv"))


class TabLayout(TabbedPanel):
    hour = ObjectProperty(None)
    minute = ObjectProperty(None)
    second = ObjectProperty(None)
    sound = ObjectProperty(None)
    popup = ObjectProperty(None)
    label = ObjectProperty(None)
    alert_msg = ObjectProperty(None)
    reminder_list = ObjectProperty()

    alarm_type_checks: set = {0}

    def alarm_type_checkbox(self, instance, value, target):
        if value:
            TabLayout.alarm_type_checks.add(target)
        else:
            TabLayout.alarm_type_checks.discard(target)

    def add(self):
        hour: str = self.hour.text
        minute: str = self.minute.text
        second: str = self.second.text
        alert_time: time = time.fromisoformat(f"{hour}:{minute}:{second}")
        days: List[DaysEnum] = list(CheckBoxLayout.checks.values())
        alert_type: AlertDataType = {
            "popup": self.popup.active,
            "sound": self.sound.active,
        }
        data = {
            "alert_time": alert_time,
            "alert_type": json.dumps(alert_type),
            "label": self.label.text,
            "days": days,
            "active": True,
        }
        remindme: Optional[RemindMe] = RemindMe.insert_data(data=data)
        if remindme is not None:
            self.clear()
            Scheduler().add_reminder(remindme)
            self.reminder_list.data = RemainderListView.append_data(
                self.reminder_list.data, remindme
            )

            # send success message
            self.push_message("Success")

    def clear(self):
        self.hour.text = "00"
        self.minute.text = "00"
        self.second.text = "00"
        self.sound.active = False
        self.popup.active = True
        self.label.text = ""
        OnceBoxLayout.label_ins.text = ""
        CheckBoxLayout.checks = {}

    def push_message(self, message):
        self.alert_msg.text = message
        Clock.schedule_once(self.pull_message, 3)

    def pull_message(self, e):
        self.alert_msg.text = ""


class CheckBoxLayout(CheckBox):
    checks = {}

    def repeat_check(self, instance, value, target):
        if value:
            CheckBoxLayout.checks.update(target)
        else:
            CheckBoxLayout.checks.pop(list(target.keys())[0])
        if OnceBoxLayout.label_ins is not None:
            OnceBoxLayout.label_ins.text = ",".join(
                sort_dict(CheckBoxLayout.checks).values()
            )

    def is_active(self, target):
        return target in CheckBoxLayout.checks.values()


class OnceBoxLayout(BoxLayout):
    once_days = ObjectProperty(None)
    label_ins = None

    def get_days(self, inst):
        OnceBoxLayout.label_ins = inst
        return ""

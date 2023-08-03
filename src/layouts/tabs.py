from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from src.utils import sort_dict

Builder.load_file("src/dl/tab.kv")


class TabLayout(TabbedPanel):
    hour = ObjectProperty(None)
    minute = ObjectProperty(None)
    second = ObjectProperty(None)
    sound = ObjectProperty(None)
    popup = ObjectProperty(None)
    label = ObjectProperty(None)
    alarm_type_checks: set = {0}

    def alarm_type_checkbox(self, instance, value, target):
        if value:
            TabLayout.alarm_type_checks.add(target)
        else:
            TabLayout.alarm_type_checks.remove(target)

    def add(self):
        print(self.hour.text)
        print(self.minute.text)
        print(self.second.text)
        print(self.sound.active)
        print(self.popup.active)
        print(self.label.text)
        print(CheckBoxLayout.checks)
        self.clear()

    def clear(self):
        self.hour.text = "00"
        self.minute.text = "00"
        self.second.text = "00"
        self.sound.active = False
        self.popup.active = True
        self.label.text = ""
        OnceBoxLayout.label_ins.text = ""
        CheckBoxLayout.checks = {}


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

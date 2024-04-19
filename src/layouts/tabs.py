import json
from datetime import date, datetime, time
from typing import List, Optional

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput

from src.db.models.remindme import RemindMe
from src.db.schema import AlertDataType, DaysEnum, InsertDataType
from src.layouts.home import *
from src.layouts.homeList import RemainderListView, ReminderState
from src.layouts.stop_watch import *
from src.scheduler import Scheduler
from src.utils import ROOT_DIR, sort_dict

Builder.load_file(str(ROOT_DIR / "src" / "dl" / "tab.kv"))  # type: ignore


class TabLayout(TabbedPanel):
    hour: Label = ObjectProperty(None)  # type: ignore
    minute = ObjectProperty(None)  # type: ignore
    second = ObjectProperty(None)  # type: ignore
    sound = ObjectProperty(None)  # type: ignore
    popup = ObjectProperty(None)  # type: ignore
    label = ObjectProperty(None)  # type: ignore
    alert_msg = ObjectProperty(None)  # type: ignore
    reminder_list = ObjectProperty()  # type: ignore
    once_days = ObjectProperty(None)  # type: ignore
    add_button = ObjectProperty(None)  # type: ignore
    alarm_type_checks: set[int] = {0}

    def alarm_type_checkbox(self, _, value: bool, target: int) -> None:
        if value:
            TabLayout.alarm_type_checks.add(target)
        else:
            TabLayout.alarm_type_checks.discard(target)

    def add(self):
        hour: str = self.hour.text  # type: ignore
        minute: str = self.minute.text  # type: ignore
        second: str = self.second.text  # type: ignore
        alert_time: time = time.fromisoformat(f"{hour}:{minute}:{second}")
        days: List[DaysEnum] = [DaysEnum[day] for day in CheckBoxLayout.checks.values()]
        alert_type: AlertDataType = {
            "popup": self.popup.active,
            "sound": self.sound.active,
        }
        data: InsertDataType = {
            "alert_time": alert_time,
            "alert_type": json.dumps(alert_type),
            "label": self.label.text,  # type: ignore
            "days": days,
            "active": True,
        }
        remindme: Optional[RemindMe] = RemindMe.insert_data(data=data)
        if remindme is not None:
            self.clear()
            Scheduler().add_reminder(remindme)
            self.reminder_list.data = RemainderListView.append_data(  # type: ignore
                self.reminder_list.data, remindme  # type: ignore
            )
            # add to the instance saved in Scheduler
            Scheduler.data_instance.data = self.reminder_list.data  # type: ignore

            # send success message
            self.push_message("Success")

    def clear(self):
        self.hour.text = "00"
        self.minute.text = "00"  # type: ignore
        self.second.text = "00"  # type: ignore
        self.sound.active = False  # type: ignore
        self.popup.active = True  # type: ignore
        self.label.text = ""  # type: ignore
        OnceBoxLayout.label_ins.text = ""
        CheckBoxLayout.checks = {}

    def push_message(self, message: str) -> None:
        self.alert_msg.text = message  # type: ignore
        Clock.schedule_once(self.pull_message, 3)  # type: ignore

    def pull_message(self, _):
        self.alert_msg.text = ""  # type: ignore

    # def _check_time(txt, type=None):
    #     pass
    #     # if type == 'hr':
    #     #     return all([
    #     #         len(txt) == 2,
    #     #         txt.isnumeric
    #     #     ])

    def try_activate_button(self) -> None:
        if (
            len(self.label.text) > 2  # type: ignore
            and self.once_days.text  # type: ignore
            and len(self.hour.text) == 2  # type: ignore
            and len(self.minute.text) in [1, 2]  # type: ignore
        ):
            try:
                time.fromisoformat(
                    f"{self.hour.text}:{self.minute.text}:{self.second.text}"  # type: ignore
                )
                self.add_button.disabled = False  # type: ignore
            except ValueError:
                self.add_button.disabled = True  # type: ignore
        else:
            self.add_button.disabled = True  # type: ignore


class ReminderListTabbedPanelItem(TabbedPanelItem):
    refresh_date: date | None = None

    def on_release(self, *largs):  # type: ignore
        current_date: date = datetime.now().date()
        if not self.refresh_date == current_date:
            self.refresh_date = current_date
            Scheduler.data_instance.data = RemainderListView.prepare_data()
        return super().on_release(*largs)  # type: ignore


class UpcomingTabbedPanelItem(TabbedPanelItem):
    pass


class CheckBoxLayout(CheckBox):
    checks: dict[int, str] = {}

    def repeat_check(self, _, value: bool, target: dict[int, str]):
        if value:
            CheckBoxLayout.checks.update(target)
        else:
            CheckBoxLayout.checks.pop(list(target.keys())[0])
        if OnceBoxLayout.label_ins is not None:
            OnceBoxLayout.label_ins.text = ",".join(
                sort_dict(CheckBoxLayout.checks).values()
            )

    def is_active(self, target: str):
        check_target: DaysEnum = DaysEnum[target]
        return check_target.value in CheckBoxLayout.checks.values()


class OnceBoxLayout(BoxLayout):
    once_days = ObjectProperty(None)  # type: ignore
    label_ins: Label | None = None

    def get_days(self, inst: Label) -> str:
        OnceBoxLayout.label_ins = inst
        return ""

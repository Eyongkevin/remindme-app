from typing import List

from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from src.db.models.remindme import RemindMe
from src.scheduler import Scheduler
from src.utils import build_dict


class RemainderListView(RecycleView):
    def __init__(self, **kwargs):  # type: ignore
        super(RemainderListView, self).__init__(**kwargs)  # type: ignore
        self.data: list[dict[str, int | str]] = RemainderListView.prepare_data()
        # Set to this instance so that we can override the data
        # state after a reminder plays the audio
        Scheduler.data_instance = self

    @staticmethod
    def prepare_data() -> list[dict[str, int | str]]:
        all_data: list[dict[str, int | str]] = []
        reminders: List[RemindMe] = RemindMe.get_all()
        for reminder in reminders:
            result: dict[str, int | str] = build_dict(
                reminder.id, reminder.label, reminder.alert_time, reminder.active
            )
            all_data.append(result)
        return all_data

    @staticmethod
    def append_data(
        old_reminders: list[dict[str, int | str]], new_reminder: RemindMe
    ) -> list[dict[str, int | str]]:
        result: dict[str, int | str] = build_dict(
            new_reminder.id,
            new_reminder.label,
            new_reminder.alert_time,
            new_reminder.active,
        )
        old_reminders.append(result)
        return old_reminders


class ReminderState(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty()  # type: ignore
    alert_time = StringProperty()  # type: ignore
    active_img = StringProperty()  # type: ignore
    state = StringProperty()  # type: ignore

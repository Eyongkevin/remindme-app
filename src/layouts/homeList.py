from typing import List
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

from src.db.models.remindme import RemindMe
from src.utils import build_dict


class RemainderListView(RecycleView):
    def __init__(self, **kwargs):
        super(RemainderListView, self).__init__(**kwargs)
        self.data = RemainderListView.prepare_data()

    @staticmethod
    def prepare_data():
        all_data = []
        reminders: List[RemindMe] = RemindMe.get_all()
        for reminder in reminders:
            result = build_dict(reminder.label, reminder.alert_time, reminder.active)
            all_data.append(result)
        return all_data

    @staticmethod
    def append_data(old_reminders, new_reminder: RemindMe):
        result = build_dict(
            new_reminder.label, new_reminder.alert_time, new_reminder.active
        )
        old_reminders.append(result)
        return old_reminders


class ReminderState(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty()
    alert_time = StringProperty()
    active_img = StringProperty()
    state = StringProperty()

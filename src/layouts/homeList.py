from typing import List
from collections import namedtuple
from datetime import datetime
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty

from src.db.models.remindme import RemindMe


class RemainderListView(RecycleView):
    def __init__(self, **kwargs):
        super(RemainderListView, self).__init__(**kwargs)
        self.data = self.prepare_data()

    def prepare_data(self):
        all_data = []
        reminders: List[RemindMe] = RemindMe.get_all()
        for reminder in reminders:
            result = {
                "text": reminder.label,
                "other_text": str(reminder.alert_time),
                "active_img": "images/active.png"
                if reminder.active
                else "images/inactive.png",
                "state": "Passed"
                if datetime.now().time() > reminder.alert_time
                else "Pending",
            }
            all_data.append(result)
        return all_data


class ReminderState(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty()
    other_text = StringProperty()
    active_img = StringProperty()
    state = StringProperty()
    # 'images/inactive.png'
    # index = 0

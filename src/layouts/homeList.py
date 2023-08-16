from typing import List
from collections import namedtuple
from datetime import datetime
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty

from src.db.models.remindme import RemindMe

# from kivy.base import runTouchApp


class RemainderListView(RecycleView):
    mock_data = [
        ("DCI Short Break 1", "10:30:00"),
        ("DCI Lunch Break", "12:15:00"),
        ("DCI Short Break 2", "13:40:00"),
    ]

    def __init__(self, **kwargs):
        super(RemainderListView, self).__init__(**kwargs)
        self.data = self.prepare_data()
        # self.data = [{"text": l, "other_text": t} for l, t in self.mock_data]

    def prepare_data(self):
        all_data = []
        reminders: List[RemindMe] = RemindMe.get_all()
        # Reminder = namedtuple("Reminder", "id label days alert_time alert_type active")
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

    # (11, 'first', ['Fri', 'Sat'], datetime.time(19, 27), {'popup': True, 'sound': False}, True)


# [(11, 'first', ['Fri', 'Sat'], datetime.time(19, 27), {'popup': True, 'sound': False}, True),
#  (12, 'second', ['Fri'], datetime.time(19, 30), {'popup': True, 'sound': False}, True)]


class ReminderState(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty()
    other_text = StringProperty()
    active_img = StringProperty()
    state = StringProperty()
    # 'images/inactive.png'
    # index = 0

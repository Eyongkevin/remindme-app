from datetime import datetime
from typing import List, Optional

from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from src.db.models.remindme import RemindMe
from src.scheduler import Scheduler
from src.utils import get_day_name_of_day_numb, get_day_numb_of_day_name


class UpcomingListView(RecycleView):
    def __init__(self, **kwargs):  # type: ignore
        super(UpcomingListView, self).__init__(**kwargs)  # type: ignore
        self.data: list[dict[str, str]] = UpcomingListView.prepare_data()
        # Set to this instance so that we can override the data
        # state after a reminder plays the audio
        Scheduler.upcoming_instance = self

    @staticmethod
    def prepare_data(state: Optional[bool] = None) -> list[dict[str, str]]:
        upcoming: RemindMe | None = RemindMe.get_upcoming_reminder(state)

        if upcoming is None:
            return [{"day": "...", "alert_time": "...", "label": "..."}]

        # =========PREPARE ALERT TIME===========
        alert_time: str = str(upcoming.alert_time)

        today_day_name: str = datetime.today().strftime("%a")
        label: str = upcoming.label
        # breakpoint()
        if today_day_name in upcoming.days:
            today: str = "Today"
            return [{"day": today, "alert_time": alert_time, "label": label}]

        # if not today, calculate the number of hours
        today_day_numb: int = int(datetime.today().strftime("%w")) - 1
        closest_day_numb: float = float("inf")
        day_name: Optional[str] = None
        for day in upcoming.days:
            day_numb: int = get_day_numb_of_day_name(day)
            temp_numb: int = day_numb - today_day_numb
            if temp_numb >= 0:
                if closest_day_numb > temp_numb:
                    closest_day_numb = temp_numb
                    day_name = day

        # get day name from day numb
        # day = get_day_name_of_day_numb(closest_day_numb)
        # breakpoint()
        today: str = day_name if day_name is not None else "..."

        return [{"day": today, "alert_time": alert_time, "label": label}]


class UpcomingState(RecycleDataViewBehavior, BoxLayout):
    day = StringProperty()  # type: ignore
    alert_time = StringProperty()  # type: ignore
    label = StringProperty()  # type: ignore


# class UpcominigBoxLayout(BoxLayout):
#     def __init__(self, **kwargs):
#         super(UpcominigBoxLayout, self).__init__(**kwargs)
#         self.upcoming: Optional[RemindMe] = RemindMe.get_upcoming_reminder()
#         Scheduler.upcoming_instance = self

#     def get_upcoming_label(self):
#         # breakpoint()
#         return self.upcoming.label if self.upcoming is not None else "---"

#     def get_upcoming_alert_time(self):
#         return str(self.upcoming.alert_time) if self.upcoming is not None else "..."

#     def get_upcoming_left_time(self):
#         # TODO: get left time.
#         pass

#     def get_upcoming_day(self):
#         if self.upcoming is None:
#             return "..."
#         # if today is found, return 'Today'
#         today_day_name = datetime.today().strftime("%a")
#         # breakpoint()
#         if today_day_name in self.upcoming.days:
#             return "Today"

#         # if not today, calculate the number of hours
#         today_day_numb = int(datetime.today().strftime("%w")) - 1
#         closest_day_numb = float("inf")
#         day_name = None
#         for day in self.upcoming.days:
#             day_numb = get_day_numb_of_day_name(day)
#             temp_numb = day_numb - today_day_numb
#             if temp_numb >= 0:
#                 if closest_day_numb > temp_numb:
#                     closest_day_numb = temp_numb
#                     day_name = day

#         # get day name from day numb
#         # day = get_day_name_of_day_numb(closest_day_numb)
#         # breakpoint()
#         return day_name if day_name is not None else "..."

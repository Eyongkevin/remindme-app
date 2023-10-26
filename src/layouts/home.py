from typing import List, Optional
from kivy.uix.boxlayout import BoxLayout
from src.db.models.remindme import RemindMe


class UpcominigBoxLayout(BoxLayout):
    upcoming: Optional[RemindMe] = RemindMe.get_upcoming_reminder()

    def get_upcoming_label(self):
        # breakpoint()
        return self.upcoming.label if self.upcoming is not None else '---'

    def get_upcoming_alert_time(self):
        return str(self.upcoming.alert_time) if self.upcoming is not None else '...'

    def get_upcoming_left_time(self):
        # TODO: get left time.
        pass

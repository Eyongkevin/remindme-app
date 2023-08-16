from typing import List
import schedule
from src.db.models.remindme import RemindMe
from src.audio import Audio


class Scheduler:
    scheduled_reminders = {}

    def __init__(self) -> None:
        self.audio = Audio()

    def schedule_all(self):
        reminders: List[RemindMe] = RemindMe.get_reminder_by_cols("active=1,")
        for reminder in reminders:
            self.add_reminder(reminder)

    def add_reminder(self, reminder: RemindMe):
        for day in reminder.days:
            if day == "Mon":
                alert = (
                    schedule.every()
                    .monday.at(reminder.alert_time.isoformat())
                    .do(self.audio.play)
                )
            elif day == "Tue":
                alert = (
                    schedule.every()
                    .tuesday.at(reminder.alert_time.isoformat())
                    .do(self.audio.play)
                )
            elif day == "Wed":
                alert = (
                    schedule.every()
                    .wednesday.at(reminder.alert_time.isoformat())
                    .do(self.audio.play)
                )
            elif day == "Thur":
                alert = (
                    schedule.every()
                    .thursday.at(reminder.alert_time.isoformat())
                    .do(self.audio.play)
                )
            elif day == "Fri":
                alert = (
                    schedule.every()
                    .friday.at(reminder.alert_time.isoformat())
                    .do(self.audio.play)
                )
            elif day == "Sat":
                alert = (
                    schedule.every()
                    .saturday.at(reminder.alert_time.isoformat())
                    .do(self.audio.play)
                )
            elif day == "Sun":
                alert = (
                    schedule.every()
                    .sunday.at(reminder.alert_time.isoformat())
                    .do(self.audio.play)
                )
            Scheduler.scheduled_reminders[
                reminder.id
            ] = Scheduler.scheduled_reminders.get(reminder.id, {}) | {day: alert}

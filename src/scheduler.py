from typing import List
import schedule
from src.db.models.remindme import RemindMe
from src.audio import Audio


class Scheduler:
    scheduled_reminders = {}
    data_instance = None

    def __init__(self) -> None:
        self.audio = Audio()

    def schedule_all(self):
        reminders: List[RemindMe] = RemindMe.get_reminder_by_active_cols(True)
        for reminder in reminders:
            self.add_reminder(reminder)

    def add_reminder(self, reminder: RemindMe):
        for day in reminder.days:
            if day == "Mon":
                alert = (
                    schedule.every()
                    .monday.at(reminder.alert_time.isoformat())
                    .do(self.run_reminder, reminder_id=reminder.id)
                )
            elif day == "Tue":
                alert = (
                    schedule.every()
                    .tuesday.at(reminder.alert_time.isoformat())
                    .do(self.run_reminder, reminder_id=reminder.id)
                )
            elif day == "Wed":
                alert = (
                    schedule.every()
                    .wednesday.at(reminder.alert_time.isoformat())
                    .do(self.run_reminder, reminder_id=reminder.id)
                )
            elif day == "Thu":
                alert = (
                    schedule.every()
                    .thursday.at(reminder.alert_time.isoformat())
                    .do(self.run_reminder, reminder_id=reminder.id)
                )
            elif day == "Fri":
                alert = (
                    schedule.every()
                    .friday.at(reminder.alert_time.isoformat())
                    .do(self.run_reminder, reminder_id=reminder.id)
                )
            elif day == "Sat":
                alert = (
                    schedule.every()
                    .saturday.at(reminder.alert_time.isoformat())
                    .do(self.run_reminder, reminder_id=reminder.id)
                )
            elif day == "Sun":
                alert = (
                    schedule.every()
                    .sunday.at(reminder.alert_time.isoformat())
                    .do(self.run_reminder, reminder_id=reminder.id)
                )
            Scheduler.scheduled_reminders[
                reminder.id
            ] = Scheduler.scheduled_reminders.get(reminder.id, {}) | {day: alert}

    def run_reminder(self, reminder_id: int):
        # Override the reminder's state
        for item in Scheduler.data_instance.data:
            if item["id"] == reminder_id:
                idx = Scheduler.data_instance.data.index(item)
                Scheduler.data_instance.data[idx]["state"] = "Passed"
                break
        # Play the audio
        self.audio.play()

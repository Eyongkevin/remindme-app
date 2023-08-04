import schedule
from src.db.database import get_active_reminder
from src.audio import Audio


class Scheduler:
    scheduled_reminders = {}

    def __init__(self) -> None:
        self.audio = Audio()

    def schedule_all(self):
        reminders = get_active_reminder()
        for reminder in reminders:
            self.add_reminder(reminder)

    def add_reminder(self, reminder):
        alert_id, days, alert_time, alert_type = reminder
        for day in days:
            if day == "Mon":
                alert = (
                    schedule.every()
                    .monday.at(alert_time.isoformat())
                    .do(self.audio.play)
                )
            elif day == "Tue":
                alert = (
                    schedule.every()
                    .tuesday.at(alert_time.isoformat())
                    .do(self.audio.play)
                )
            elif day == "Wed":
                alert = (
                    schedule.every()
                    .wednesday.at(alert_time.isoformat())
                    .do(self.audio.play)
                )
            elif day == "Thur":
                alert = (
                    schedule.every()
                    .thursday.at(alert_time.isoformat())
                    .do(self.audio.play)
                )
            elif day == "Fri":
                alert = (
                    schedule.every()
                    .friday.at(alert_time.isoformat())
                    .do(self.audio.play)
                )
            elif day == "Sat":
                alert = (
                    schedule.every()
                    .saturday.at(alert_time.isoformat())
                    .do(self.audio.play)
                )
            elif day == "Sun":
                alert = (
                    schedule.every()
                    .sunday.at(alert_time.isoformat())
                    .do(self.audio.play)
                )
            Scheduler.scheduled_reminders[alert_id] = Scheduler.scheduled_reminders.get(
                alert_id, {}
            ) | {day: alert}

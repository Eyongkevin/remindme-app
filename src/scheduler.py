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

    def set_reminder_to_passed(self, reminder_id):
        """change the reminder state that just alarmed to `passed`

        The only way I could get this to work was to
        - Get the reminder and change the state
        - delete that reminder from the total data of reminders
        - Then append them again.

        Args:
            reminder_id (int): ID of reminder to change the state.
        """
        data = Scheduler.data_instance.data
        for item in data:
            if item["id"] == reminder_id:
                idx = data.index(item)
                data[idx]["state"] = "[color=#f74728]Passed[/color]"
                modified_reminder = data[idx]
                data.remove(modified_reminder)
                Scheduler.data_instance.data = data + [modified_reminder]
                break

    def run_reminder(self, reminder_id: int):
        # Override the reminder's state
        self.set_reminder_to_passed(reminder_id)
        # Play the audio
        self.audio.play()

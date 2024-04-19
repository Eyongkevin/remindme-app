from datetime import datetime, timedelta
from typing import Any, List

import schedule

from src.audio import Audio
from src.db.models.remindme import RemindMe


class Scheduler:
    scheduled_reminders: dict[int, dict[str, schedule.Job | None]] = {}
    data_instance: Any = (
        None  # if the class is import here, we will have cyclic import error
    )
    upcoming_instance: Any = None

    def __init__(self) -> None:
        self.audio: Audio = Audio()

    def schedule_all(self) -> None:
        reminders: List[RemindMe] = RemindMe.get_reminder_by_active_cols(True)
        for reminder in reminders:
            self.add_reminder(reminder)

    def add_reminder(self, reminder: RemindMe) -> None:
        alert: schedule.Job | None = None

        for day in reminder.days:
            if day == "Mon":
                alert = (
                    schedule.every()
                    .monday.at(reminder.alert_time.isoformat())  # type: ignore
                    .do(self.run_reminder, reminder_id=reminder.id)  # type: ignore
                )
            elif day == "Tue":
                alert = (
                    schedule.every()
                    .tuesday.at(reminder.alert_time.isoformat())  # type: ignore
                    .do(self.run_reminder, reminder_id=reminder.id)  # type: ignore
                )
            elif day == "Wed":
                alert = (
                    schedule.every()
                    .wednesday.at(reminder.alert_time.isoformat())  # type: ignore
                    .do(self.run_reminder, reminder_id=reminder.id)  # type: ignore
                )
            elif day == "Thu":
                alert = (
                    schedule.every()
                    .thursday.at(reminder.alert_time.isoformat())  # type: ignore
                    .do(self.run_reminder, reminder_id=reminder.id)  # type: ignore
                )
            elif day == "Fri":
                alert = (
                    schedule.every()
                    .friday.at(reminder.alert_time.isoformat())  # type: ignore
                    .do(self.run_reminder, reminder_id=reminder.id)  # type: ignore
                )
            elif day == "Sat":
                alert = (
                    schedule.every()
                    .saturday.at(reminder.alert_time.isoformat())  # type: ignore
                    .do(self.run_reminder, reminder_id=reminder.id)  # type: ignore
                )
            elif day == "Sun":
                alert = (
                    schedule.every()
                    .sunday.at(reminder.alert_time.isoformat())  # type: ignore
                    .do(self.run_reminder, reminder_id=reminder.id)  # type: ignore
                )
            Scheduler.scheduled_reminders[reminder.id] = (
                Scheduler.scheduled_reminders.get(reminder.id, {}) | {day: alert}
            )

    def set_reminder_to_passed(self, reminder_id: int) -> None:
        """change the reminder state that just alarmed to `passed`

        The only way I could get this to work was to
        - Get the reminder and change the state
        - delete that reminder from the total data of reminders
        - Then append them again.

        Args:
            reminder_id (int): ID of reminder to change the state.
        """
        data: list[dict[str, int | str]] = Scheduler.data_instance.data
        for item in data:
            if item["id"] == reminder_id:
                idx = data.index(item)
                data[idx]["state"] = "[color=#f74728]Passed[/color]"
                modified_reminder = data[idx]
                data.remove(modified_reminder)
                Scheduler.data_instance.data = data + [modified_reminder]
                break

    def set_upcoming_to_next(self):
        # Scheduler.upcoming_instance.upcoming = None
        data = Scheduler.upcoming_instance.prepare_data(True)
        print("Next upcoming: ", data)
        Scheduler.upcoming_instance.data = data
        return schedule.CancelJob

    def run_reminder(self, reminder_id: int):
        # Override the reminder's state
        self.set_reminder_to_passed(reminder_id)

        schedule.every().day.at(  # type: ignore
            (datetime.now() + timedelta(seconds=10)).strftime("%H:%M:%S")
        ).do(self.set_upcoming_to_next)
        # Play the audio
        self.audio.play()

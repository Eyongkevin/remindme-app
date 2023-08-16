from typing import List
from src.db.database import Database
from src.db.serializers import serialize_filter


class RemindMe:
    def __init__(
        self,
        id,
        label=None,
        days=None,
        alert_time=None,
        type=None,
        active=None,
        created_at=None,
        modified_at=None,
    ):
        self.id = id
        self.label = label
        self.days = days
        self.alert_time = alert_time
        self.type = type
        self.active = active
        self.created_at = created_at
        self.modified_at = modified_at

    @classmethod
    def get_all(cls) -> List["RemindMe"]:
        conn = Database()
        query = """
            SELECT 
                id,
                label,
                days,
                alert_time,
                type,
                active,
                created_at,
                modified_at
            FROM remindmeapp;
        """

        with conn.cursor() as cursor:
            cursor.execute(query)
            reminders = cursor.fetchall()
            if reminders is not None:
                return [cls(*reminder) for reminder in reminders]
            return []

    @classmethod
    def get_reminder_by_cols(cls, filter) -> List["RemindMe"]:
        conn = Database()
        filter, values = serialize_filter(filter)
        query = f"""
            SELECT 
                id,
                label,
                days,
                alert_time,
                type,
                active,
                created_at,
                modified_at
            FROM remindmeapp
            WHERE {filter};
        """
        with conn.cursor() as cursor:
            cursor.execute(
                query,
                values,
            )
            reminders = cursor.fetchall()
            if reminders is not None:
                return [cls(*reminder) for reminder in reminders]
            return []

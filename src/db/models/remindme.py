from typing import List, Optional
from src.db.database import Database
from src.db.serializers import serialize_filter
from src.db.schema import InsertDataType


class RemindMe:
    def __init__(
        self,
        id,
        label=None,
        alert_time=None,
        days=None,
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
                alert_time,
                days,
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
                alert_time,
                days,
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

    @classmethod
    def insert_data(cls, data: InsertDataType) -> Optional["RemindMe"]:
        conn = Database()
        query = """
        INSERT INTO remindmeapp(
            label,
            alert_time,
            days,
            type,
            active
        ) VALUES (%s,%s,%s,%s,%s) RETURNING *;
        """
        with conn.cursor() as cursor:
            cursor.execute(
                query,
                [
                    data["label"],
                    data["alert_time"],
                    data["days"],
                    data["alert_type"],
                    data["active"],
                ],
            )
            redmindme = cursor.fetchone()
            conn.commit()
            return cls(*redmindme) if redmindme else None

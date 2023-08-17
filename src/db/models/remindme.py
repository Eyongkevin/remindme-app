from typing import List, Optional
from pathlib import Path
from src.db.database import Database
from src.db.schema import InsertDataType
from src.utils import ROOT_DIR, load_sql


class RemindMe:
    queries = load_sql(Path(ROOT_DIR) / "src" / "db" / "sql" / "remindme")

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
        reminders = cls.queries.fetch_all(conn)
        return [cls(*reminder) for reminder in reminders]

    @classmethod
    def get_reminder_by_active_cols(cls, active) -> List["RemindMe"]:
        conn = Database()
        reminders = cls.queries.fetch_by_active(conn, active=active)
        return [cls(*reminder) for reminder in reminders]

    @classmethod
    def insert_data(cls, data: InsertDataType) -> Optional["RemindMe"]:
        conn = Database()
        reminder = cls.queries.insert(
            conn,
            data["label"],
            data["alert_time"],
            data["days"],
            data["alert_type"],
            data["active"],
        )[0]
        conn.commit()
        return cls(*reminder) if reminder else None

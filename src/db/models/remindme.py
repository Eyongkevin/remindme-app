import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from src.db.database import Database
from src.db.schema import InsertDataType
from src.utils import ROOT_DIR, load_sql


class RemindMe:
    __queries = load_sql(Path(ROOT_DIR) / "src" / "db" / "sql" / "remindme")

    def __init__(
        self,
        id,
        label: str,
        alert_time: datetime.time,
        days: str = "",
        type=None,
        active: bool = True,
        created_at=None,
        modified_at=None,
    ):
        self.id: int = id
        self.label = label
        self.days: str = days
        self.alert_time = alert_time
        self.type = type
        self.active = active
        self.created_at = created_at
        self.modified_at = modified_at

    @classmethod
    def get_all(cls) -> List["RemindMe"]:
        conn = Database()
        reminders = cls.__queries.fetch_all(conn)
        return [cls(*reminder) for reminder in reminders]

    @classmethod
    def get_upcoming_reminder(
        cls, state: Optional[bool] = None
    ) -> Optional["RemindMe"]:
        conn = Database()
        if state is not None:
            reminder: List[Tuple["RemindMe"]] = cls.__queries.fetch_next_refresh(conn)
            if len(reminder) > 1:
                reminder = [reminder[1]]
        else:
            reminder: List[Tuple["RemindMe"]] = cls.__queries.fetch_next(conn)
        return cls(*reminder[0]) if reminder else None

    @classmethod
    def get_reminder_by_active_cols(cls, active: bool) -> List["RemindMe"]:
        conn = Database()
        reminders = cls.__queries.fetch_by_active(conn, active=active)
        return [cls(*reminder) for reminder in reminders]

    @classmethod
    def insert_data(cls, data: InsertDataType) -> Optional["RemindMe"]:
        conn = Database()
        reminder = cls.__queries.insert( # type: ignore
            conn,
            data["label"],
            data["alert_time"],
            [day.value for day in data["days"]],
            data["alert_type"],
            data["active"],
        )[0]
        conn.commit()
        return cls(*reminder) if reminder else None

from datetime import time
from enum import Enum
from typing import List, TypedDict


class DaysEnum(Enum):
    Mon = "Mon"
    Tue = "Tue"
    Wed = "Wed"
    Thu = "Thu"
    Fri = "Fri"
    Sat = "Sat"
    Sun = "Sun"


class AlertDataType(TypedDict):
    popup: bool
    sound: bool


class InsertDataType(TypedDict):
    alert_time: time
    alert_type: str  # AlertDataType
    label: str
    days: List[DaysEnum]
    active: bool

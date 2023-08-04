from typing import TypedDict, List
from enum import Enum
from datetime import time


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
    alert_type: AlertDataType
    label: str
    days: List[DaysEnum]
    active: bool

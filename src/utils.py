import datetime
from pathlib import Path

import anosql  # this seems to only work with pycopg2.
import psycopg2
from kivy.core.text import LabelBase

# from src.db.models.remindme import RemindMe

ROOT_DIR: Path = Path(__file__).parent.parent

DAY_NAME_TO_DAY_NUMB: dict[str, int] = {
    "Mon": 0,
    "Tue": 1,
    "Wed": 2,
    "Thu": 3,
    "Fri": 4,
    "Sat": 5,
    "Sun": 6,
}


def sort_dict(data: dict[int, str]) -> dict[int, str]:
    return {k: data[k] for k in sorted(data)}


def load_sql(path: Path):
    queries = None
    for file in path.iterdir():
        if file.is_file() and file.name.endswith(".sql"):
            query = anosql.from_path(str(file), "psycopg2")  # type: ignore
            if queries:
                for qname in query.available_queries:  # type: ignore
                    queries.add_query(qname, getattr(query, qname))  # type: ignore
            else:
                queries = query
    return queries


def build_dict(
    id: int,
    label: str,
    alert_time: datetime.time,
    active: bool,
) -> dict[str, int | str]:
    return {
        "id": id,
        "text": label,
        "alert_time": str(alert_time),
        "active_img": "images/active.png" if active else "images/inactive.png",
        "state": (
            "[color=#f74728]Passed[/color]"
            if datetime.datetime.now().time() > alert_time
            else "Pending"
        ),
    }


def load_fonts() -> None:
    font_path: Path = ROOT_DIR / "static" / "fonts" / "Roboto"
    LabelBase.register(  # type: ignore
        name="Roboto",
        fn_regular=str(font_path / "Roboto-Thin.ttf"),
        fn_bold=str(font_path / "Roboto-Medium.ttf"),
    )


def seconds_until_midnight() -> int:
    now = datetime.datetime.now()
    tomorrow = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
    return abs(tomorrow - now).seconds


def get_day_numb_of_day_name(day_name: str) -> int:
    return DAY_NAME_TO_DAY_NUMB[day_name]


def get_day_name_of_day_numb(day_numb: int) -> str | None:
    result = list(filter(lambda x: x[1] == day_numb, DAY_NAME_TO_DAY_NUMB.items()))
    if len(result) > 0:
        return result[0][0]

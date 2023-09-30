from pathlib import Path
import datetime
from kivy.core.text import LabelBase
import anosql  # this seems to only work with pycopg2.
import psycopg2

# from src.db.models.remindme import RemindMe

ROOT_DIR = Path(__file__).parent.parent


def sort_dict(data: dict) -> dict:
    return {k: data[k] for k in sorted(data)}


def load_sql(path: Path):
    queries = None
    for file in path.iterdir():
        if file.is_file() and file.name.endswith(".sql"):
            query = anosql.from_path(str(file), "psycopg2")
            if queries:
                for qname in query.available_queries:
                    queries.add_query(qname, getattr(query, qname))
            else:
                queries = query
    return queries


def build_dict(id: int, label: str, alert_time: datetime, active: bool):
    return {
        "id": id,
        "text": label,
        "alert_time": str(alert_time),
        "active_img": "images/active.png" if active else "images/inactive.png",
        "state": "[color=#f74728]Passed[/color]"
        if datetime.datetime.now().time() > alert_time
        else "Pending",
    }


def load_fonts():
    font_path = ROOT_DIR / "static" / "fonts" / "Roboto"
    LabelBase.register(
        name="Roboto",
        fn_regular=str(font_path / "Roboto-Thin.ttf"),
        fn_bold=str(font_path / "Roboto-Medium.ttf"),
    )


def seconds_until_midnight():
    now = datetime.datetime.now()
    tomorrow = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
    return abs(tomorrow - now).seconds

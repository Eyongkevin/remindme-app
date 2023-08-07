from typing import Optional
import environ
import psycopg as pg

from src.utils import ROOT_DIR
from src.db.schema import InsertDataType

env = environ.Env()
environ.Env.read_env(str(ROOT_DIR / ".env"))


class Database:
    _instance = None

    def __new__(cls):
        if Database._instance is None:
            Database._instance = super().__new__(cls)
            Database._instance.__init__()
        return Database._instance._conn

    def __init__(self) -> None:
        self._conn = pg.connect(
            host=env.str("db_host"),
            dbname=env.str("db_name"),
            user=env.str("db_user"),
            password=env.str("db_password"),
            port=env.int("db_port"),
        )


def get_all():
    conn = Database()
    query = """
        SELECT 
            id,
            label,
            days,
            alert_time,
            type,
            active
        FROM remindmeapp;
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        reminders = cursor.fetchall()
        return reminders


def get_active_reminder():
    conn = Database()
    query = """
      SELECT 
         id,
         days,
         alert_time,
         type
      FROM remindmeapp
      WHERE active = %s;
   """
    with conn.cursor() as cursor:
        cursor.execute(
            query,
            ["1"],
        )
        reminders = cursor.fetchall()
        return reminders


def insert_data(data: InsertDataType) -> Optional[int]:
    conn = Database()
    query = """
      INSERT INTO remindmeapp(
         label,
         alert_time,
         days,
         type,
         active
      ) VALUES (%s,%s,%s,%s,%s) RETURNING id;
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
        inserted_id = cursor.fetchone()[0]
        conn.commit()
        return inserted_id

import sqlite3

from .create_database import create_database
from .hour import insert_into_hour
from .day import insert_into_day
from .vessel import insert_into_vessel


class Entry:

    def __init__(self, db_name=":memory:"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)

    def init_database(self):
        return create_database(self.conn)

    def insert_vessel_info(self, **kwargs):
        return insert_into_vessel(self.conn, kwargs)

    def insert_daily_entry(self, **kwargs):
        return insert_into_day(self.conn, kwargs)

    def insert_hourly_entry(self, **kwargs):
        return insert_into_hour(self.conn, kwargs)

import sqlite3

from .create_database import create_database
from .day import (check_if_daily_entry_exists, insert_into_day,
                  update_total_distance_this_day, select_all_from_day_with_id)
from .hour import insert_into_hour, select_all_from_hour_with_id
from .vessel import insert_into_vessel, select_all_from_vessel_with_id
from .general import select_count_from_table


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

    def update_total_distance_daily_entry(self, current_date):
        return update_total_distance_this_day(self.conn, current_date)

    def insert_hourly_entry(self, **kwargs):
        return insert_into_hour(self.conn, kwargs)

    def daily_entry_exists(self, current_date, vessel_name):
        return check_if_daily_entry_exists(
            self.conn, current_date, vessel_name)

    def get_vessel_info(self, id):
        return select_all_from_vessel_with_id(self.conn, id)

    def get_day_info(self, id):
        return select_all_from_day_with_id(self.conn, id)

    def get_hour_info(self, id):
        return select_all_from_hour_with_id(self.conn, id)

    def get_count_from_table(self, table_name):
        return select_count_from_table(self.conn, table_name)

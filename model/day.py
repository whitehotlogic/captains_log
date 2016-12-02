from config.config import CONFIG
from datetime import date

from geopy.distance import vincenty


def select_all_from_day_with_id(conn, id):
    with conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT vessel_id, date, port_of_call_start, port_of_call_end,
                total_distance_this_day, high_tide, low_tide, skipper
                FROM day
                    WHERE id = ?
        """, [id])
        vessel_data = cur.fetchone()

        return vessel_data


def check_if_daily_entry_exists(conn, current_date, vessel_name):
    with conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id FROM day WHERE date = ?
        """, [str(current_date)])
        daily_entry = cur.fetchone()

        print("DAILY ENTRY EXISTS", daily_entry)

        if daily_entry is None:
            return False
        else:
            return True


def insert_into_day(conn, kwargs):
    if "date" in kwargs:
        current_date = kwargs["date"]
    else:
        current_date = date.today()

    port_of_call_start = kwargs.get("port_of_call_start", None)
    port_of_call_end = kwargs.get("port_of_call_end", None)
    high_tide = kwargs.get("high_tide", None)
    low_tide = kwargs.get("low_tide", None)
    skipper = kwargs.get("skipper", None)

    with conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id FROM vessel WHERE name = ?;
        """, [CONFIG["vessel_name"]])
        vessel_id = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO day VALUES(
                :id, :vessel_id, :date, :port_of_call_start,
                :port_of_call_end, :total_distance_this_day,
                :high_tide, :low_tide, :skipper
            );
        """, {
            "id": None, "vessel_id": vessel_id, "date": str(current_date),
            "port_of_call_start": port_of_call_start,
            "port_of_call_end": port_of_call_end,
            "total_distance_this_day": None,
            "high_tide": high_tide, "low_tide": low_tide,
            "skipper": skipper
        })


def update_total_distance_this_day(conn, current_date):
    with conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id FROM vessel WHERE name = ?;
        """, [CONFIG["vessel_name"]])
        vessel_id = cur.fetchone()[0]
        cur.execute("""
            SELECT hour.latitude, hour.longitude FROM hour
                INNER JOIN day ON
                    day.id = hour.day_id
                WHERE day.date = ?
        """, [current_date])
        coordinates_this_day = cur.fetchall()
        if len(coordinates_this_day) == 0:
            total_distance_this_day = 0
        else:
            total_distance_this_day = vincenty(
                (coordinates_this_day[0][0],
                 coordinates_this_day[0][1]),
                (coordinates_this_day[len(coordinates_this_day) - 1][0],
                 coordinates_this_day[len(coordinates_this_day) - 1][1])
            ).miles * 0.868976  # nm from miles
        cur.execute("""
            UPDATE day SET total_distance_this_day = ?
                WHERE date = ? and vessel_id = ?;
        """, [total_distance_this_day, current_date, vessel_id])

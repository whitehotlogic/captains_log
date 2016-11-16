from datetime import date


def insert_into_day(conn, kwargs):
    vessel = kwargs.get("vessel", None)
    current_date = date.today()
    port_of_call_start = kwargs.get("port_of_call_start", None)
    port_of_call_end = kwargs.get("port_of_call_end", None)
    total_distance_this_day = 1  # TODO: add all from hourly entries
    high_tide = 1  # TODO: get from data source
    low_tide = 1  # TODO: get from data source
    skipper = kwargs.get("skipper", None)

    with conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO data VALUES(
                :vessel, :date, :port_of_call_start,
                :port_of_call_end, :total_distance_this_day,
                :high_tide, :low_tide, :skipper
            )
        """, {
            "vessel": vessel, "date": current_date,
            "port_of_call_start": port_of_call_start,
            "port_of_call_end": port_of_call_end,
            "total_distance_this_day": total_distance_this_day,
            "high_tide": high_tide, "low_tide": low_tide,
            "skipper": skipper
        })

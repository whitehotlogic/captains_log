from datetime import datetime


def insert_into_hour(self, kwargs):
    vessel = kwargs.get("vessel", None)
    day = 1  # TODO: select day id based on vessel and current date
    current_time = datetime.now().time()
    course = kwargs.get("course", None)
    latitude = kwargs.get("latitude", None)
    longitude = kwargs.get("longitude", None)
    weather = kwargs.get("weather", None)
    wind_speed = kwargs.get("wind_speed", None)
    wind_direction = kwargs.get("wind_direction", None)
    engine_hours = kwargs.get("engine_hours", None)
    fuel_level = kwargs.get("fuel_level", None)
    water_level = kwargs.get("water_level", None)
    visibility = kwargs.get("visibility", None)
    distance_since_last_entry = kwargs.get(
        "distance_since_last_entry", None)
    notes = " | ".join(kwargs.get("notes", []))

    with self.conn:
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO data VALUES(
                :vessel, :day, :time,
                :port_of_call_end, :total_distance_this_day,
                :high_tide, :low_tide, :skipper
            )
        """, {
            "vessel": vessel, "day": day, "time": current_time,
            "course": course, "latitude": latitude, "longitude": longitude,
            "weather": weather, "wind_speed": wind_speed,
            "wind_direction": wind_direction, "engine_hours": engine_hours,
            "fuel_level": fuel_level, "water_level": water_level,
            "visibility": visibility, "notes": notes,
            "distance_since_last_entry": distance_since_last_entry
        })

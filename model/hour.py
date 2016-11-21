from config.config import CONFIG
from datetime import date, datetime

from geopy.distance import vincenty


def insert_into_hour(conn, kwargs):
    if "date" in kwargs:
        current_date = kwargs["date"]
    else:
        current_date = date.today()
    if "time" in kwargs:
        current_time = kwargs["time"]
    else:
        current_time = datetime.now().time()
    course = kwargs.get("course", None)
    latitude = kwargs.get("latitude", None)
    longitude = kwargs.get("longitude", None)
    weather = kwargs.get("weather", None)
    wind_speed = kwargs.get("wind_speed", None)
    wind_direction = kwargs.get("wind_direction", None)
    visibility = kwargs.get("visibility", None)
    engine_hours = kwargs.get("engine_hours", None)
    fuel_level = kwargs.get("fuel_level", None)
    water_level = kwargs.get("water_level", None)

    with conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id FROM day WHERE date = ?
                AND vessel_id = (
                    SELECT id FROM vessel WHERE name = ?);
        """, [str(current_date), CONFIG["vessel_name"]])
        day_id = cur.fetchone()[0]
        cur.execute("""
            SELECT latitude, longitude FROM hour
                WHERE day_id = ? AND (SELECT id FROM vessel WHERE name = ?)
                    AND latitude IS NOT NULL AND longitude IS NOT NULL
                        ORDER BY id DESC LIMIT 1;
        """, [day_id, CONFIG["vessel_name"]])
        coordinates_at_last_entry = cur.fetchone()
        if coordinates_at_last_entry is not None:
            distance_since_last_entry = vincenty(
                (coordinates_at_last_entry[0],
                 coordinates_at_last_entry[1]),
                (latitude, longitude)).miles * 0.868976
        else:
            distance_since_last_entry = 0
        speed = int(round(distance_since_last_entry))
        cur.execute("""
            INSERT INTO hour VALUES(
                :id, :day_id, :time, :course, :speed, :latitude,
                :longitude, :weather, :wind_speed, :wind_direction,
                :visibility, :engine_hours, :fuel_level, :water_level,
                :distance_since_last_entry
            );
        """, {
            "id": None, "day_id": day_id,
            "time": str(current_time), "course": course, "latitude": latitude,
            "longitude": longitude, "weather": weather, "speed": speed,
            "wind_speed": wind_speed, "wind_direction": wind_direction,
            "engine_hours": engine_hours, "fuel_level": fuel_level,
            "water_level": water_level, "visibility": visibility,
            "distance_since_last_entry": distance_since_last_entry
        })

def create_database(conn, test=False):
    with conn:
        cur = conn.cursor()
        if test is True:
            cur.execute("""
                PRAGMA synchronous = 0
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vessel (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                hull_number INTEGER NOT NULL UNIQUE,
                uscg_number INTEGER UNIQUE,
                fuel_capacity INTEGER NOT NULL,
                water_capacity INTEGER NOT NULL,
                battery_capacity INTEGER NOT NULL,
                engine_manufacturer TEXT,
                engine_number INTEGER,
                engine_type TEXT,
                owner_name TEXT NOT NULL,
                owner_certification_agency TEXT,
                owner_certification_number TEXT
            );
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS vessel_name ON vessel (name);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS vessel_hull_number
                ON vessel (hull_number);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS vessel_uscg_number
                ON vessel (uscg_number);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS vessel_owner_name
                ON vessel (owner_name);
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS day (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vessel_id int NOT NULL REFERENCES vessel,
                date TEXT NOT NULL,
                port_of_call_start TEXT,
                port_of_call_end TEXT,
                total_distance_this_day INTEGER,
                high_tide NUMERIC,
                low_tide NUMERIC,
                skipper TEXT
            );
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS day_vessel_id ON day (vessel_id);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS day_date
                ON day (date);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS day_port_of_call
                ON day (port_of_call_start, port_of_call_end);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS day_total_distance_this_day
                ON day (total_distance_this_day);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS day_skipper
                ON day (skipper);
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hour (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                day_id int NOT NULL REFERENCES day,
                time INTEGER NOT NULL,
                course INTEGER,
                speed INTEGER,
                latitude NUMERIC,
                longitude INTEGER,
                weather TEXT,
                wind_speed INTEGER,
                wind_direction INTEGER,
                visibility INTEGER,
                engine_hours INTEGER,
                fuel_level NUMERIC,
                water_level NUMERIC,
                distance_since_last_entry NUMERIC
            );
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_day_id_asc ON hour (day_id ASC);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_day_id_desc ON hour (day_id DESC);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_day_id_time ON hour (day_id, time);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_position
                ON hour (latitude, longitude);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_weather ON hour (weather);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_wind
                ON hour (wind_speed, wind_direction);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_engine_hours
                ON hour (engine_hours);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_fuel_level
                ON hour (fuel_level);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_water_level
                ON hour (water_level);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_visibility
                ON hour (visibility);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_distance_since_last_entry
                ON hour (distance_since_last_entry);
        """)
        cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS notes USING fts4 (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                note TEXT
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hour_notes (
                notes_id INTEGER UNIQUE NOT NULL,
                hour_id INTEGER NOT NULL
            );
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_notes_notes_id_asc
                ON hour_notes (notes_id ASC);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_notes_notes_id_desc
                ON hour_notes (notes_id DESC);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_notes_hour_id_asc
                ON hour_notes (hour_id ASC);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_notes_hour_id_desc
                ON hour_notes (hour_id DESC);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_notes_hour_id_notes_id
                ON hour_notes (hour_id, notes_id);
        """)

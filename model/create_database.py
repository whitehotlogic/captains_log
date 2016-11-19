def create_database(conn):
    with conn:
        cur = conn.cursor()
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
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                vessel int NOT NULL REFERENCES vessel,
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
            CREATE INDEX IF NOT EXISTS day_vessel ON day (vessel);
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
                vessel int NOT NULL REFERENCES vessel,
                day TEXT NOT NULL REFERENCES day,
                time TEXT NOT NULL,
                course INTEGER,
                latitude NUMERIC,
                longitude INTEGER,
                weather TEXT,
                wind_speed INTEGER,
                wind_direction TEXT,
                engine_hours INTEGER,
                fuel_level INTEGER,
                water_level INTEGER,
                visibility INTEGER,
                distance_since_last_entry NUMERIC,
                notes INTEGER
            );
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_vessel ON hour (vessel);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_day_asc ON hour (day ASC);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_day_desc ON hour (day DESC);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS hour_datetime ON hour (day, time);
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

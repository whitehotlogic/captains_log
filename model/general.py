def select_count_from_vessel(conn):
    with conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(0) FROM vessel;
        """)
        count = cur.fetchone()

        if not count:
            return 0
        return count[0]


def select_count_from_day(conn):
    with conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(0) FROM day;
        """)
        count = cur.fetchone()

        if not count:
            return 0
        return count[0]


def select_count_from_hour(conn):
    with conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(0) FROM hour;
        """)
        count = cur.fetchone()

        if not count:
            return 0
        return count[0]


def select_count_from_table(conn, table_name):
    TABLES = {
        "vessel": select_count_from_vessel,
        "day": select_count_from_day,
        "hour": select_count_from_hour
    }

    return TABLES[table_name](conn)

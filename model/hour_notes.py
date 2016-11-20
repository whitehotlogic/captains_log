def insert_into_hour_notes(conn, hour_id, notes_id):

    with conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO hour_notes VALUES(
                :hour_id, :notes_id
            )
        """, {"hour_id": hour_id, "notes_id": notes_id})

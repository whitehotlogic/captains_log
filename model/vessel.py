def insert_into_vessel(conn, kwargs):
    name = kwargs.get("name", None)
    hull_number = kwargs.get("hull_number", None)
    uscg_number = kwargs.get("uscg_number", None)
    fuel_capacity = kwargs.get("fuel_capacity", None)
    water_capacity = kwargs.get("water_capacity", None)
    battery_capacity = kwargs.get("battery_capacity", None)
    engine_manufacturer = kwargs.get("engine_manufacturer", None)
    engine_number = kwargs.get("engine_number", None)
    engine_type = kwargs.get("engine_type", None)
    owner_name = kwargs.get("owner_name", None)
    owner_certification_agency = kwargs.get(
        "owner_certification_agency", None)
    owner_certification_number = kwargs.get(
        "owner_certification_number", None)

    with conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO vessel VALUES(
                :id, :name, :hull_number, :uscg_number,
                :fuel_capacity, :water_capacity,
                :battery_capacity, :engine_manufacturer, :engine_number,
                :engine_type, :owner_name, :owner_certification_agency,
                :owner_certification_number
            )
        """, {
            "id": None, "name": name, "hull_number": hull_number,
            "uscg_number": uscg_number, "fuel_capacity": fuel_capacity,
            "water_capacity": water_capacity,
            "battery_capacity": battery_capacity,
            "engine_manufacturer": engine_manufacturer,
            "engine_type": engine_type, "engine_number": engine_number,
            "owner_name": owner_name,
            "owner_certification_agency": owner_certification_agency,
            "owner_certification_number": owner_certification_number
        })

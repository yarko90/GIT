
def create_tables(conn):
    cur = conn.cursor()

    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS Detectors
                  (
                    GUID CHARACTER VARYING (36) NOT NULL PRIMARY KEY,
                    detector_name CHARACTER VARYING (200),
                    Hour_1 REAL, Hour_2 REAL, Hour_3 REAL, Hour_4 REAL, Hour_5 REAL, Hour_6 REAL,
                    Hour_7 REAL, Hour_8 REAL, Hour_9 REAL, Hour_10 REAL, Hour_11 REAL, Hour_12 REAL,
                    Hour_13 REAL, Hour_14 REAL, Hour_15 REAL, Hour_16 REAL, Hour_17 REAL, Hour_18 REAL,
                    Hour_19 REAL, Hour_20 REAL, Hour_21 REAL, Hour_22 REAL, Hour_23 REAL, Hour_24 REAL
                    ) """)
    except:
        print('Rise error, Detector_table creation error')
    conn.commit()

    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS Rooms
                  (
                    GUID CHARACTER VARYING (36) NOT NULL PRIMARY KEY,
                    room_name CHARACTER VARYING (200),
                    detector CHARACTER VARYING (200)
                    ) ''')
    except:
        print('Rise error, Room_table creation error')
    conn.commit()

    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS Offices
                  (
                    GUID CHARACTER VARYING (36) NOT NULL PRIMARY KEY,
                    office_name CHARACTER VARYING (200),
                    room CHARACTER VARYING (200)
                    ) ''')
    except:
        print('Rise error, Office_table creation error')
    conn.commit()

    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS Floors
                  (
                    GUID CHARACTER VARYING (36) NOT NULL PRIMARY KEY,
                    floor_name CHARACTER VARYING (200),
                    office CHARACTER VARYING (200)
                    ) ''')
    except:
        print('Rise error, Floor_table creation error')
    conn.commit()

    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS Buildings
                  (
                    GUID CHARACTER VARYING (36) NOT NULL PRIMARY KEY,
                    Building_name CHARACTER VARYING (200),
                    floor CHARACTER VARYING (200)
                    ) ''')
    except:
        print('Rise error, Floor_table creation error')

    conn.commit()
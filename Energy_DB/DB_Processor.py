import uuid

#Add item to table
class Adder():
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def make_guid(self, name):
        return str(uuid.uuid4())

    def add_building(self, building_name, floor='Null'):
        print('add_building')
        #guid = "a"
        #building_name = "b"
        #floor = "c"
        try:
            self.building_GUID = self.make_guid(building_name)
            print(self.building_GUID)
            self.cur.execute("""INSERT INTO public.buildings
                                  ("guid","building_name","floor") VALUES (%s,%s,%s)""",(self.building_GUID, building_name, floor))
            self.conn.commit()
            self.flag = True
            print('Building_added')
        except:
            print('Building add fail')
            self.flag = False
        self.conn.commit()
        return self.flag

    def add_floor(self, building_name, floor_name, office='Null'):
        print('add_floor')
        try:
            self.floor_GUID = self.make_guid(floor_name)
            self.flag = self.add_building(building_name, self.floor_GUID)

            if self.flag is True:
                self.cur.execute("""INSERT INTO public.floors
                                ("guid","floor_name","office") VALUES (%s,%s,%s)""", (self.floor_GUID, floor_name, office))
                self.conn.commit()
                print('Floor_added')
        except:
            print('Floor add fail')
            self.flag = False
        self.conn.commit()
        return self.flag

    def add_office(self, building_name, floor_name, office_name, room='Null'):
        print('add_office')
        try:
            self.office_GUID = self.make_guid(office_name)
            self.flag = self.add_floor(building_name, floor_name, self.office_GUID)

            if self.flag is True:
                self.cur.execute("""INSERT INTO public.offices
                                ("guid","office_name","room") VALUES (%s,%s,%s)""", (self.office_GUID, office_name, room))
                self.conn.commit()
                print('Office_added')
        except:
            print('Office add fail')
        self.conn.commit()
        return self.flag

    def add_room(self, building_name, floor_name, office_name, room_name, detector='Null'):
        print('add_room')
        try:
            self.room_GUID = self.make_guid(room_name)
            self.flag = self.add_office(building_name, floor_name, office_name, self.room_GUID)

            if self.flag is True:
                self.cur.execute("""INSERT INTO public.rooms
                                ("guid","room_name","detector") VALUES (%s,%s,%s)""",(self.room_GUID, room_name, detector))
                self.conn.commit()
                print('Room_added')
        except:
            print('Room add fail')
        self.conn.commit()
        return self.flag

    def add_detector(self, building_name, floor_name, office_name, room_name, detector_name):
        print('add_detector')
        try:
            self.detector_GUID = self.make_guid(detector_name)
            self.flag = self.add_room(building_name, floor_name, office_name, room_name, self.detector_GUID)

            if self.flag is True:
                self.cur.execute("""INSERT INTO public.detectors
                                ("guid","detector_name") VALUES (%s,%s)""", (self.detector_GUID, detector_name ))
                self.conn.commit()
                print('Detector_added')
        except:
            print('Detector add fail')
        self.conn.commit()


#Update temperature value
class Updater():
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def update (self, detector_name, value,  time):
        detector_name = detector_name.split('|')
        time_column = 'Hour_7'+str(time)
        try:
            self.cur.execute('''UPDATE public.detectors SET "total_games"=%s WHERE "detector_name"=%s""",(p1.total_games,))''')
            self.conn.commit()
        except:
            print('Rise update error')
            self.conn.commit()




#Get detecrtor from table
class Getter():
    def __init__(self, conn):
        self.cur = conn.cursor()

    def get_building(self, building_name):
        pass

    def get_floor(self, building_name, floor_name):
        pass

    def get_office(self, building_name, floor_name, office_name):
        pass

    def get_room(self, building_name, floor_name, office_name, room_name):
        pass

    def get_detector(self, building_name, floor_name, office_name, room_name, detector_name):

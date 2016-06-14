import uuid
import Detector
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
        except Exception as e:
            print('Building add fail', e)
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
        except Exception as e:
            print('Floor add fail', e)
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
        except Exception as e:
            print('Office add fail', e)
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
        except Exception as e:
            print('Room add fail', e)
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
        except Exception as e:
            print('Detector add fail', e)
        self.conn.commit()


#Update temperature value
class Updater():
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def update (self, detector_name, value,  time):
        detector_name = detector_name.split('|')[-1]
        time_column = 'hour_'+str(time+1)
        print(detector_name, time_column)
        try:
            execute_string = 'UPDATE public.detectors SET {}={} WHERE detector_name = \'{}\';'.format(time_column, value, detector_name)
            print(execute_string)
            self.cur.execute(execute_string)
            self.conn.commit()
        except Exception as e:
            print('Rise update error', e)
            self.conn.commit()


#Get detecrtor from table
class Getter():
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def make_answer(self, execute_string):
        #print(execute_string)
        try:
            self.cur.execute(execute_string)
            detector_data = self.cur.fetchall()
            self.conn.commit()
            detector = Detector.Detector(detector_data[0][0], detector_data[0][-24:])
            return detector
        except Exception as e:
            print('Rise update error', e)
            self.conn.commit()

    def get_building(self, building_name):
        execute_string = """SELECT building_name, floor_name, office_name,room_name, detector_name,
                                    hour_1, hour_2, hour_3, hour_4, hour_5, hour_6, hour_7, hour_8,
                                    hour_9, hour_10, hour_11, hour_12, hour_13, hour_14, hour_15, hour_16,
                                    hour_17, hour_18, hour_19, hour_20, hour_21, hour_22, hour_23, hour_24
                              FROM public.detectors AS detectors
                              JOIN public.rooms AS rooms ON rooms.detector=detectors.guid
                              JOIN public.offices AS offices ON offices.room=rooms.guid
                              JOIN public.floors AS floors ON floors.office=offices.guid
                              JOIN public.buildings AS buildings ON buildings.floor=floors.guid
                              WHERE buildings.building_name = '{}'""".format(building_name)
        self.make_answer(execute_string)

    def get_floor(self, building_name, floor_name):
        execute_string = """SELECT building_name, floor_name, office_name,room_name, detector_name,
                                    hour_1, hour_2, hour_3, hour_4, hour_5, hour_6, hour_7, hour_8,
                                    hour_9, hour_10, hour_11, hour_12, hour_13, hour_14, hour_15, hour_16,
                                    hour_17, hour_18, hour_19, hour_20, hour_21, hour_22, hour_23, hour_24
                              FROM public.detectors AS detectors
                              JOIN public.rooms AS rooms ON rooms.detector=detectors.guid
                              JOIN public.offices AS offices ON offices.room=rooms.guid
                              JOIN public.floors AS floors ON floors.office=offices.guid
                              JOIN public.buildings AS buildings ON buildings.floor=floors.guid
                              WHERE buildings.building_name = '{}'
                                    AND
                                    floors.floor_name = '{}'""".format(building_name, floor_name)
        self.make_answer(execute_string)

    def get_office(self, building_name, floor_name, office_name):
        execute_string = """SELECT building_name, floor_name, office_name,room_name, detector_name,
                                    hour_1, hour_2, hour_3, hour_4, hour_5, hour_6, hour_7, hour_8,
                                    hour_9, hour_10, hour_11, hour_12, hour_13, hour_14, hour_15, hour_16,
                                    hour_17, hour_18, hour_19, hour_20, hour_21, hour_22, hour_23, hour_24
                              FROM public.detectors AS detectors
                              JOIN public.rooms AS rooms ON rooms.detector=detectors.guid
                              JOIN public.offices AS offices ON offices.room=rooms.guid
                              JOIN public.floors AS floors ON floors.office=offices.guid
                              JOIN public.buildings AS buildings ON buildings.floor=floors.guid
                              WHERE buildings.building_name = '{}'
                                    AND
                                    floors.floor_name = '{}'
                                    AND
                                    offices.office_name = '{}'""".format(building_name, floor_name, office_name)
        self.make_answer(execute_string)

    def get_room(self, building_name, floor_name, office_name, room_name):
        execute_string = """SELECT building_name, floor_name, office_name,room_name, detector_name,
                                           hour_1, hour_2, hour_3, hour_4, hour_5, hour_6, hour_7, hour_8,
                                           hour_9, hour_10, hour_11, hour_12, hour_13, hour_14, hour_15, hour_16,
                                           hour_17, hour_18, hour_19, hour_20, hour_21, hour_22, hour_23, hour_24
                                     FROM public.detectors AS detectors
                                     JOIN public.rooms AS rooms ON rooms.detector=detectors.guid
                                     JOIN public.offices AS offices ON offices.room=rooms.guid
                                     JOIN public.floors AS floors ON floors.office=offices.guid
                                     JOIN public.buildings AS buildings ON buildings.floor=floors.guid
                                     WHERE buildings.building_name = '{}'
                                           AND
                                           floors.floor_name = '{}'
                                           AND
                                           offices.office_name = '{}'
                                           AND
                                           rooms.room_name = '{}'""".format(building_name, floor_name, office_name, room_name)
        self.make_answer(execute_string)

    def get_detector(self, building_name, floor_name, office_name, room_name, detector_name):
        execute_string = """SELECT building_name, floor_name, office_name,room_name, detector_name,
                                           hour_1, hour_2, hour_3, hour_4, hour_5, hour_6, hour_7, hour_8,
                                           hour_9, hour_10, hour_11, hour_12, hour_13, hour_14, hour_15, hour_16,
                                           hour_17, hour_18, hour_19, hour_20, hour_21, hour_22, hour_23, hour_24
                                     FROM public.detectors AS detectors
                                     JOIN public.rooms AS rooms ON rooms.detector=detectors.guid
                                     JOIN public.offices AS offices ON offices.room=rooms.guid
                                     JOIN public.floors AS floors ON floors.office=offices.guid
                                     JOIN public.buildings AS buildings ON buildings.floor=floors.guid
                                     WHERE buildings.building_name = '{}'
                                           AND
                                           floors.floor_name = '{}'
                                           AND
                                           offices.office_name = '{}'
                                           AND
                                           rooms.room_name = '{}'
                                           AND
                                           detectors.detector_name = '{}'""".format(building_name, floor_name, office_name, room_name, detector_name)
        self.make_answer(execute_string)
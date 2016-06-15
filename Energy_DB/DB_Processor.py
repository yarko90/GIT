import uuid
import Detector

#Add object(building/floor/office/room/detector) to table
class Adder():
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def make_guid(self, name):
        return str(uuid.uuid4())

    def make_link(self):
        return str(uuid.uuid4())

    def add_building(self, building_name, floor='Null'):
        print('add_building')
        #guid = "a"
        #building_name = "b"
        #floor = "c"
        try:
            self.building_GUID = self.make_guid(building_name)
            self.floor_link = self.make_link()
            #print(self.building_GUID)
            self.cur.execute("""INSERT INTO public.buildings
                                  ("guid","building_name","floor") VALUES (%s,%s,%s)""",(self.building_GUID, building_name, self.floor_link))
            self.conn.commit()
            self.flag = True
            print('Building_added')
        except Exception as e:
            print('Building add fail', e)
            self.flag = False
        self.conn.commit()
        return self.flag, [self.floor_link]*2

    def add_floor(self, building_name, floor_name, office='Null'):
        print('add_floor')
        try:
            self.flag, links = self.add_building(building_name)

            if self.flag is True:
                self.office_links = []
                for link in links:
                    self.floor_GUID = self.make_guid(floor_name)
                    office = self.make_link()
                    self.cur.execute("""INSERT INTO public.floors
                                    ("guid","link","floor_name","office") VALUES (%s,%s,%s,%s)""", (self.floor_GUID, link, floor_name, office))
                    self.conn.commit()
                    self.office_links.append(office)
                    print('Floor_added')
        except Exception as e:
            print('Floor add fail', e)
            self.flag = False
        self.conn.commit()
        return self.flag, self.office_links*2

    def add_office(self, building_name, floor_name, office_name, room='Null'):
        print('add_office')
        try:
            self.flag, links = self.add_floor(building_name, floor_name)

            if self.flag is True:
                self.room_links = []
                for link in links:
                    self.office_GUID = self.make_guid(office_name)
                    room = self.make_link()
                    self.cur.execute("""INSERT INTO public.offices
                                    ("guid","link","office_name","room") VALUES (%s,%s,%s,%s)""", (self.office_GUID, link, office_name, room))
                    self.conn.commit()
                    self.room_links.append(room)
                    print('Office_added')
        except Exception as e:
            print('Office add fail', e)
        self.conn.commit()
        return self.flag, self.room_links*2

    def add_room(self, building_name, floor_name, office_name, room_name, detector='Null'):
        print('add_room')
        try:
            self.flag, links = self.add_office(building_name, floor_name, office_name)

            if self.flag is True:
                self.detector_links = []
                for link in links:
                    self.room_GUID = self.make_guid(room_name)
                    detector = self.make_link()
                    self.cur.execute("""INSERT INTO public.rooms
                                    ("guid","link","room_name","detector") VALUES (%s,%s,%s,%s)""",(self.room_GUID, link, room_name, detector))
                    self.conn.commit()
                    self.detector_links.append(detector)
                    print('Room_added')
        except Exception as e:
            print('Room add fail', e)
        self.conn.commit()
        return self.flag, self.detector_links*2

    def add_detector(self, building_name, floor_name, office_name, room_name, detector_name):
        print('add_detector')
        try:
            self.flag, links = self.add_room(building_name, floor_name, office_name, room_name)

            if self.flag is True:
                #detector_list = []
                for link in links:
                    self.detector_GUID = self.make_guid(detector_name)
                    self.cur.execute("""INSERT INTO public.detectors
                                    ("guid","link","detector_name") VALUES (%s,%s,%s)""", (self.detector_GUID, link, detector_name ))
                    self.conn.commit()
                    #detector_list.append(self.detector_GUID)
                    print('Detector_added')
                #return detector_list
        except Exception as e:
            print('Detector add fail', e)
        self.conn.commit()


#Update temperature value
class Updater():
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def update (self, detector_guid, value, time):
        #detector_guid = detector_guid.split('|')[-1]
        time_column = 'hour_'+str(time+1)
        #print(detector_guid, time_column)
        try:
            execute_string = 'UPDATE public.detectors SET {}={} WHERE guid = \'{}\';'.format(time_column, value, detector_guid)
            #print(execute_string)
            self.cur.execute(execute_string)
            self.conn.commit()
        except Exception as e:
            print('Rise update error', e)
            self.conn.commit()


#Get oject(building/floor/office/room/detector) temperature logg from table
class Getter():
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    #makes object model on data from DB
    def make_answer(self, execute_string, name):
        #print(execute_string)
        try:
            self.cur.execute(execute_string)
            detector_data = self.cur.fetchall()
            self.conn.commit()
            time = 1
            hour_dict = {}
            while time<=24:
                hour_dict[time] = []
                time += 1
            time = 1

            #fill hour_dict of an object with data from DB
            for detector in detector_data:
                measurments = detector[-24:]
                while time<=24:
                    if measurments[time-1] is not None:
                        hour_dict[time].append(measurments[time-1])
                    time += 1

            #make avarage hour temperature of an object
            for time_stamp in hour_dict.keys():
                if len(hour_dict[time_stamp])>0:
                    hour_dict[time_stamp] = round(sum(hour_dict[time_stamp])/len(hour_dict[time_stamp]),3)
            object = Detector.Detector(name, hour_dict)
            return object

        except Exception as e:
            print('Rise update error', e)
            self.conn.commit()

    def get_building(self, building_name):
        execute_string = """SELECT building_name, floor_name, office_name,room_name, detector_name,
                                    hour_1, hour_2, hour_3, hour_4, hour_5, hour_6, hour_7, hour_8,
                                    hour_9, hour_10, hour_11, hour_12, hour_13, hour_14, hour_15, hour_16,
                                    hour_17, hour_18, hour_19, hour_20, hour_21, hour_22, hour_23, hour_24
                              FROM public.detectors AS detectors
                              JOIN public.rooms AS rooms ON rooms.detector=detectors.link
                              JOIN public.offices AS offices ON offices.room=rooms.link
                              JOIN public.floors AS floors ON floors.office=offices.link
                              JOIN public.buildings AS buildings ON buildings.floor=floors.link
                              WHERE buildings.building_name = '{}'""".format(building_name)
        return(self.make_answer(execute_string, building_name))

    def get_floor(self, building_name, floor_name):
        execute_string = """SELECT building_name, floor_name, office_name,room_name, detector_name,
                                    hour_1, hour_2, hour_3, hour_4, hour_5, hour_6, hour_7, hour_8,
                                    hour_9, hour_10, hour_11, hour_12, hour_13, hour_14, hour_15, hour_16,
                                    hour_17, hour_18, hour_19, hour_20, hour_21, hour_22, hour_23, hour_24
                              FROM public.detectors AS detectors
                              JOIN public.rooms AS rooms ON rooms.detector=detectors.link
                              JOIN public.offices AS offices ON offices.room=rooms.link
                              JOIN public.floors AS floors ON floors.office=offices.link
                              JOIN public.buildings AS buildings ON buildings.floor=floors.link
                              WHERE buildings.building_name = '{}'
                                    AND
                                    floors.floor_name = '{}'""".format(building_name, floor_name)
        self.make_answer(execute_string, floor_name)

    def get_office(self, building_name, floor_name, office_name):
        execute_string = """SELECT building_name, floor_name, office_name,room_name, detector_name,
                                    hour_1, hour_2, hour_3, hour_4, hour_5, hour_6, hour_7, hour_8,
                                    hour_9, hour_10, hour_11, hour_12, hour_13, hour_14, hour_15, hour_16,
                                    hour_17, hour_18, hour_19, hour_20, hour_21, hour_22, hour_23, hour_24
                              FROM public.detectors AS detectors
                              JOIN public.rooms AS rooms ON rooms.detector=detectors.link
                              JOIN public.offices AS offices ON offices.room=rooms.link
                              JOIN public.floors AS floors ON floors.office=offices.link
                              JOIN public.buildings AS buildings ON buildings.floor=floors.link
                              WHERE buildings.building_name = '{}'
                                    AND
                                    floors.floor_name = '{}'
                                    AND
                                    offices.office_name = '{}'""".format(building_name, floor_name, office_name)
        self.make_answer(execute_string, office_name)

    def get_room(self, building_name, floor_name, office_name, room_name):
        execute_string = """SELECT building_name, floor_name, office_name,room_name, detector_name,
                                           hour_1, hour_2, hour_3, hour_4, hour_5, hour_6, hour_7, hour_8,
                                           hour_9, hour_10, hour_11, hour_12, hour_13, hour_14, hour_15, hour_16,
                                           hour_17, hour_18, hour_19, hour_20, hour_21, hour_22, hour_23, hour_24
                                     FROM public.detectors AS detectors
                                     JOIN public.rooms AS rooms ON rooms.detector=detectors.link
                                     JOIN public.offices AS offices ON offices.room=rooms.link
                                     JOIN public.floors AS floors ON floors.office=offices.link
                                     JOIN public.buildings AS buildings ON buildings.floor=floors.link
                                     WHERE buildings.building_name = '{}'
                                           AND
                                           floors.floor_name = '{}'
                                           AND
                                           offices.office_name = '{}'
                                           AND
                                           rooms.room_name = '{}'""".format(building_name, floor_name, office_name, room_name)
        self.make_answer(execute_string, room_name)

    def get_detector(self, building_name, floor_name, office_name, room_name, detector_name):
        execute_string = """SELECT building_name, floor_name, office_name,room_name, detector_name,
                                           hour_1, hour_2, hour_3, hour_4, hour_5, hour_6, hour_7, hour_8,
                                           hour_9, hour_10, hour_11, hour_12, hour_13, hour_14, hour_15, hour_16,
                                           hour_17, hour_18, hour_19, hour_20, hour_21, hour_22, hour_23, hour_24
                                     FROM public.detectors AS detectors
                                     JOIN public.rooms AS rooms ON rooms.detector=detectors.link
                                     JOIN public.offices AS offices ON offices.room=rooms.link
                                     JOIN public.floors AS floors ON floors.office=offices.link
                                     JOIN public.buildings AS buildings ON buildings.floor=floors.link
                                     WHERE buildings.building_name = '{}'
                                           AND
                                           floors.floor_name = '{}'
                                           AND
                                           offices.office_name = '{}'
                                           AND
                                           rooms.room_name = '{}'
                                           AND
                                           detectors.detector_name = '{}'""".format(building_name, floor_name, office_name, room_name, detector_name)
        self.make_answer(execute_string, detector_name)


import psycopg2
import Detector
import Create_tables
from DB_Processor import Adder, Getter, Updater
from Tester import Tester
from datetime import datetime

#make tables, fill with test info
def main_preparation(conn):
    Create_tables.create_tables(conn)
    Add = Adder(conn)
    number_of_buildings = 5
    Test = Tester(conn, number_of_buildings)
    test_sets_list = Test.test_sets_list

    for t_set in test_sets_list:
        t_set_DB = t_set.split("|")
        Add.add_detector(t_set_DB[0], t_set_DB[1], t_set_DB[2], t_set_DB[3], t_set_DB[4])
    Test.all_dectors_dict = Test.get_all_detectors()
    test_detector_dict = Test.all_dectors_dict
    return test_detector_dict, Test


#main cycle generates random temperature measurment on random detector. Every 10 seconds writes averaged measurments to DB#
def main_cycle(test_detector_dict, Test, conn):
    t = True
    flag = True

    #Updates detector value every hour(10 seconds)
    Update = Updater(conn)

    #Get object temperature logg
    Get = Getter(conn)
    while t is True:
        Test.add_measurment()

        #write detectors to DB if time is ok
        if datetime.now().second%10 == 0 and flag is True:
            time = int(datetime.now().second/10)
            print(time)

            for detector_name in test_detector_dict.keys():
                if len(test_detector_dict[detector_name]) > 0:
                    value = round(sum(test_detector_dict[detector_name])/len(test_detector_dict[detector_name]),3)
                else:
                    value = 0.0 #no measurments were made
                Update.update(detector_name, value, time)
            flag = False

            #Get needed data from DB, building for exapmle
            for detector_name in Test.test_sets_list:
                building = Get.get_building(detector_name.split('|')[0])
                print('{}\n{}'.format(building.name, building.hour_dict))

        elif datetime.now().second%10 != 0:
            flag = True



if __name__ == "__main__":
    try:
        conn = psycopg2.connect("dbname='IQnergy' user='postgres' host='localhost' password='123'")
        #make tables, fill with test info
        test_detector_dict, Test = main_preparation(conn)
        #generates random temperature measurment on random detector. Every 10 seconds writes averaged measurments to DB
        main_cycle(test_detector_dict, Test, conn)
    except Exception as e:
        print('Rise DB_Error', e)
    cur = conn.cursor()




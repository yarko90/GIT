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
    number_of_detectors = 5
    Test = Tester(number_of_detectors)
    test_sets_list = Test.test_sets_list
    test_detector_dict = {}
    #print(test_sets_list)
    for t_set in test_sets_list:
        t_set_DB = t_set.split("|")
        #print(t_set_DB)
        Add.add_detector(t_set_DB[0], t_set_DB[1], t_set_DB[2], t_set_DB[3], t_set_DB[4])
        test_detector_dict[t_set] = []
        #print(name)
    return test_detector_dict, Test


#get (detector name,value) pair, append it to dictionary of detectors
def get_detector_value(test_detector_dict, Test):
    sample = Test.test_detector_value(len(test_detector_dict.keys()))
    #print(len(test_detector_dict.keys()))
    detector_name = sample[0]
    value = sample[1]
    if detector_name in test_detector_dict:
        test_detector_dict[detector_name].append(value)
    else:
        test_detector_dict[detector_name] = [value, ]

#main cycle
def main_cycle(test_detector_dict, Test, conn):
    print(test_detector_dict)
    T = True
    Update = Updater(conn)
    while T is True:
        get_detector_value(test_detector_dict, Test)

        #write detectors to DB if time is ok
        if datetime.now().second%10 == 0:
            time = int(datetime.now().second)%10
            print(time)
            for detector in test_detector_dict.keys():
                Update.update(detector,test_detector_dict[detector],time)


if __name__ == "__main__":
    #try:
    conn = psycopg2.connect("dbname='IQnergy' user='postgres' host='localhost' password='123'")
    #make tables, fill with test info
    test_detector_dict, Test = main_preparation(conn)
    main_cycle(test_detector_dict, Test, conn)
    #except:
    #    print('Rise DB_Error')
    #cur = conn.cursor()




import random


class Tester():

    struct = ['building', 'floor', 'office', 'room', 'detector']

    def __init__(self, conn, n):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.test_sets_list = self.test_sets_maker(n)
        self.all_dectors_dict = self.get_all_detectors()

#returns dictionary of all detectors from public.detectors table
    def get_all_detectors(self):
        self.cur.execute("""SELECT guid FROM public.detectors""")
        all_detectors = self.cur.fetchall()
        detectors_dict = {}
        for detector in all_detectors:
            detectors_dict[detector[0]] = []
        self.conn.commit()
        return detectors_dict

#returns n examples of detectors full name
    def test_sets_maker(self,n):
        i = 0
        test_sets_list = []
        while i<n:
            test_set = []
            for element in self.struct:
                test_set.append(element+str(i))
            test_sets_list.append('|'.join(test_set))
            i += 1
        return test_sets_list


#adds measurment to detector logg
    def add_measurment(self):
        value = round(random.uniform(18.0, 28.0),3)
        detector_name = random.choice(list(self.all_dectors_dict.keys()))
        self.all_dectors_dict[detector_name].append(value)
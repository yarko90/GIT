import random


class Tester():

    struct = ['building', 'floor', 'office', 'room', 'detector']

    def __init__(self, n):
        self.test_sets_list = self.test_sets_maker(n)

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

    def test_detector_value(self,n):
        value = round(random.uniform(18.0, 28.0),3)
        detector_number = random.randint(0,n-1)
        detector_name = self.test_sets_list[detector_number]
        #print(detector_name)
        return (detector_name, value)
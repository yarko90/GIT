class Detector():

    def __init__ (self, name):
        self.name = name
        self.value_list = []

    def add_value(self,value):
        self.value_list.append(value)
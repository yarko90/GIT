class Detector():

    def __init__ (self, name, values):
        self.name = name
        self.values_dict = {}
        self.hour = 1
        for element in values:
            self.values_dict[self.hour] = element
            self.hour += 1
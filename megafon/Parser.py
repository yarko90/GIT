import csv
from datetime import datetime

class Parser():
    '''Read target file and make two new ones.

    time_liner - transforms document date line into needed format
    process - reads document line by line and makes two new files(tmp_0001.dat, tmp_0002.dat)

    '''

    row_ident = 'BSRID'
    temp1_ident = 'PSC'
    temp2_ident = 'BAND'

    def __init__ (self, source_file, temp1, temp2):
        self.source_file = source_file
        self.temp1 = temp1
        self.temp2 = temp2

    def time_liner(self, line):
        line = line[0].split(' ')
        line.pop(-2)
        line = ' '.join(line)
        d = datetime.strptime(line, '%a %b %d %H:%M:%S %Y')
        return d.strftime("%d-%m-%Y %H:%M:%S")

    def process (self):
        row_identificator = ' '
        target_file = 'temp1'
        with open(self.source_file, 'r') as f, open(self.temp1,'w') as temp1, open(self.temp2, 'w') as temp2:
            line_iterator = csv.reader(f, delimiter='\t')
            date_and_time = self.time_liner(line_iterator.next())
            for element in line_iterator:
                if element[0] == self.row_ident:
                    row_identificator = ';'.join(line_iterator.next())
                elif element[0] == self.temp1_ident:
                    target_file = temp1
                elif element[0] == self.temp2_ident:
                    target_file = temp2
                else:
                    line = date_and_time +';'+ row_identificator + ';'+';'.join(element)+'\n'
                    target_file.write(line)
import sys
from Parser import Parser

if __name__ == '__main__':
    print sys.argv[1]
    parser = Parser(sys.argv[1], 'tmp_0001.dat', 'tmp_0002.dat')
    parser.process()


import os, sqlite3, time
from datetime import datetime

READ_LINENO = 10
READ_SIZE = READ_LINENO*24

def csvfilereader(filepath):
    last_lines_cleaned = []
    with open(filepath, 'rb') as csvfile:
        csvfile.seek(-READ_SIZE,2)
        #last line eg. 18/04/2013 13:28,178.301
        bottom_lines = csvfile.read(READ_SIZE)
        last_lines = bottom_lines.split(b'\r\n')
        for i in range(1, READ_LINENO):
            measure_time, height = last_lines[i].split(b',')
            #datetime object eg. datetime.datetime(2013, 4, 18, 13, 28)
            #TODO: %S to be removed in production
            time_cleaned = datetime.strptime(measure_time.decode('utf-8'), '%d/%m/%Y %H:%M')
            height_cleaned = height.decode('utf-8')
            last_lines_cleaned.append([time_cleaned, height_cleaned])
        print (last_lines_cleaned)
        return last_lines_cleaned

if __name__ == "__main__":
    filepath=os.path.abspath('A___2SPL.csv')
    csvfilereader(filepath=filepath)

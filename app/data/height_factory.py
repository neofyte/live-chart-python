import os, sqlite3, time
from datetime import datetime

#a little bigger than the size of a line in the csv
READ_LINENO = 10
READ_SIZE = READ_LINENO*24

#same as the write interval in simulator.py
READ_INTERVAL = 30

#dbname
DATABASENAME = 'poolheight'

#if there exists multiple tables, these statements should be modified to funcitons
#db insert statement
def insert_statement(table_name):
    return ''.join(['INSERT INTO ', table_name, ' (datetime, height) VALUES (?,?)'])

#db create table statement
def create_statement(table_name):
    return ''.join(['CREATE TABLE ', table_name, 
        ' (id integer primary key autoincrement, datetime text, height real)'])

#db select statement
def select_statement(table_name):
    return ''.join(['SELECT datetime, height FROM ', table_name])

#the database path
DBPATH = os.path.abspath(''.join([DATABASENAME, '.db']))

#the csv file path
FILEPATH = os.path.abspath('A___2SPL.csv')
    
#read the last line of the file
#the list returned consists of a datetime object and a string
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
        return last_lines_cleaned

#push the data into a database, sqlite3 for now
def sqlite3_writer(table_name='A___2SPL', measure_time=datetime.now(), height=0.0, dbpath=DBPATH):
    #time eg. '16/04/2013 15:16'
    #TODO: %S to be removed in production
    #create a string object of format 'yyyy-mm-dd hh:mm:ss' suited to the format of mysql

    #todo:check duplicate

    time_cleaned = datetime.strftime(measure_time, '%Y-%m-%d %H:%M')
    conn = sqlite3.connect(DBPATH)
    c = conn.cursor()
    try:
        c.execute(create_statement(table_name))
    except:
        pass
    c.execute(insert_statement(table_name), 
              (time_cleaned, height))
    conn.commit()
    c.close()
        
if __name__=='__main__':
    try:
        while True:
            data_group = csvfilereader(filepath=FILEPATH)
            for measure_time, height in data_group:
                sqlite3_writer(table_name='A___2SPL',measure_time=measure_time, height=height, dbpath=DBPATH)
            conn = sqlite3.connect(DBPATH)
            c = conn.cursor()
            c.execute(select_statement('A___2SPL'))
            a = c.fetchall()
            c.close()
            print(a)
            time.sleep(READ_INTERVAL)
    except KeyboardInterrupt:
        c.close()
        print('stop')
    
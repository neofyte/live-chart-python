import os, sqlite3, time
from datetime import datetime

#a little bigger than the size of a line in the csv
READ_LINENO = 10
READ_SIZE = READ_LINENO*24

READ_INTERVAL = 300

#dbname
DATABASENAME = 'poolheight'

#the database path
DBPATH = os.path.abspath(''.join([DATABASENAME, '.db']))

#the csv file path
FILEPATH = os.path.abspath('A___2SPL.csv')

#if there exists multiple tables, these statements should be modified to funcitons
#db insert statement
def insert_statement(table_name):
    return 'INSERT INTO {0} (datetime, height) VALUES (?,?)'.format(table_name)

#db create table statement
def create_statement(table_name):
    return 'CREATE TABLE {0} \
        id integer primary key autoincrement, datetime text, height real'\
        .format(table_name,)

def select_statement(table_name, record_no=10):
    return 'SELECT datetime, height FROM {1} DESC LIMIT {0}'.format(record_no, table_name)

def table_name_generator(file_name):
    
    '''tranlate the file_name to the table_name'''

    table_name = file_name.split('.')[0]

    return table_name


class database_writer:

    ''' 
    This class accepts an updated csv file, 
    reads the last 10 lines, and sends the data 
    to the database.
    '''

    def __init__(self, file_name):

        '''
        establish the connection to the database
        '''
        
        self.db_conn = sqlite3.connect(DBPATH)
        self.cursor_object = self.db_conn.cursor()
        self.file_name = file_name
        self.table_name = table_name_generator(file_name)

    def csvfile_reader(self):

        '''
        read the csvfile
        clean the formats of time and height
        output the cleaned data
        '''

        file_name = self.file_name
        last_lines_cleaned = []

        with open(file_name, 'rb') as csvfile:
            csvfile.seek(-READ_SIZE,2)
            #last line eg. 18/04/2013 13:28,178.301
            bottom_lines = csvfile.read(READ_SIZE)
            last_lines = bottom_lines.split(b'\r\n')
            for i in range(1, READ_LINENO+1):
                measure_time, height = last_lines[i].split(b',')
                #datetime object eg. datetime.datetime(2013, 4, 18, 13, 28)
                time_cleaned = datetime.strptime(measure_time.decode('utf-8'), '%d/%m/%Y %H:%M')
                height_cleaned = height.decode('utf-8')
                last_lines_cleaned.append((time_cleaned, height_cleaned))
            return last_lines_cleaned


    def table_writer(self, data_group):

        '''
        push the data into a database, sqlite3 for now
        '''

        cursor_object = self.cursor_object
        conn = self.db_conn
        table_name = self.table_name

        #cursor_object.execute(select_statement(self.table_name))
        #selected_data = cursor_object.fetchall()

        # each data group contains 10 lists as [measure_time, height]
        # write them to the database
        # the time column is unique 
        # when exception occurs, the loop continues to the next row
        for measure_time, height in data_group:
            time_cleaned = datetime.strftime(measure_time, '%Y-%m-%d %H:%M')
            try:
                cursor_object.execute(insert_statement(table_name), 
                      (time_cleaned, height))
            except:
                continue

        conn.commit()
        
    def db_writer(self):

        cursor_object = self.cursor_object
        conn = self.db_conn
        table_name = self.table_name

        #try:
        data_group = self.csvfile_reader()
        self.table_writer(data_group)

        #print the latest records in the table

        cursor_object.execute('SELECT * FROM {0}'.format(self.table_name))
        a = cursor_object.fetchall()
        for item in a:
            id,t,h =item
            print(id,t,h)
        cursor_object.close()
        #except:
            #cursor_object.close()
        print('stop')

        
if __name__=='__main__':

    writer_instance = database_writer('A___2SPL.csv')
    writer_instance.db_writer()
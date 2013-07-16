import csv, os, random, time
from datetime import datetime

WRITE_INTERVAL = 30

#write data [time, height] into the file 'egg.csv'
#simulates the real production environment
#note that the wirte interval is set to 30 second
#whilest in production environment it is at least 300 seconds
def auto_csvwriter(filepath):
    try:
        while True:
            with open(filepath, 'a') as csvfile:
                eggs = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
                #get current time
                current_time = datetime.now()
                #time eg. '16/04/2013 15:16'
                #TODO: %S to be removed in production
                time_formulated = datetime.strftime(current_time, '%d/%m/%Y %H:%M:%S')
                #height eg. '228.842'
                #random number between 0 and 300
                height = round(random.random()*300, 2)
                eggs.writerow([time_formulated, height])
                print(time_formulated,height)
            time.sleep(WRITE_INTERVAL)
    except KeyboardInterrupt:
        csvfile.close()
        print ('Stop Due to Interruption')

if __name__ == '__main__':
    filepath = os.path.abspath('egg.csv')
    auto_csvwriter(filepath)
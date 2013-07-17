import sqlite3, os, json, time
from datetime import datetime
from flask import Flask, request, g, redirect, url_for, abort, render_template, flash, make_response

DATABASE='data/poolheight.db'
DEBUG=True

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')

app = Flask(__name__, template_folder=tmpl_dir)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def select_last_statement(tablename, line_number):
    return '''SELECT * FROM {0} ORDER BY ID DESC LIMIT {1}'''.format(tablename, line_number)

def db_query(table_name):
    g.db = connect_db()
    database_cursor = g.db.cursor()
    database_cursor.execute(select_last_statement(table_name, 10))
    #data_group is a list whose items are [id, measure_time,height]
    data_group = database_cursor.fetchall()
    data_cleaned = []

    for item in data_group:
        id, measure_time, height = item
        time_object = time.strftime("%b %d %Y %H:%M",
                    time.strptime(measure_time, '%Y-%m-%d %H:%M')
        )
        measure_time = time_object
        data_cleaned.append([id, measure_time, height])

    g.db.close()
    return data_cleaned

@app.route('/')
def main():
    return render_template('main_highcharts.html')

@app.route('/data')
def data_push():
    if request.method == 'GET':
        data = db_query()
        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
import sqlite3

#for win users without sqlite3 on PATH
#run in command line : python db_init_py_win.py
#to initialize the database
#for more tables or other options, modify the schema.sql
with open('schema.sql', 'r') as f:
	conn = sqlite3.connect('poolheight.db')
	c = conn.cursor()
	c.executescript(f.read())
	conn.commit()
	c.close()
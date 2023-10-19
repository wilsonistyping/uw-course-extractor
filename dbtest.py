import sqlite3

con = sqlite3.connect('uw.db')

cur = con.cursor()

cur.execute('''
            CREATE TABLE IF NOT EXISTS people
            (first_name TEXT, last_name TEXT)
            ''')
con.commit()

cur.close()
con.close()

# TEXT, INTEGER, REAL, BOOLEAN, BLOB,
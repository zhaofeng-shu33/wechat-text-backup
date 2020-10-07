# tested on Debian buster
# close all firefox instance first
from datetime import datetime
import sqlite3

db_file = '/home/zhaofeng/.mozilla/firefox/s899heb8.default-esr/places.sqlite'

def get_all_records(cursor):
    sqlite_command = 'select place_id, visit_date from moz_historyvisits order by visit_date'
    cursor.execute(sqlite_command)
    f = open('build/firefox.md', 'w')
    for data in cursor.fetchall():
        record_str = process_one_data(cursor, data)
        f.write(record_str)
    f.close()

def process_one_data(cursor, data):
    place_id, visit_date_timestamp = data
    time_obj = datetime.fromtimestamp(visit_date_timestamp/1e6)
    record_str = time_obj.strftime("%Y-%m-%d, %H:%M:%S")
    title, url, description = get_records(cursor, place_id)
    if title is not None:
        record_str += ' : ' + title + '\n'
    else:
        record_str += ' :\n'
    record_str += url + '\n'
    if description is not None:
        record_str += description + '\n\n'
    else:
        record_str += '\n'
    return record_str           
def get_records(cursor, id):
    sqlite_command = 'select title,url,description from moz_places where id = %d' % id
    cursor.execute(sqlite_command)
    return cursor.fetchall()[0]

if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    get_all_records(cursor)
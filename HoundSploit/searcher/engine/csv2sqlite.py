import csv
import sqlite3
import os


def create_db(init_path):
    db_path = init_path + "/HoundSploit/hound_db.sqlite3"
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("CREATE TABLE searcher_exploit (id, file, description, date, author, type, platform, port);")
    exploits_path = init_path + "/HoundSploit/csv/files_exploits.csv"
    with open(exploits_path, 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['id'], i['file'], i['description'], i['date'], i['author'], i['type'], i['platform'], i['port']) for i in dr]
    cur.executemany("INSERT INTO searcher_exploit (id, file, description, date, author, type, platform, port) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)

    cur.execute("CREATE TABLE searcher_shellcode (id, file, description, date, author, type, platform);")
    shellcodes_path = init_path + "/HoundSploit/csv/files_shellcodes.csv"
    with open(shellcodes_path, 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['id'], i['file'], i['description'], i['date'], i['author'], i['type'], i['platform']) for i in dr]
    cur.executemany("INSERT INTO searcher_shellcode (id, file, description, date, author, type, platform) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)

    con.commit()
    con.close()
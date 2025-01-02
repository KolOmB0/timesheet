"""Главный файл приложения"""
import sqlite3 as sq
import os
def update_work_team():
    db_path = os.path.join(os.path.dirname(__file__), '..')
    print(db_path)
    with sq.connect(db_path) as con:
        con.row_factory = sq.Row
        cur = con.cursor()
        DISTINCT_work_team = cur.execute("""
        SELECT DISTINCT work_team
        FROM scratch""").fetchall()
        return [row[0] for row in DISTINCT_work_team]
print(update_work_team())
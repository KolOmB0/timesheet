import sqlite3 as sq
with sq.connect("employees.db") as con:
    con.row_factory = sq.Row
    cur = con.cursor()
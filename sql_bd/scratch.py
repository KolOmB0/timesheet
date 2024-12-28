import sqlite3 as sq
with sq.connect("employees.db") as con:
    cur = con.cursor()
    # cur.execute("DROP TABLE IF EXISTS scratch")
    cur.execute(""" CREATE TABLE IF NOT EXISTS scratch (
    scratch_id INTEGER PRIMARY KEY,
    name_SNP TEXT,
    work_team TEXT,
    Date_of_employment DATE
    )""")
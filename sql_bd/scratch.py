import sqlite3 as sq
with sq.connect("employees.db") as con:
    con.row_factory = sq.Row
    cur = con.cursor()
    # Создание таблицы ork_hours
    cur.execute("""
    CREATE TABLE IF NOT EXISTS work_hours (
        id_work_hours INTEGER PRIMARY KEY AUTOINCREMENT,
        scratch_id INTEGER NOT NULL,
        date DATE NOT NULL,
        status_shift TEXT DEFAULT 'Р',
        day_shift_hours INTEGER DEFAULT 0,
        night_shift_hours INTEGER DEFAULT 0,
        FOREIGN KEY(scratch_id) REFERENCES scratch(scratch_id),
        CHECK(day_shift_hours + night_shift_hours <= 11)
    );
    """)

    # Создание триггера для вставки work_hours
    cur.execute("""
    CREATE TRIGGER IF NOT EXISTS set_work_hours_default_after_insert
    AFTER INSERT ON work_hours
    FOR EACH ROW
    BEGIN
        -- Если статус смены 'п' (прогул), 'б' (болезнь) или пустое значение, устанавливаем часы 0
        UPDATE work_hours
        SET day_shift_hours = CASE
            WHEN NEW.status_shift IN ('П', 'Б', '') THEN 0
            ELSE NEW.day_shift_hours
        END,
        night_shift_hours = CASE
            WHEN NEW.status_shift IN ('П', 'Б', '') THEN 0
            ELSE NEW.night_shift_hours
        END
        WHERE id_work_hours = NEW.id_work_hours;
    END;
    """)

    # Создание триггера для обновления
    cur.execute("""
    CREATE TRIGGER IF NOT EXISTS set_work_hours_default_after_update
    AFTER UPDATE ON work_hours
    FOR EACH ROW
    BEGIN
        -- Если статус смены 'п' (прогул), 'б' (болезнь) или пустое значение, устанавливаем часы 0
        UPDATE work_hours
        SET day_shift_hours = CASE
            WHEN NEW.status_shift IN ('П', 'Б', '') THEN 0
            ELSE NEW.day_shift_hours
        END,
        night_shift_hours = CASE
            WHEN NEW.status_shift IN ('П', 'Б', '') THEN 0
            ELSE NEW.night_shift_hours
        END
        WHERE id_work_hours = NEW.id_work_hours;
    END;
    """)


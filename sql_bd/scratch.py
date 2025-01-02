import sqlite3 as sq
from datetime import datetime, timedelta
import os
def update_work_team():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'sql_bd', 'employees.db')
    with sq.connect(db_path) as con:
        con.row_factory = sq.Row
        cur = con.cursor()
        DISTINCT_work_team = cur.execute("""
        SELECT DISTINCT work_team
        FROM scratch""").fetchall()
        return [row[0] for row in DISTINCT_work_team]
def update_name_SNP():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'sql_bd', 'employees.db')
    with sq.connect(db_path) as con:
        con.row_factory = sq.Row
        cur = con.cursor()
        DISTINCT_name_SNP = cur.execute("""
        SELECT DISTINCT name_SNP
        FROM scratch""").fetchall()
        return [row[0] for row in DISTINCT_name_SNP]
def timesheet_generation(fin):
    db_path = os.path.join(os.path.dirname(__file__), '..', 'sql_bd', 'employees.db')
    try:
        with sq.connect(db_path) as con:
            cur = con.cursor()
            # Преобразуем входную дату в первый и последний день месяца
            input_date = datetime.strptime(fin, "%m.%Y")
            start_date = input_date.replace(day=1) # 1й день текушего месяца
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1) # последний день текушего месяца
            # Находим последнюю дату прошлого месяца для смены A
            prev_month_end = start_date - timedelta(days=1) # последний день предыдущего месяца.
            cur.execute("""
                    SELECT date, day_shift_hours, night_shift_hours
                    FROM work_hours wh
                    JOIN scratch s on s.scratch_id = wh.scratch_id
                    WHERE work_team = 'A' AND date <= ?
                    ORDER BY date DESC
                    LIMIT 1
                """, (prev_month_end.strftime('%d.%m.%Y'),))

            last_entry = cur.fetchone()
            # Последовательность смен для команды A, B, C, D
            sequence = [
                (11, None),  # 1-е число
                (2, 2),  # 2-е число
                (1, 6),  # 3-е число
                (None, None)  # 4-е число
            ]
            # Определяем позицию в последовательности
            seq_index = 0
            if last_entry: # существует ли запись о последней смене
                last_day_shift, last_night_shift = last_entry[1], last_entry[2]
                for idx, (day_hours, night_hours) in enumerate(sequence): # Перебор последовательности смен:
                    if last_day_shift == day_hours and last_night_shift == night_hours: # Проверка соответствия смен
                        seq_index = (idx + 1) % len(sequence)
                        break
            # Генерация данных для текущего месяца
            for day in range(1, end_date.day + 1):
                current_date = start_date + timedelta(days=day - 1)
                # Проверяем наличие записи
                cur.execute("""
                SELECT * FROM work_hours
                WHERE scratch_id IN (
                SELECT scratch_id FROM scratch WHERE work_team = 'A'
                ) AND date = ?
                """, (current_date.strftime('%d.%m.%Y'),))
                if not cur.fetchone(): #Проверка, существует ли уже запись для текущей даты:
                    # Вставляем новую запись
                    day_shift_hours, night_shift_hours = sequence[seq_index] # Определение количества дневных и ночных смен
                    cur.execute("""
                    INSERT INTO work_hours (scratch_id, date, day_shift_hours, night_shift_hours, status_shift)
                    SELECT scratch_id, ?, ?, ?, 'Р'
                    FROM scratch WHERE work_team = 'A'
                    """, (current_date.strftime('%d.%m.%Y'), day_shift_hours, night_shift_hours))
                    # Обновляем индекс последовательности
                    seq_index = (seq_index + 1) % len(sequence)
        # Сохраняем изменения
        con.commit()
        print("Данные успешно сгенерированы для команды A.")
    except sq.Error as e:
        print(f"Ошибка работы с базой данных: {e}")

if __name__ == "__main__":
    timesheet_generation("12.2023")
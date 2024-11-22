import sqlite3
from sqlite3 import Connection as Db


#-----------------------------------------------------------------------------------------------------------------------
# database
def create_db(database_name: str):
    # Создайте файл базы данных not_telegram.db
    # и подключитесь к ней, используя встроенную библиотеку sqlite3.
    db = sqlite3.connect(database_name)
    return db


def close_db(db: Db):
    db.commit()
    db.close()


def create_table(db: Db, table: str):
    # Создайте объект курсора
    cursor = db.cursor()
    # Создайте таблицу Users, если она ещё не создана.
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {table} ('
        # В этой таблице должны присутствовать следующие поля:
        'id INTEGER PRIMARY KEY,'   # целое число, первичный ключ
        'username TEXT NOT NULL,'   # текст (не пустой)
        'email TEXT NOT NULL,'      # текст (не пустой)
        'age INTEGER,'              # целое число
        'balance INTEGER NOT NULL'  # целое число (не пустой)
    ')')

    delete_from_db(db, table)
    #cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users (email)')


def delete_from_db(db: Db, table: str, cond: str = 'TRUE', value: tuple = ()):
    cursor = db.cursor()
    cmd = f'DELETE FROM {table} WHERE {cond}'
    cursor.execute(cmd, value)


def update_db(db: Db, table: str, op: str, cond: str, params: tuple):
    cursor = db.cursor()
    cmd = f'UPDATE {table} SET {op} WHERE {cond}'
    cursor.execute(cmd, params)


def fetch_records(db: Db, table: str, cond: str = 'TRUE', value: tuple = ()):
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM {table} WHERE {cond}', value)
    return cursor.fetchall()


def op_db(db: Db, table: str, op: str, cond: str = 'TRUE', value: tuple = ()):
    cursor = db.cursor()
    cursor.execute(f'SELECT {op} FROM {table} WHERE {cond}', value)
    return cursor.fetchone()[0]


#-----------------------------------------------------------------------------------------------------------------------
# print
def print_records(records: list):
    for _, username, email, age, balance in records:
        print(f'Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')


#-----------------------------------------------------------------------------------------------------------------------
# tests
def fill_table(db: Db, table: str):
    cursor = db.cursor()
    # Заполните её 10 записями:
    for i in range(1, 11):
        cmd = f'INSERT INTO {table} (username, email, age, balance) VALUES (?, ?, ?, ?)'
        params = f'User{i}', f'example{i}@gmail.com', str(i*10), 1000
        cursor.execute(cmd, params)


def modify_table(db: Db, table: str):
    # Обновите balance у каждой 2ой записи начиная с 1ой на 500:
    for i in range(1, 11, 2):
        update_db(db, table, 'balance = ?', 'username = ?', (500, f'User{i}'))

    # Удалите каждую 3ую запись в таблице начиная с 1ой:
    for i in range(1, 11, 3):
        delete_from_db(db, table, 'username = ?', (f'User{i}',))


def test1(db: Db, table: str):
    # Сделайте выборку всех записей при помощи fetchall(), где возраст не равен 60
    results = fetch_records(db, table, 'age != ?', ('60',))
#    results = fetch_records(db, table)
    print_records(results)


def test2(db: Db, table: str):
    # Удалите из базы данных not_telegram.db запись с id = 6.
    delete_from_db(db, table, 'id = ?', ('6',))
    # Подсчитать общее количество записей.
    records_count = op_db(db, table, 'COUNT(*)')
    # Посчитать сумму всех балансов.
    records_sum = op_db(db, table, 'SUM(balance)')
    records_avg = records_sum / records_count
    # Вывести в консоль средний баланс всех пользователей.
    print(records_avg)

#    records_avg = op_db(db, table, 'AVG(balance)')
#    print(records_avg)
    """
    Вывод на консоль:
    700.0
    """


def main():
    db = create_db('not_telegram.db')
    table = 'Users'
    create_table(db, table)
    fill_table(db, table)
    modify_table(db, table)
#    test1(db, table)
    test2(db, table)
    close_db(db)


if __name__ == '__main__':
    main()


"""
2024/01/30 00:00|Домашнее задание по теме "Выбор элементов и функции в SQL запросах"
Если вы решали старую версию задачи, проверка будет производиться по ней.
Ссылка на старую версию тут.
Цель: научится использовать функции внутри запросов языка SQL и использовать их в решении задачи.

Задача "Средний баланс пользователя":
Для решения этой задачи вам понадобится решение предыдущей.
Для решения необходимо дополнить существующий код:
Удалите из базы данных not_telegram.db запись с id = 6.
Подсчитать общее количество записей.
Посчитать сумму всех балансов.
Вывести в консоль средний баланс всех пользователей.



Пример результата выполнения программы:
Выполняемый код:
# Код из предыдущего задания
# Удаление пользователя с id=6
# Подсчёт кол-ва всех пользователей
# Подсчёт суммы всех балансов
print(all_balances / total_users)
connection.close()

Вывод на консоль:
700.0

Файл module_14_2.py с кодом и базу данных not_telegram.db загрузите на ваш GitHub репозиторий. В решении пришлите ссылку на него.
"""
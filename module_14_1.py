import sqlite3
from sqlite3 import Connection as Db


def create_db(database_name: str):
    # Создайте файл базы данных not_telegram.db
    # и подключитесь к ней, используя встроенную библиотеку sqlite3.
    db = sqlite3.connect(database_name)
    return db


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

    cursor.execute(f'DELETE FROM {table}')
    #cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users (email)')


def fill_table(db: Db, table: str):
    cursor = db.cursor()
    # Заполните её 10 записями:
    for i in range(1, 11):
        cmd = f'INSERT INTO {table} (username, email, age, balance) VALUES (?, ?, ?, ?)'
        params = f'User{i}', f'example{i}@gmail.com', str(i*10), 1000
        cursor.execute(cmd, params)


def modify_table(db, table: str):
    cursor = db.cursor()
    # Обновите balance у каждой 2ой записи начиная с 1ой на 500:
    for i in range(1, 11, 2):
        cmd = f'UPDATE {table} SET balance = ? WHERE username = ?'
        params = 500, f'User{i}'
        cursor.execute(cmd, params)

    # Удалите каждую 3ую запись в таблице начиная с 1ой:
    for i in range(1, 11, 3):
        cmd = f'DELETE FROM {table} WHERE username = ?'
        params = f'User{i}',
        cursor.execute(cmd, params)


def fetch_records(db: Db, table: str):
    cursor = db.cursor()
    # Сделайте выборку всех записей при помощи fetchall(), где возраст не равен 60
    cursor.execute(f'SELECT * FROM {table} WHERE age != 60')
    return cursor.fetchall()


def print_records(records: list):
    # и выведите их в консоль в следующем формате (без id):
    # Имя: <username> | Почта: <email> | Возраст: <age> | Баланс: <balance>
    for _, username, email, age, balance in records:
        print(f'Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')


def close_db(db: Db):
    db.commit()
    db.close()


def main():
    db = create_db('not_telegram.db')
    table = 'Users'
    create_table(db, table)
    fill_table(db, table)
    modify_table(db, table)
    results = fetch_records(db, table)
    print_records(results)
    close_db(db)

    """
    Вывод на консоль:
    Имя: User2 | Почта: example2@gmail.com | Возраст: 20 | Баланс: 1000
    Имя: User3 | Почта: example3@gmail.com | Возраст: 30 | Баланс: 500
    Имя: User5 | Почта: example5@gmail.com | Возраст: 50 | Баланс: 500
    Имя: User8 | Почта: example8@gmail.com | Возраст: 80 | Баланс: 1000
    Имя: User9 | Почта: example9@gmail.com | Возраст: 90 | Баланс: 500
    """


if __name__ == '__main__':
    main()


"""
2024/01/29 00:00|Домашнее задание по теме "Создание БД, добавление, выбор и удаление элементов."
Если вы решали старую версию задачи, проверка будет производиться по ней.
Ссылка на старую версию тут.
Цель: освоить основные команды языка SQL и использовать их в коде используя SQLite3.

Задача "Первые пользователи":
Создайте файл базы данных not_telegram.db и подключитесь к ней, используя встроенную библиотеку sqlite3.
Создайте объект курсора и выполните следующие действия при помощи SQL запросов:
Создайте таблицу Users, если она ещё не создана. В этой таблице должны присутствовать следующие поля:
id - целое число, первичный ключ
username - текст (не пустой)
email - текст (не пустой)
age - целое число
balance - целое число (не пустой)
Заполните её 10 записями:
User1, example1@gmail.com, 10, 1000
User2, example2@gmail.com, 20, 1000
User3, example3@gmail.com, 30, 1000
...
User10, example10@gmail.com, 100, 1000
Обновите balance у каждой 2ой записи начиная с 1ой на 500:
User1, example1@gmail.com, 10, 500
User2, example2@gmail.com, 20, 1000
User3, example3@gmail.com, 30, 500
...
User10, example10@gmail.com, 100, 1000
Удалите каждую 3ую запись в таблице начиная с 1ой:
User2, example2@gmail.com, 20, 1000
User3, example3@gmail.com, 30, 500
User5, example5@gmail.com, 50, 500
...
User9, example9@gmail.com, 90, 500

Сделайте выборку всех записей при помощи fetchall(), где возраст не равен 60 и выведите их в консоль в следующем формате (без id):
Имя: <username> | Почта: <email> | Возраст: <age> | Баланс: <balance>

Пример результата выполнения программы:
Вывод на консоль:
Имя: User2 | Почта: example2@gmail.com | Возраст: 20 | Баланс: 1000
Имя: User3 | Почта: example3@gmail.com | Возраст: 30 | Баланс: 500
Имя: User5 | Почта: example5@gmail.com | Возраст: 50 | Баланс: 500
Имя: User8 | Почта: example8@gmail.com | Возраст: 80 | Баланс: 1000
Имя: User9 | Почта: example9@gmail.com | Возраст: 90 | Баланс: 500
Содержание БД:


Файл module_14_1.py с кодом и базу данных not_telegram.db загрузите на ваш GitHub репозиторий. В решении пришлите ссылку на него.
"""
import sqlite3


def db_connect():
    global conn, cursor
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    # Пользователи
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id integer primary key,
                            username text not null,
                            password text not null,
                            tg_id integer,
                            name text,
                            pet_id integer,
                            role integer);
                        ''')
    # role 0 - пользователь 1 - администратор
    conn.commit()
    # Питомцы

    cursor.execute('''CREATE TABLE IF NOT EXISTS pets
                            (pet_id integer primary key,
                            name text not null,
                            birthdate text not null,
                            animal_type integer,
                            breed_id integer,
                            colour_id integer);
                            ''')

    # 0 - кошка 1 - собака
    conn.commit()
    # Породы

    cursor.execute('''CREATE TABLE IF NOT EXISTS breeds
                            (breed_id integer primary key,
                            animal_type integer,
                            name_breed text not null);
                            ''')
    conn.commit()

    # Вакцинация

    cursor.execute('''CREATE TABLE IF NOT EXISTS vaccination
                            (vaccination_id integer primary key,
                            user_id integer,
                            pet_id integer,
                            vaccine_type integer,
                            vaccination_date text,
                            vaccination_untill_date text);
                            ''')
    conn.commit()

    # Тип вакцины

    cursor.execute('''CREATE TABLE IF NOT EXISTS vaccination_type
                            (vaccine_type_id integer primary key,
                            vaccine_type integer,
                            vaccine_name text not null);
                            ''')
    conn.commit()


def breed():
    with open('breeds_cat.txt') as f:
        breeds = f.readlines()
    all_breeds = [(i, 0, x.strip()) for i, x in enumerate(breeds)]
    cursor.executemany('''INSERT INTO breeds (breed_id, animal_type, name_breed)
                            VALUES (?, ?, ?);''', all_breeds)
    conn.commit()
    cursor.execute('SELECT * FROM breeds')
    print(cursor.fetchall())

    cursor.execute("SELECT breed_id FROM breeds ORDER BY breed_id DESC LIMIT 1")
    last_id = cursor.fetchone()[0] + 1
    print(last_id)

    with open('breeds_dog.txt') as f:
        breeds = f.readlines()
    all_breeds = [(last_id + i, 1, x.strip()) for i, x in enumerate(breeds)]
    cursor.executemany('''INSERT INTO breeds (breed_id, animal_type, name_breed)
                                VALUES (?, ?, ?);''', all_breeds)
    conn.commit()
    cursor.execute('SELECT * FROM breeds')
    print(cursor.fetchall())


def ds():
    cursor.execute("SELECT breed_id FROM breeds ORDER BY breed_id DESC LIMIT 1")
    x = cursor.fetchone()
    if x:
        last_id = cursor.fetchone()[0] + 1
    else: x = 0
    print(last_id)
    cursor.execute('''INSERT INTO users (id, username, tg_id) VALUES (?,?);''', (username, tg_id))


if __name__ == '__main__':
    db_connect()
    breed()

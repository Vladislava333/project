import sqlite3


def db_connect():
    global conn, cursor
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    # Пользователи
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id integer primary key,
                            username text not null,
                            password text,
                            tg_id integer,
                            name text,
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


def db_check_user(tg_id):
    cursor.execute("SELECT id, username, tg_id FROM users WHERE tg_id=? LIMIT 1", (tg_id,))
    user_data = cursor.fetchone()
    print(user_data)
    return user_data


def db_check_users():
    cursor.execute("SELECT * FROM users")
    user_data = cursor.fetchall()


def db_add_user(name, tg_id):
    cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
    x = cursor.fetchone()
    print(x)
    if x:
        last_id = x[0] + 1
    else:
        last_id = 0
    cursor.execute('''INSERT INTO users (id, username, tg_id) VALUES (?,?,?);''', (last_id, name, tg_id))
    conn.commit()
    cursor.execute('SELECT * FROM users')
    print(cursor.fetchall())



if __name__ == '__main__':
    db_connect()
    db_check_users()

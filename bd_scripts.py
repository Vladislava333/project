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
                            user_id integer,
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
    with open('../Владка Кучева/vladaK/breeds_cat.txt') as f:
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

    with open('../Владка Кучева/vladaK/breeds_dog.txt') as f:
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
    print(user_data)


def db_add_user(name, tg_id):
    cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
    x = cursor.fetchone()
    if x:
        last_id = x[0] + 1
    else:
        last_id = 0
    cursor.execute('''INSERT INTO users (id, username, tg_id) VALUES (?,?,?);''', (last_id, name, tg_id))
    conn.commit()
    cursor.execute('SELECT * FROM users')
    print(cursor.fetchall())


def savePet(*args, user):
    cursor.execute("SELECT pet_id FROM pets ORDER BY pet_id DESC LIMIT 1")
    x = cursor.fetchone()
    print('_____')
    print(x)
    print('_____')
    if x:
        last_id = x[0] + 1
    else:
        last_id = 0
    print(args)
    cursor.execute("SELECT id FROM users WHERE tg_id=?", (user,))
    uid = cursor.fetchone()
    p = (last_id, uid[0], args[0], args[2], args[1])
    #print(last_id, uid[0], args[0], args[2], args[1])
    #p = (1, 0, 'Коля', '01.01.2023', 1)

    cursor.execute('''INSERT INTO pets
                    (pet_id, user_id, name, birthdate, animal_type)
                    VALUES (?, ?, ?, ?, ?)
                    ''', p)
    conn.commit()
    all_pets()


def check_animal_type(t):
    if t == 0:
        return 'Кошка'
    elif t == 1:
        return 'Собака'


def get_pets(u_id):
    cursor.execute('''SELECT pets.name, pets.animal_type FROM pets JOIN users
                         ON users.id=pets.user_id
                         WHERE users.tg_id=?''', (u_id,))
    a = '\n'.join([' '.join([check_animal_type(x[1]), x[0]]) for x in cursor.fetchall()])
    return a

def get_pets_id(u_id):
    cursor.execute('''SELECT pets.pet_id, pets.name, pets.animal_type FROM pets JOIN users
                         ON users.id=pets.user_id
                         WHERE users.tg_id=?''', (u_id,))

    return cursor.fetchall()

def all_pets():
    cursor.execute('''SELECT * FROM pets''')
    #cursor.execute("SELECT pet_id FROM pets ORDER BY pet_id DESC LIMIT 1")
    a = cursor.fetchall()
    print(a)


def get_all_vacs():
    cursor.execute('''SELECT * FROM vaccination ''')
    return cursor.fetchall()

def get_vacs(u_id):
    cursor.execute('''SELECT vaccination.pet_id, 
                        vaccination.vaccine_type,
                        vaccination_untill_date
                        FROM vaccination JOIN users
                         ON users.id=vaccination.user_id
                         WHERE users.tg_id=?''', (u_id,))
    #a = '\n'.join([' '.join([check_animal_type(x[1]), x[0]]) for x in cursor.fetchall()])
    return a


if __name__ == '__main__':
    db_connect()
    #all_pets()
    get_vacs(u_id)

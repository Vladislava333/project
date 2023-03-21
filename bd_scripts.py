import sqlite3
from datetime import datetime

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


def set_vasc():
    v = [(0, 0, 'Первая'), (1, 0, 'Хорошая'), (2, 0, 'Неинтересная')]
    cursor.executemany('''INSERT INTO vaccination_type (
                         vaccine_type_id, vaccine_type,vaccine_name)
                          VALUES(?,?,?)''', v)
    #cursor.execute("DROP TABLE vaccination_type ")
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

    a = cursor.fetchall()
    print(a)


def get_all_vacs1():
    date = datetime.today().strftime("%d.%m.%Y")
    DELTA = '+2 year' #минимальный срок предупреждения о вакцине
    cursor.execute('''SELECT users.tg_id, 
                                users.username,
                                pets.name, 
                                pets.animal_type,
                                vaccination.vaccination_untill_date,
                                vaccination_type.vaccine_name
                                FROM vaccination 
                                JOIN users
                                ON users.id=vaccination.user_id
                                JOIN pets ON pets.pet_id=vaccination.pet_id
                                JOIN vaccination_type ON vaccination_type.vaccine_type_id = vaccination.vaccine_type
                                WHERE strftime(vaccination_untill_date) - date(?) < ? 
                                 ''', (date, '+2 year'))
    return cursor.fetchall()

def get_all_vacs():
    date = datetime.today().strftime("%d.%m.%Y")
    DELTA = '+2 year' #минимальный срок предупреждения о вакцине
    cursor.execute('''SELECT users.tg_id,
                            users.username,
                            pets.name, 
                            pets.animal_type,
                            vaccination.vaccination_untill_date,
                            vaccination_type.vaccine_name
                            FROM vaccination    
                            JOIN users
                            ON users.id=vaccination.user_id
                            JOIN pets ON pets.pet_id=vaccination.pet_id
                            JOIN vaccination_type ON vaccination_type.vaccine_type_id = vaccination.vaccine_type
                                 ''')
    return cursor.fetchall()



def get_vacs(u_id):
    cursor.execute('''SELECT pets.name, 
                        pets.animal_type,
                        vaccination_untill_date,
                        vaccination_type.vaccine_name
                        FROM vaccination JOIN users
                         ON users.id=vaccination.user_id
                         JOIN pets ON pets.pet_id=vaccination.pet_id
                         JOIN vaccination_type ON vaccination_type.vaccine_type_id = vaccination.vaccine_type
                         WHERE users.tg_id=?''', (u_id,))
    animal_types = ['Кошка', 'Собака']
    a = '\n'.join([' '.join([check_animal_type(x[1]), x[0], x[2], '\nВакцина', x[3]]) for x in cursor.fetchall()])
    return a


def get_vac_types():
    cursor.execute('''SELECT vaccine_type_id ,vaccine_name FROM vaccination_type''')
    v = list(map(lambda x: x[1], cursor.fetchall()))
    return cursor.fetchall()

def set_year(date_):
    d = date_.split('.')
    year = str(int(d[-1])+1)
    res = '.'.join([d[0], d[1], year])
    return res


def saveVasc(*args, user):
    cursor.execute("SELECT vaccination_id FROM vaccination ORDER BY vaccination_id DESC LIMIT 1")
    x = cursor.fetchone()
    if x:
        last_id = x[0] + 1
    else:
        last_id = 0
    print(args)
    cursor.execute("SELECT id FROM users WHERE tg_id=?", (user,))
    uid = cursor.fetchone()
    p = (last_id, uid[0], args[0], args[1], args[2], set_year(args[2]))
    print(p)

    cursor.execute('''INSERT INTO vaccination
                        (vaccination_id,
                        user_id, 
                        pet_id, 
                        vaccine_type, 
                        vaccination_date,
                        vaccination_untill_date)
                        VALUES (?, ?, ?, ?, ?, ?)
                        ''', p)
    conn.commit()


if __name__ == '__main__':
    db_connect()
    get_vac_types()

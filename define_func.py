def create_table(cur):  # Создаём таблицы
    cur.execute('''CREATE TABLE IF NOT EXISTS client (
        id SERIAL PRIMARY KEY,
        name VARCHAR(80) NOT NULL,
        surname VARCHAR(80) NOT NULL,
        email VARCHAR(80) NOT NULL);''')
    cur.execute('''CREATE TABLE IF NOT EXISTS phone (
        id SERIAL PRIMARY KEY,
        number VARCHAR(21) NOT NULL,
        client_id INTEGER REFERENCES client(id));''')


def drop_table(cur):  # Удаляем таблицы
    cur.execute('''DROP TABLE phone;''')
    cur.execute('''DROP TABLE client;''')


def select_all(cur):  # Выдаём все данные
    cur.execute('''SELECT client.id,
                          client.name,
                          client.surname,
                          client.email,
                          phone.number
                    FROM client
                    LEFT JOIN phone ON client.id = phone.client_id
                    ORDER BY id;''')
    result = cur.fetchall()
    return result


def add_client(cur, name, surname, email, number=None):  # Добавляем нового клиента
    cur.execute('''INSERT INTO client(name, surname, email)
        VALUES (%s, %s, %s) RETURNING id;''', (name, surname, email))
    result = cur.fetchone()[0]
    if number:
        cur.execute('''INSERT INTO phone(number, client_id)
            VALUES (%s, %s);''', (number, result))
    return result


def add_number(cur, client_id, number: str):  # Добавляем один номер к клиенту
    cur.execute('''INSERT INTO phone(number, client_id)
        VALUES (%s, %s) RETURNING id;''', (number, client_id))
    result = cur.fetchone()
    return result


def change_client(cur, client_id, name=None, surname=None, email=None):  # Меняем данные клиента
    if name:
        cur.execute('''UPDATE client SET name = %s
            WHERE id = %s;''', (name, client_id))
    if surname:
        cur.execute('''UPDATE client SET surname = %s
            WHERE id = %s;''', (surname, client_id))
    if email:
        cur.execute('''UPDATE client SET email = %s
            WHERE id = %s;''', (email, client_id))
    result = cur.statusmessage
    return result


def delete_phone(cur, client_id, number=None):  # Удаляем номера клиента
    if number is None:
        cur.execute('''DELETE FROM phone
            WHERE client_id = %s;''', (client_id, ))
    else:
        cur.execute('''DELETE FROM phone
            WHERE client_id = %s AND number = %s;''', (client_id, number))


def delete_client(cur, client_id):  # Удаляем клиента
    cur.execute('''DELETE FROM phone
        WHERE client_id = %s;''', (client_id,))
    cur.execute('''DELETE FROM client
        WHERE id = %s;''', (client_id,))


def find_client(cur, *, name=None, surname=None, email=None, number=None):  # Ищем клиента
    cur.execute('''SELECT client.id, name, surname, email, number FROM client
        LEFT JOIN phone ON client.id = phone.client_id
        WHERE email = %s OR number = %s OR name = %s OR surname = %s;''',
                (email, number, name, surname))
    result = cur.fetchall()
    return result

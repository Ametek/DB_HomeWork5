import psycopg2
from psycopg2 import Error
from define_func import (create_table, drop_table,  select_all,
                         add_client, add_number, change_client,
                         delete_phone, delete_client, find_client)
from pprint import pprint


def tests():
    # basename = input('Введите название базы клиентов: ')
    # username = input('Введите имя пользователя: ')
    # password = input('Введите пароль: ')
    basename = 'clientbase'
    username = 'postgres'
    password = '8846'

    try:
        conn = psycopg2.connect(database=basename, user=username, password=password)

        with conn:
            with conn.cursor() as cur:
                if cur.execute('''SELECT EXISTS (
                                  SELECT FROM pg_tables
                                  WHERE tablename = 'phone');''') is None:
                    drop_table(cur)  # Удаляем таблицы при наличии оных

        with conn:
            with conn.cursor() as cur:
                create_table(cur)  # Создаём таблицы

        with conn:
            with conn.cursor() as cur:
                print('\nВыводим созданную таблицу. Если таблица пустая, то она пустая:)')
                print(select_all(cur))

        with conn:
            with conn.cursor() as cur:  # Заполняем таблицу первородными данными
                add_client(cur, 'Рулон', 'Обоев', 'rulon@mail.ru', '+7987654321')
                add_client(cur, 'Камаз', 'Отходов', 'kamaz@mail.ru')
                add_client(cur, 'Волочила', 'Мудипополу', 'volochila@mail.hu', '+7765432198')
                add_client(cur, 'Угон', 'Харлеев', 'ugon@mail.ru', '+7321798454')
                add_client(cur, 'Херанука', 'Пороялю', 'heranuka@mail.jp')

        with conn:
            with conn.cursor() as cur:
                print('\nВыводим таблицу после заполнения первородными данными:')
                pprint(select_all(cur))

        with conn:
            with conn.cursor() as cur:  # Вносим дополнительные номера для клиентов
                add_number(cur, 3, '+7654321987')
                add_number(cur, 2, '+7891218775')

        with conn:
            with conn.cursor() as cur:  # Меняем какие-нибудь данные какого-нибудь клиента
                change_client(cur, 2, surname='Баянов')

        with conn:
            with conn.cursor() as cur:
                delete_phone(cur, 1, '+7987654321')

        with conn:
            with conn.cursor() as cur:  # Удаляем неугодного клиента
                delete_client(cur, 4)

        with conn:
            with conn.cursor() as cur:
                print('\nВыводим таблицу после всех наших противоестественных манипуляций:')
                pprint(select_all(cur))

        with conn:
            with conn.cursor() as cur:  # Ищем клиента, даже если он против
                print('\nА вот тут выходят результаты поиска:')
                result = find_client(cur, number='+7654321987')
                pprint(result)
                result = find_client(cur, name='Херанука')
                pprint(result)

        conn.close()

    except(Exception, Error) as error:
        print('При выполнении запроса произошла ошибка: ', error)


if __name__ == '__main__':
    tests()

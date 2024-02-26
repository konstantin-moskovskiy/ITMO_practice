import psycopg2

conn = psycopg2.connect(dbname="postgres", user="postgres", password="123456", host="127.0.0.1")
cursor = conn.cursor()

def create_db():
    cursor.execute("""CREATE TABLE table_name (
                        id SERIAL NOT NULL,
                        id_List INTEGER NOT NULL,
                        id_Row INTEGER NOT NULL,
                        id_Cam INTEGER NOT NULL,
                        PRIMARY KEY (id)
                        );""")
    conn.commit()

def insert_to_table():
    cursor.execute("""INSERT INTO
                            table_name(id_List, id_Row, id_Cam)
                            VALUES(1, 2, 3);""")
    conn.commit()


def read_from_table():
    cursor.execute("""SELECT * FROM table_name;""")
    return cursor.fetchall()

def updating_values():
    cursor.execute("""UPDATE table_name SET id_List = 4, id_Row = 5, id_Cam = 6
                        WHERE id = 1;""")
    conn.commit()

def delete_rows():
    cursor.execute(""" DELETE FROM table_name WHERE id = 1;""")
    conn.commit()


if __name__ == '__main__':
    ...
    # create_db() создание таблицы в бд
    # insert_to_table() вставка строк в таблицу
    # read_from_table() чтение строк из таблицы
    # updating_values() обновление значений в строке/ах
    # delete_rows() удаление строк



cursor.close()  # закрываем курсор
conn.close()    # закрываем подключение
from mariadb import connect
from mariadb.connections import Connection

def _get_connection() -> Connection:
<<<<<<< Updated upstream:data/database.py
    return connect(user='root', password='0887123168', host='localhost', port=3306, database='web_project')
=======
    return connect(
        user='root',
        password='0887123168',
        host='localhost',
        port=3306,
        database='web_project'
    )

>>>>>>> Stashed changes:Web-Project/data_/database.py

def read_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)

def insert_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid

def update_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

    return True
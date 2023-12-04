import sqlite3
import os

class DbHelper:

    def __init__(self) -> None:
        self.DB_FILE_PATH = f'{os.getcwd()}/temp/database.db'

        # хардкодим креды
        self.host = '10.0.0.99'
        self.port = 3306
        self.user = 'USER_DB'
        self.password = 'Pa$$w0rd'


    def initialize(self):
        db_exists = os.path.exists(self.DB_FILE_PATH)

        if db_exists:
            return
        
        self._create_database()

    
    def execute_read(self, sql, params={}):
        con = None
        try:
            con = self._get_db_connection()
            cur = con.cursor()

            cur.execute(sql, params)
            result = cur.fetchall()

            return result

        finally:
            if con is not None:
                con.close()


    def _create_database(self):
        con = None
        try:
            con = self._get_db_connection()
            cur = con.cursor()

            cur.execute('CREATE TABLE users (id integer, username text, password text, is_admin integer)') # создаем бд с пользователями
            cur.execute('INSERT INTO users VALUES (1, "admin", "21232f297a57a5a743894a0e4a801fc3", 1)') #admin
            cur.execute('INSERT INTO users VALUES (2, "prettyroseslover", "8287458823facb8ff918dbfabcd22ccb", 0)') #parola
            cur.execute('INSERT INTO users VALUES (3, "anonymus", "5f4dcc3b5aa765d61d8327deb882cf99", 0)') # password
            
            # База данных для XSS
            cur.execute('CREATE TABLE books (id integer, name text, value real)')
            cur.execute('INSERT INTO books VALUES (1, "Little Women", 19.99)')
            cur.execute('INSERT INTO books VALUES (2, "Solaris", 20.50)')
            cur.execute('INSERT INTO books VALUES (3, "Moby Dick", 30.00)')
            cur.execute('INSERT INTO books VALUES (4, "La Divina Commedia", 17.50)')
            cur.execute('INSERT INTO books VALUES (5, "Das Kapital", 18.99)')
            
            con.commit()
            con.close()
        finally:
            if con is not None:
                con.close()


    def _get_db_connection(self):
        return sqlite3.connect(self.DB_FILE_PATH)


db_helper = DbHelper()
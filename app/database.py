import sqlite3
from app.logger import Logger


class Sqlite:

    def __init__(self, name):
        self.name = name
        self.conn, self.cur = self.connect()

    def connect(self):
        logger = Logger('sqlite_connect').set_logger()
        sqlite_connection=None
        cursor=None
        try:
            sqlite_connection = sqlite3.connect(self.name)
            cursor = sqlite_connection.cursor()
            logger.info(f"The SQLite database '{self.name}' is created")
        except sqlite3.Error as err:
            logger.error(err)

        return sqlite_connection, cursor

    def insert(self, sql_insert_query, list_of_companies):
        logger = Logger('sqlite_insert').set_logger()
        try:
            self.cur.executemany(sql_insert_query, list_of_companies)
            self.conn.commit()
            logger.info(f"Total of {self.cur.rowcount} records inserted successfully into table")
        except sqlite3.Error as err:
            logger.error(err)

    def execute(self, query):
        logger = Logger('sqlite_execute').set_logger()
        rows = []
        try:
            self.cur.execute(query)
            self.conn.commit()
            rows = self.cur.fetchall()
        except sqlite3.Error as err:
            logger.error(err)

        return rows

    def close_connection(self):
        logger = Logger('sqlite_close_connection').set_logger()
        if self.conn:
            self.conn.close()
            logger.info("The SQLite connection is closed")


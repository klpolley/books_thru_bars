import psycopg2
import psycopg2.extras
from app.scripts.database.config import config
import sys


def connect():
    try:
        params = config()
        con = psycopg2.connect(**params)
        cur = con.cursor()
        cur.execute('SELECT version()')
        version = cur.fetchone()[0]
        print(version)

        return con

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)


def disconnect(con):
    if con:
        con.close()


if __name__ == '__main__':
    connect()

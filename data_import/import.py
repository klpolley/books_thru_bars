import sys
from psycopg2 import Error, DatabaseError

from data_import.connect import connect, disconnect
from data_import.read_csv import read_library_csv


def insert_books(conn, values):

    titles_seen = set()

    for row in values:
        try:
            c = conn.cursor()

            if row['title'] in titles_seen:
                continue

            select = "SELECT genreID from genre where name ="+"'"+row['genre']+"'"
            c.execute(select)
            data = c.fetchall()
            genreID = data[0][0]

            insert = "INSERT INTO book(title, genreID) VALUES(" + "'" + row['title'] + "'" + "," + str(genreID) + ")"
            c.execute(insert)

            titles_seen.add(row['title'])

        except Error as e:
            print(e)


def insert_copies(conn, values):
    for row in values:
        try:
            c = conn.cursor()

            print("inserting: " + row['title'])

            select = "SELECT bookId from book where title ="+"'"+row['title']+"'"
            c.execute(select)
            data = c.fetchall()
            bookId = data[0][0]

            if row['sent'] != None:
                insert = "INSERT INTO copy(bookId, logged, sent) VALUES(" + "'" + str(bookId) + "'" \
                     + ", '" + row['logged'] + "','" + row['sent'] + "')"
            else:
                insert = "INSERT INTO copy(bookId, logged, sent) VALUES(" + "'" + str(bookId) + "'" \
                         + ", '" + row['logged'] + "',NULL)"
            c.execute(insert)

        except Error as e:
            print(e)



def import_library():
    conn = connect()

    try:
        values = read_library_csv('catalog.csv')
        #insert_books(conn, values)
        insert_copies(conn, values)

        conn.commit()

    except DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)

    disconnect(conn)



if __name__ == '__main__':
    import_library()
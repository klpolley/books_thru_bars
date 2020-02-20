import sys
from psycopg2 import Error, DatabaseError

from app.scripts.database.connect import connect, disconnect
from data_import.read_csv import read_prison_csv


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


def insert_authors(conn, values):

    books_done = set()
    authors_done = set()
    editors_done = set()

    for row in values:
        try:
            c = conn.cursor()

            if row['title'] in books_done: continue

            select = "SELECT bookID from book where title =" + "'" + row['title'] + "'"
            c.execute(select)

            data = c.fetchall()
            bookID = data[0][0]

            for author in row['authors']:

                if author not in authors_done:
                    insert = "INSERT INTO author(name) VALUES(" + "'" + author + "')"
                    c.execute(insert)
                    authors_done.add(author)

                select = "SELECT authorID from author where name =" + "'" + author + "'"
                c.execute(select)

                data = c.fetchall()
                authorID = data[0][0]

                join = "INSERT INTO written_by(bookid, authorid) VALUES("+ "'" + str(bookID) + "'," + "'" + str(authorID) + "')"
                c.execute(join)

            if 'editors' in row:
                for editor in row['editors']:
                    if editor not in editors_done:
                        insert = "INSERT INTO editor(name) VALUES(" + "'" + editor + "')"
                        c.execute(insert)
                        editors_done.add(editor)

                    select = "SELECT editorId from editor where name =" + "'" + editor + "'"
                    c.execute(select)

                    data = c.fetchall()
                    editorID = data[0][0]

                    join = "INSERT INTO edited_by VALUES("+ "'" + str(bookID) + "'," + "'" + str(editorID) + "')"
                    c.execute(join)

            books_done.add(row['title'])
            print(row['title'])

        except Error as e:
            print(e)


def import_facilities(conn, values):

    seen = set()

    for entry in values:
        try:
            c = conn.cursor()
            if entry['facility'] in seen:
                select = "SELECT facilityId FROM facility WHERE name = '"+entry['facility'] + "'"
                c.execute(select)
                data = c.fetchall()
                facilityId = data[0][0]
            else:
                state = "SELECT stateId FROM state WHERE abbreviation = '"+ entry['state'] + "'"
                c.execute(state)
                data = c.fetchall()
                stateId = data[0][0]
                insert = "INSERT INTO facility(name, address, city, zipcode, stateId) VALUES('"+entry['facility'] + \
                         "', '" + entry['address'] + "', '"+ entry['city'] + "', '" + entry['zipcode'] + \
                         "', " + str(stateId) + ") RETURNING facilityId"
                c.execute(insert)
                data = c.fetchall()
                facilityId = data[0][0]
                seen.add(entry['facility'])

            insert = "INSERT INTO package(facilityId, datesent) VALUES(" + str(facilityId) + ", '" + entry['date'] + "')"
            c.execute(insert)

        except Error as e:
            print(e)



def import_library():
    conn = connect()

    try:
        #values = read_library_csv('catalog.csv')
        #insert_books(conn, values)
        #insert_copies(conn, values)
        #insert_authors(conn, values)
        values = read_prison_csv('packages_confirmed.csv')
        import_facilities(conn, values)

        conn.commit()

    except DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)

    disconnect(conn)



if __name__ == '__main__':
    import_library()
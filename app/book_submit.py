from app.connect import connect, disconnect
from datetime import date

def submit(title, authors, editors, genre, quant):
    submit_book(title, authors, editors, genre, quant)

def submit_book(title, authors, editors, genre, quant):
    conn = connect()
    with conn.cursor() as cursor:
        s = "SELECT bookid FROM book WHERE title = %s"
        cursor.execute(s, [title])
        data = cursor.fetchall()

        if len(data) == 0:
            s = "SELECT genreid FROM genre WHERE name = %s"
            cursor.execute(s, [genre])
            gid = cursor.fetchall()[0][0]
            i = "INSERT INTO book(title, genreid, location) VALUES(%s, %s, 'SAC') RETURNING bookid";
            cursor.execute(i, [title, gid])
            id = cursor.fetchall()[0][0]

            for auth in authors:
                s = "SELECT authorid FROM author WHERE name = %s"
                cursor.execute(s, [auth])
                adata = cursor.fetchall()

                if len(adata) == 0:
                    i = "INSERT INTO author(name) VALUES(%s) RETURNING authorid"
                    cursor.execute(i, [auth])
                    aid = cursor.fetchall()[0][0]
                else:
                    aid = adata[0][0]

                i = "INSERT INTO written_by(bookid, authorid) VALUES(%s, %s)"
                cursor.execute(i, [id, aid])

            for edit in editors:
                s = "SELECT editorid FROM editor WHERE name = %s"
                cursor.execute(s, [edit])
                edata = cursor.fetchall()


                if len(edata) == 0:
                    i = "INSERT INTO editor(name) VALUES(%s) RETURNING editorid";
                    cursor.execute(i, [edit])
                    eid = cursor.fetchall()[0][0]
                else:
                    eid = edata[0][0]

                i = "INSERT INTO edited_by(bookid, editorid) VALUES(%s, %s)"
                cursor.execute(i, [id, eid])

        else:
            id = data[0][0]

        for i in range(int(quant)):
            i = "INSERT INTO copy(bookid, logged) VALUES(%s, %s)"
            cursor.execute(i, [id, date.today()])

        conn.commit()
        disconnect(conn)


def logout(copy):
    conn = connect()
    with conn.cursor() as cursor:
        s = "UPDATE copy SET sent = %s WHERE copyid = %s"
        cursor.execute(s, [date.today(), copy])

    conn.commit()
    disconnect(conn)



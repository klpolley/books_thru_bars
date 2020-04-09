from app.connect import connect
from datetime import date

def submit_book(title, authors, editors, genre, quant):
    with connect().cursor() as cursor:
        s = "SELECT bookid FROM book WHERE title = %s"
        cursor.execute(s, title)
        id = cursor.fetchall()[0][0]

        if id is None:
            s = "SELECT genreid FROM genre WHERE name = %s"
            cursor.execute(s, (genre))
            gid = cursor.fetchall[0][0]
            i = "INSERT INTO book(title, genreid, location) VALUES(%s, %s, 'SAC') RETURNING bookid";
            cursor.execute(i, (title, gid))
            id = cursor.fetchall()[0][0]

            for auth in authors:
                s = "SELECT authorid FROM author WHERE name = %s"
                cursor.execute(s, auth)
                aid = cursor.fetchall()[0][0]

                if aid is None:
                    i = "INSERT INTO author(name) VALUES(%s) RETURNING authorid";
                    cursor.execute(i, auth)
                    aid = cursor.fetchall()[0][0]

                i = "INSERT INTO written_by(bookid, authorid) VALUES(%s, %s)"
                cursor.execute(i, (id, aid))

            for edit in editors:
                s = "SELECT editorid FROM editor WHERE name = %s"
                cursor.execute(s, edit)
                eid = cursor.fetchall()[0][0]

                if eid is None:
                    i = "INSERT INTO editor(name) VALUES(%s) RETURNING editorid";
                    cursor.execute(i, edit)
                    eid = cursor.fetchall()[0][0]

                i = "INSERT INTO edited_by(bookid, editor) VALUES(%s, %s)"
                cursor.execute(i, (id, eid))

        for i in range(quant):
            i = "INSERT INTO copy(bookid, logged) VALUES(%s, %s)"
            cursor.execute(i, id, date.today())



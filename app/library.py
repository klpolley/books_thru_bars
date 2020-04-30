from app.connect import connect, disconnect
from app.book_retrieve import proper_case

def select_have():
    return "select copyid, book.title, author.name, " \
             "genre.name, copy.logged from copy " \
             "join book using(bookid) join genre using(genreid) " \
             "left join written_by using(bookid) " \
             "left join author using(authorid) " \
             "where copy.sent is null;"

def select_sent():
    return "select copyid, book.title, author.name, editor.name, " \
           "genre.name, copy.logged from copy " \
           "join book using(bookid) join genre using(genreid) " \
           "left join written_by using(bookid) " \
           "left join author using(authorid) " \
           "left join edited_by using (bookid) " \
           "left join editor using (editorid)" \
           "where copy.sent is not null;"

def get_books(sql):
    conn = connect()
    c = conn.cursor()

    select = sql
    c.execute(select)
    data = c.fetchall()

    books = {

    }
    for tuple in data:

        if tuple[0] in books.keys():
            if tuple[2] not in books[tuple[0]]['authors']:
                books[tuple[0]]['authors'].append(tuple[2])
            # if tuple[3] != '':
            #     books[tuple[0]]['editors'].append(tuple[3])

        else:

            d = {
                'title': proper_case(tuple[1]).replace("^", "'"),
                'authors': [tuple[2]],
                #'editors': [tuple[3]],
                'genre': tuple[3],
                'logged': tuple[4],
                'id': tuple[0]
            }
            d['logged'] = d['logged'].strftime("%m/%d/%Y")

            books[tuple[0]] = d

    disconnect(conn)

    books = books.values()

    for b in books:
        bauth = b['authors']
        authors = ''
        for a in bauth:
            authors += proper_case(a)
            if a != bauth[len(bauth) - 1]:
                authors += ", "
        b['authors'] = authors

        # bedit = b['editors']
        # editors = ''
        # if None not in b['editors']:
        #     for e in b['editors']:
        #         editors += proper_case(e)
        #         if e != bedit[len(bedit)-1]:
        #             editors += ", "
        # else:
        #     editors = 'N/A'
        #
        # b['editors'] = editors


    return books

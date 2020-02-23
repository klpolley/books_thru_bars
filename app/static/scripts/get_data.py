from app.static.scripts.database.connect import connect, disconnect

def retrieve_facilities():
    conn = connect()
    c = conn.cursor()

    select = "SELECT name, latitude, longitude FROM facility"
    c.execute(select)
    data = c.fetchall()

    facilities = []
    for tuple in data:
        dictionary = {
            'name': tuple[0],
            'latitude': tuple[1],
            'longitude': tuple[2]
        }
        facilities.append(dictionary)

    for f in facilities:
        f['name'] = f['name'].replace("^", "'")

    return facilities


def get_ithaca():
    conn = connect()
    c = conn.cursor()

    select = "SELECT latitude, longitude FROM ithaca"
    c.execute(select)
    data = c.fetchall()[0]

    coords = {
        'name': "Ithaca",
        'latitude': data[0],
        'longitude': data[1]
    }

    return coords


def retrieve_genres():
    conn = connect()
    c = conn.cursor()

    select_lib = "SELECT g.name AS genre, count(*) AS num FROM copy " \
                 "JOIN book b ON copy.bookid = b.bookid " \
                 "JOIN genre g ON b.genreid = g.genreid " \
                 "WHERE sent IS NULL " \
                 "GROUP BY g.name " \
                 "ORDER BY g.name"

    select_sent = "SELECT g.name AS genre, count(*) AS num FROM copy " \
                 "JOIN book b ON copy.bookid = b.bookid " \
                 "JOIN genre g ON b.genreid = g.genreid " \
                 "WHERE sent IS NOT NULL " \
                 "GROUP BY g.name " \
                 "ORDER BY g.name"

    c.execute(select_lib)
    data = c.fetchall()

    library = {}
    for row in data:
        library[row[0]] = row[1]

    c.execute(select_sent)
    data = c.fetchall()

    sent = {}
    for row in data:
        sent[row[0]] = row[1]

    return library, sent


def retrieve_mailings():
    conn = connect()
    c = conn.cursor()

    select = "SELECT sent, count(*) FROM copy WHERE sent IS NOT NULL GROUP BY sent;"
    c.execute(select)
    data = c.fetchall()

    mailings = {}
    for row in data:
        mailings[str(row[0])] = row[1]

    return mailings
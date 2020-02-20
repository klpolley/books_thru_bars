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
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


if __name__ == '__main__':
    retrieve_facilities()
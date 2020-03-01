from app.connect import connect, disconnect
import json


def proper_case(string):
    words = string.split(' ')
    result = ''
    for word in words:
        word = word.lower()
        if word in ['ii', 'iii']:
            word = word.upper()
        else:
            word = word.capitalize()
        result += word + ' '

    result = result.strip()
    return result


def get_titles(query):
    result = []
    try:
        with connect().cursor() as cursor:
            q = query.replace("'", "^")
            print(query)
            sql = "select title from book where title like UPPER('%" + q + "%')"
            cursor.execute(sql)
            data = cursor.fetchall()
    finally:
        for t in data:
            result.append(proper_case(t[0].replace("^", "'")))


    return json.dumps({"suggestions": result})
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
            sql = "select title from book where title like UPPER('%" + q + "%')"
            cursor.execute(sql)
            data = cursor.fetchall()
    finally:
        for t in data:
            result.append(proper_case(t[0].replace("^", "'")))


    return json.dumps({"suggestions": result})

def get_all_titles():
    result = []
    try:
        with connect().cursor() as cursor:
            sql = "select title from book"
            cursor.execute(sql)
            data = cursor.fetchall()
    finally:
        for t in data:
            result.append(proper_case(t[0].replace("^", "'")))

    return json.dumps(result)

def get_all_authors():
    result = []
    try:
        with connect().cursor() as cursor:
            sql = "select name from author where name not like 'VARIOUS' and name not like 'N/A'"
            cursor.execute(sql)
            data = cursor.fetchall()
    finally:
        for t in data:
            result.append(proper_case(t[0].replace("^", "'")))

    return json.dumps(result)

def get_all_editors():
    result = []
    try:
        with connect().cursor() as cursor:
            sql = "select name from editor"
            cursor.execute(sql)
            data = cursor.fetchall()
    finally:
        for t in data:
            result.append(proper_case(t[0].replace("^", "'")))

    return json.dumps(result)

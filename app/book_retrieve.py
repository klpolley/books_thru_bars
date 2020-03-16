from app.connect import connect, disconnect
import json
import re

def proper_case(string):
    #words = re.split(r"[\s/-]", string)
    words = string.split(' ')
    result = ''
    for word in words:
        word = word.lower()
        if word in ['ii', 'iii', 'lgbt']:
            word = word.upper()
        else:
            word = word.capitalize()

        idx = word.find('/')
        if idx != -1:
            word = word[0:idx+1] + word[idx+1].upper() + word[idx+2: len(word)]

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
            sql = "select title from book order by title asc"
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
            sql = "select name from author where name not like 'VARIOUS' and name not like 'N/A' order by name asc"
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
            sql = "select name from editor where name not like 'VARIOUS' order by name asc"
            cursor.execute(sql)
            data = cursor.fetchall()
    finally:
        for t in data:
            result.append(proper_case(t[0].replace("^", "'")))

    return json.dumps(result)

def get_genres():
    result = {}
    try:
        with connect().cursor() as cursor:
            sql = "select name, color, label from genre order by name asc"
            cursor.execute(sql)
            data = cursor.fetchall()
    finally:
        for t in data:
            result[t[0]] = [proper_case(t[1]), proper_case(t[2])]

    return json.dumps(result)
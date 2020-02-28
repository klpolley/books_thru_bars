import csv
from datetime import datetime

def read_library_csv(file_name):
    with open(file_name) as currentcsv:

        readcsv = csv.reader(currentcsv, delimiter=',')
        # 0 - title, 1 - author, 2 - editor, 3 - genre, 4 - date in, 5 - date out

        entries = []

        for row in readcsv:

            values = {}

            values['title'] = row[0].replace("'", "^").strip()

            author_string = row[1].replace("'", "^")
            author_list = author_string.split(',')
            for i in range(len(author_list)):
                author_list[i] = author_list[i].strip()
            values['authors'] = author_list

            if (row[2] != ''):
                editor_string = row[2].replace("'", "^")
                editor_list = editor_string.split(',')
                for i in range(len(editor_list)):
                    editor_list[i] = editor_list[i].strip()
                values['editors'] = editor_list

            values['genre'] = row[3].strip()

            values['logged'] = datetime.strptime(row[4], '%m/%d/%y').strftime("%Y-%m-%d")
            if row[5] != '':
                values['sent'] = datetime.strptime(row[5], '%m/%d/%y').strftime("%Y-%m-%d")
            else:
                values['sent'] = None

            entries.append(values)


        return entries

def read_prison_csv(file_name):
    with open(file_name) as currentcsv:
        readcsv = csv.reader(currentcsv, delimiter=',')
        # 0 - date, 1 - facility name, 2 - address, 3 - city, 4 - zip code, 5 - state abbr, 6 - state

        entries = []

        for row in readcsv:

            if row[0] == '\ufeffdate': continue

            values = {}

            values['date'] = datetime.strptime(row[0], '%m/%d/%y').strftime("%Y-%m-%d")
            values['facility'] = row[1].strip().upper()
            values['address'] = row[2].strip().upper()
            values['city'] = row[3].strip().upper()
            values['zipcode'] = row[4].strip()
            values['state'] = row[5].strip().upper()

            entries.append(values)

        return entries
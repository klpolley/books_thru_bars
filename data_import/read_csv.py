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

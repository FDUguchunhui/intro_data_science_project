import sqlite3
import os
import pandas as pd


def data_func(csv_f):
    db_fname = csv_f.replace('.csv', '.db')
    table_name = os.path.basename(csv_f).split('.')[0].lower()

    conn = sqlite3.connect(db_fname)
    cursor = conn.cursor()

    check = """SELECT name FROM sqlite_master WHERE type='table' AND name=?"""
    cursor.execute(check, (table_name,))
    if bool(cursor.fetchone()):
        cursor.execute('DROP TABLE ' + table_name)

    df = pd.read_csv(csv_f, index_col=0)

    df = pd.read_csv(csv_f, index_col=0)

    # create sql table
    df.to_sql(table_name, conn)


    author = input('Author name: ')

    query = "SELECT * FROM {0} where FAU like \'%{1}%\';".format(table_name, author)
    results = []
    for row in cursor.execute(query):
        # print(row)
        results.append(row)

    return results


if __name__ == '__main__':
    results = data_func(csv_f='HIV.csv')
    print(results)

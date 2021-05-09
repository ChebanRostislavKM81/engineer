import webbrowser
import os
import psycopg2
import time
import datetime
import json
import re
import dotenv

dotenv.load_dotenv()


def main():
    dbname = os.environ.get("dbname")
    user = os.environ.get("user")
    password = os.environ.get("password")
    conn = psycopg2.connect("dbname='" + dbname + "' user='" + user + "' password='" + password + "'")

    cursor = conn.cursor()

    download_path = os.environ.get("download_path")

    download_files_list_path = download_path + 'files_list.data'
    if os.path.exists(download_files_list_path):
        os.remove(download_files_list_path)

    webbrowser.open('http://data-engineering-interns.macpaw.io.s3.amazonaws.com/files_list.data')

    while not os.path.exists(download_files_list_path):
        time.sleep(1)

    with open(download_files_list_path) as file:
        files_list = file.read()
    pythonlist_of_files = files_list.strip('\n').split('\n')

    processed_file_table = "CREATE TABLE IF NOT EXISTS ProcessedFile(filename varchar);"
    cursor.execute(processed_file_table)
    conn.commit()

    song_table = """CREATE TABLE IF NOT EXISTS Song(
    artist_name varchar,
    title varchar,
    year int,
    release varchar,
    ingestion_time timestamp);"""
    cursor.execute(song_table)
    conn.commit()

    movie_table = """CREATE TABLE IF NOT EXISTS Movie(
    original_title varchar,
    original_language varchar,
    budget int,
    is_adult boolean,
    release_date date,
    original_title_normalized varchar);"""
    cursor.execute(movie_table)
    conn.commit()

    app_table = """CREATE TABLE IF NOT EXISTS App(
    name	varchar,
    genre	varchar,
    rating	float,
    version	varchar,
    size_bytes	bigint,
    is_awesome	boolean);"""
    cursor.execute(app_table)
    conn.commit()

    select = 'select * from ProcessedFile'
    cursor.execute(select)
    select_processed_files = cursor.fetchall()
    processed_file_list = []
    for i in select_processed_files:
        processed_file_list.append(list(i)[0])
    todo_list = []
    for i in pythonlist_of_files:
        if not (i in processed_file_list):
            todo_list.append(i)
    for todo_file in todo_list:
        string_to_download = 'http://data-engineering-interns.macpaw.io.s3.amazonaws.com/' + todo_file
        webbrowser.open(string_to_download)
        download_file_path = download_path + todo_file
        while not os.path.exists(download_file_path):
            time.sleep(1)

        download_file_path = open(download_file_path)
        file_open = json.load(download_file_path)
        for i in file_open:
            if i['type'] == 'app':

                if i['data']['rating'] >= 4.0:
                    is_awesome = True
                else:
                    is_awesome = False
                name = i['data']['name'].replace("'", "`")
                query = f"INSERT INTO App(name, genre, rating, version, size_bytes, is_awesome) VALUES ('" + str(
                    name) + "','" + str(i['data']['genre']) + "','" + str(i['data']['rating']) + "','" + str(
                    i['data']['version']) + "','" + str(i['data']['size_bytes']) + "','" + str(is_awesome) + "')"
                cursor.execute(query)

            elif i['type'] == 'song':
                now = datetime.datetime.now()
                artist_name = i['data']['artist_name'].replace("'", "`")
                title = i['data']['title'].replace("'", "`")
                release = i['data']['release'].replace("'", "`")
                query = f"INSERT INTO Song(artist_name, title, year, release, ingestion_time) VALUES ('" + str(
                    artist_name) + "','" + str(title) + "','" + str(i['data']['year']) + "','" + str(
                    release) + "','" + str(
                    now) + "')"
                cursor.execute(query)

            elif i['type'] == 'movie':
                low = i['data']['original_title'].lower().split(' ')

                final_list = []
                for jj in low:
                    f_n = re.sub('[^a-z0-9]', '', jj)

                    final_list.append(f_n)

                original_title_normalized = '_'.join(final_list)

                original_title = i['data']['original_title'].replace("'", "`")
                original_language = i['data']['original_language'].replace("'", "`")
                query = f"INSERT INTO Movie(original_title, original_language, budget, is_adult, release_date, original_title_normalized) VALUES ('" + str(
                    original_title) + "','" + str(original_language) + "','" + str(i['data']['budget']) + "','" + str(
                    i['data']['is_adult']) + "','" + str(i['data']['release_date']) + "','" + str(
                    original_title_normalized) + "')"
                cursor.execute(query)
        conn.commit()
        query = f"INSERT INTO ProcessedFile(filename) VALUES('" + todo_file + "')"
        cursor.execute(query)
        conn.commit()


if __name__ == '__main__':
    main()

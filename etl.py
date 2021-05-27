import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    - It reads a song JSON file and transform on a Pandas DataFrame;
    - Selects the specifics columns related to Artist and Songs;
    - Inserts data into Artist and Songs tables;
    """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values.tolist()[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = artist_data = df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values.tolist()[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    - Load a log JSON file and transform on a Pandas Dataframe;
    - Filter dataframe where page is equal to 'NextSong';
    - Convert 'ts' (timestamp) to 'datetime' format;
    - Insert data into Time, User and Songplay tables
    """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ("start_time", 'hour', 'day', 'weekofyear', 'month', 'year', 'weekday')

    dict_time = dict(zip(column_labels, time_data))
    time_df = pd.DataFrame(dict_time)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    - Searches for files within the directories;
    - Calls specific functions for each file type (log and song data);
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Connects to Postgres database;
    - Creates a cursor;
    - Start the functions for each file type;
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    song_files_path = os.path.join("./", "data", "song_data")
    process_data(cur, conn, filepath=song_files_path, func=process_song_file)

    log_files_path = os.path.join("./", "data", "log_data")
    process_data(cur, conn, filepath=log_files_path, func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
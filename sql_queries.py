# DROP TABLES

songplay_table_drop = ""
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id VARCHAR PRIMARY KEY,
        first_name varchar,
        last_name varchar,
        gender char,
        level varchar
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id VARCHAR PRIMARY KEY, 
        title VARCHAR,
        artist_id VARCHAR, 
        year int, 
        duration NUMERIC
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR PRIMARY KEY, 
        artist_name VARCHAR, 
        artist_location VARCHAR,
        artist_latitude NUMERIC,
        artist_longitude NUMERIC
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        timestamp timestamp, 
        hour int, 
        day int,
        weekofyear int,
        month int,
        year int,
        weekday int
    )
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
    INSERT INTO users ( user_id, first_name, last_name, gender, level )
    VALUES (  %s, %s, %s, %s, %s )
    ON CONFLICT DO NOTHING;
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    VALUES ( %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, artist_name, artist_location, artist_latitude, artist_longitude)
    VALUES (  %s, %s, %s, %s, %s )
    ON CONFLICT DO NOTHING;
""")


time_table_insert = ("""
    INSERT INTO time (timestamp, hour, day, weekofyear, month, year, weekday)
    VALUES ( %s, %s, %s, %s, %s, %s, %s )
    ON CONFLICT DO NOTHING;
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
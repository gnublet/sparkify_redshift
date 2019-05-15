import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS times"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS
staging_events
(
    artist VARCHAR,
    auth VARCHAR,
    firstName VARCHAR,
    gender VARCHAR,
    itemInSession VARCHAR,
    lastName VARCHAR,
    length VARCHAR,
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration VARCHAR,
    sessionId VARCHAR,
    song VARCHAR,
    status VARCHAR,
    ts VARCHAR,
    userAgent VARCHAR,
    userId VARCHAR
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS 
staging_songs
(
    artist_id VARCHAR,
    artist_latitude VARCHAR,
    artist_location VARCHAR,
    artist_longitude VARCHAR,
    artist_name VARCHAR,
    duration DECIMAL,
    num_songs INTEGER,
    song_id VARCHAR,
    title VARCHAR,
    year INTEGER
)
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS 
songplays
(
    songplay_id SERIAL PRIMARY KEY, 
    start_time TIMESTAMP REFERENCES times(start_time), 
    user_id INT REFERENCES users(user_id), 
    level VARCHAR NOT NULL, 
    song_id VARCHAR REFERENCES songs(song_id), 
    artist_id VARCHAR REFERENCES artists(artist_id), 
    session_id INT NOT NULL, 
    location VARCHAR NOT NULL, 
    user_agent VARCHAR NOT NULL
)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS 
users
(
    user_id INT PRIMARY KEY, 
    first_name VARCHAR NOT NULL, 
    last_name VARCHAR NOT NULL, 
    gender VARCHAR NOT NULL, 
    level VARCHAR NOT NULL
)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS
songs
(
    song_id VARCHAR PRIMARY KEY, 
    title VARCHAR NOT NULL, 
    artist_id VARCHAR NOT NULL, 
    year INT NOT NULL, 
    duration NUMERIC(9,5) NOT NULL CHECK(duration >= 0)
)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS
artists
(
    artist_id VARCHAR PRIMARY KEY, 
    name VARCHAR NOT NULL, 
    location VARCHAR NOT NULL, 
    latitude NUMERIC(9,5) NOT NULL CHECK(latitude >= 0 AND latitude <= 90), 
    longitude NUMERIC(9,5) NOT NULL CHECK(longitude >= -180 AND longitude <= 180)
)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS 
times
(
    start_time TIMESTAMP PRIMARY KEY, 
    hour INT NOT NULL CHECK(hour >= 0), 
    day INT NOT NULL CHECK(day >= 0), 
    week INT NOT NULL CHECK(week >= 0), 
    month INT NOT NULL CHECK(month >= 0), 
    year INT NOT NULL, 
    weekday INT NOT NULL CHECK(weekday >= 0)
)
""")

# STAGING TABLES
staging_events_copy = ("""
copy staging_events
from '{}'
iam_role '{}'
region 'us-west-2';
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'])

staging_songs_copy = ("""
copy staging_songs
from '{}'
iam_role '{}'
region 'us-west-2';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO 
songplays 
(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
VALUES 
(%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
-- (user_id)
-- DO UPDATE
-- SET level=EXCLUDED.level, location=EXCLUDED.location, user_agent=EXCLUDED.user_agent
""")

user_table_insert = ("""
INSERT INTO
users
(user_id, first_name, last_name, gender, level)
VALUES
(%s, %s, %s, %s, %s)
ON CONFLICT (user_id)
DO UPDATE
SET level=EXCLUDED.level, first_name=EXCLUDED.first_name, last_name=EXCLUDED.last_name, gender=EXCLUDED.gender
""")

song_table_insert = ("""
INSERT INTO
songs
(song_id, title, artist_id, year, duration)
VALUES
(%s, %s, %s, %s, %s)
ON CONFLICT (song_id)
DO UPDATE
SET title=EXCLUDED.title, artist_id=EXCLUDED.artist_id, year=EXCLUDED.year, duration=EXCLUDED.duration
""")

artist_table_insert = ("""
INSERT INTO 
artists
(artist_id, name, location, latitude, longitude)
VALUES
(%s, %s, %s, %s, %s)
ON CONFLICT (artist_id)
DO UPDATE
SET name=EXCLUDED.name, location=EXCLUDED.location, latitude=EXCLUDED.latitude, longitude=EXCLUDED.longitude
""")

time_table_insert = ("""
INSERT INTO 
times
(start_time, hour, day, week, month, year, weekday)
VALUES
(%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

from dotenv import load_dotenv

import os
import psycopg2.pool
import psycopg2.extras

load_dotenv()

pool = psycopg2.pool.SimpleConnectionPool(
    minconn=2,
    maxconn=10,
    database=os.getenv("DB"),
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    port=os.getenv("DB_PORT"),
    password=os.getenv("DB_PASSWORD"),
)

def get_cursor():
    connection = pool.getconn()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return connection, cursor

def release_connection(connection):
    pool.putconn(connection)
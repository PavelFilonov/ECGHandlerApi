import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

configs = "host=localhost port=5432 user=postgres password=postgres"


def open_db():
    connection = psycopg2.connect(configs)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    return connection, cursor


def close_db(connection, cursor):
    cursor.close()
    connection.close()

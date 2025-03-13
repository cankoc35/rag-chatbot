from config import DATABASE_CONFIG
import psycopg2

db_connection = psycopg2.connect(**DATABASE_CONFIG)

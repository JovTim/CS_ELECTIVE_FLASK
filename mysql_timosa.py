from flask import Flask, jsonify, request
from http import HTTPStatus
import pymysql

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root", # placeholder, not my real password
    "database": "books_timosa",
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

def fetch_all_books():
    connection = get_db_connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM books")
            return cursor.fetchall()
    finally:
        connection.close()

def fetch_book_by_id(book_id):
    connection = get_db_connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
            return cursor.fetchone()
    finally:
        connection.close()
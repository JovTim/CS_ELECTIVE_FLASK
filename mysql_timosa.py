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

def insert_book(data):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)",
                (data["title"], data["author"], data["year"]),
            )
            connection.commit()
            return cursor.lastrowid
    finally:
        connection.close()

def update_book_in_db(book_id, data):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE books SET title = %s, author = %s, year = %s WHERE id = %s",
                (data["title"], data["author"], data["year"], book_id),
            )
            connection.commit()
            return cursor.rowcount > 0
    finally:
        connection.close()

def delete_book_from_db(book_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
            connection.commit()
            return cursor.rowcount > 0
    finally:
        connection.close()

@app.route("/api/books", methods=["GET"])
def get_books():
    books = fetch_all_books()
    return jsonify({"success": True, 
                    "data": books, 
                    "total": len(books)}), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = fetch_book_by_id(book_id)
    if book is None:
        return jsonify({"success": False, 
                        "error": "Book not found"}), HTTPStatus.NOT_FOUND
    
    return jsonify({"success": True, 
                    "data": book}), HTTPStatus.OK

@app.route("/api/books", methods=["POST"])
def create_book():
    if not request.is_json:
        return jsonify({"success": False, 
                        "error": "Content-type must be application/json"}), HTTPStatus.BAD_REQUEST

    data = request.get_json()
    required_fields = ["title", "author", "year"]
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, 
                            "error": f"Missing required field: {field}"}), HTTPStatus.BAD_REQUEST

    book_id = insert_book(data)
    new_book = fetch_book_by_id(book_id)
    return jsonify({"success": True, 
                    "data": new_book}), HTTPStatus.CREATED

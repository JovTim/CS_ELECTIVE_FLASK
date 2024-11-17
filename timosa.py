from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

books = [
    {
        "id": 1,
        "title":"The Great Gatsby",
        "author":"F. Scott Firzgerald",
        "year": 1925,
    },
    {"id": 2, "title":"1984","author":"George Orwell", "year": 1949},
]

def find_book(book_id):
    return next((book for book in books if book["id"] == book_id), None)

@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify({"success": True, "data": books,"total": len(books)}), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = find_book(book_id)
    if book is None:
        return(
            jsonify(
                {
                    "success": False,
                    "error": "Book not found",
                }
            ),
            HTTPStatus.NOT_FOUND,
        )
    return(
            jsonify(
                {
                    "success": True,
                    "data": book,
                }
            ),
            HTTPStatus.OK,
        )

@app.route("/api/books", methods=["POST"])
def create_book():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), HTTPStatus.BAD_REQUEST

    data = request.get_json()

    required_fields = ["title", "author", "year"]
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing required fields: {field}"
                }
            ), HTTPStatus.BAD_REQUEST
    
    new_book = {
        "id": max(book['id'] for book in books) + 1,
        "title": data['title'],
        "author": data['author'],
        "year" : data['year']
    }

    books.append(new_book)

    return jsonify(
        {
            "success": True,
            "data": new_book
        }
    ), HTTPStatus.CREATED


@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), HTTPStatus.BAD_REQUEST

    data = request.get_json()

    book = find_book(book_id)
    if book is None:
        return jsonify(
            {
                "success": False,
                "error": "Book not found"
            }
        ), HTTPStatus.NOT_FOUND

    book.update(
        {
            "title": data.get("title", book["title"]),
            "author": data.get("author", book["author"]),
            "year": data.get("year", book["year"]),
        }
    )

    return jsonify(
        {
            "success": True,
            "data": book
        }
    ), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books

    book = find_book(book_id)
    if book is None:
        return jsonify(
            {
                "success": False,
                "error": "Book not found"
            }
        ), HTTPStatus.NOT_FOUND

    books = [b for b in books if b["id"] != book_id]

    return jsonify(
        {
            "success": True,
            "message": "Book deleted successfully"
        }
    ), HTTPStatus.OK

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Resource not found"
    }
    ), HTTPStatus.NOT_FOUND

@app.errorhandler(500)
def internal_server(error):
    return jsonify(
        {
            "success": False,
            "error": "Internal Server Error"
        }
    ), HTTPStatus.INTERNAL_SERVER_ERROR
    

if __name__ == "__main__":
    app.run(debug=True)

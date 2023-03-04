from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from BookModel import *
import json
from settings import *



def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False



@app.route('/books')
def get_books():
    return jsonify({"books": Book.get_all_books()})



@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if (validBookObject(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response= Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in the request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 123456789}"
        }
        response = jsonify(invalidBookObjectErrorMsg)
        response.status_code = 400
        return response


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)

def valid_put_request_data(request_data):
    if ("name" in request_data and "price" in request_data):
        return True
    else:
        return False

#PUT

@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            "error": "Valid book object must be passed in the request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status=204)
    return response

#PATCH

@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    
    if ("name" in request_data):
        Book.update_book_name(isbn, request_data['name'])
    if ("price" in request_data):
        Book.update_book_price(isbn, request_data['price'])
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

#DELETE
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if(Book.delete_book(isbn)):
        response = Response("", status=204)
        return response
    invalidBookObjectErrorMsg = {
        "error": "Book with the ISBN number that was provided was not found, so therefore unable to delete"
    }
    response = jsonify(invalidBookObjectErrorMsg)
    response.status_code = 404
    return response

app.run(port=5000, debug=True)
from flask import Flask, jsonify, request

app= Flask(__name__)
print(__name__)

books = [
    {  
        "name": "Harry Potter",
        "price": 7.99,
        "isbn": 9781536831139
    },
    {
        "name": "Lord of the Rings",
        "price": 6.99,
        "isbn": 9781536831139
    }
]


def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False



@app.route('/books')
def hello_world():
    return jsonify({"books": books})



@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if (validBookObject(request_data)):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = jsonify(new_book)
        response.status_code = 201
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
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book['name'],
                'price': book['price']
            }
    return jsonify(return_value)

app.run(port=5000)
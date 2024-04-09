#Module 4 Lab - Case Study: Python APIs
#Created by Austin Stroud
#File name: module04lab.py 
#Description: CRUD API for a Book. 

#Import flask framework
from flask import Flask, request, jsonify
#Import SQLAlchemy for database management
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

#Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Book(id={self.id}, book_name={self.book_name}, author={self.author}, publisher={self.publisher})"

#Route to create new book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    new_book = Book(book_name=data['book_name'], author=data['author'], publisher=data['publisher'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'}), 201

#Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    output = [{'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher} for book in books]
    return jsonify({'books': output})

#Route to get specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher})

#Route to update book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.json
    book.book_name = data['book_name']
    book.author = data['author']
    book.publisher = data['publisher']
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

#Route to delete book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
    #Create database tables
    with app.app_context():
        db.create_all()
    #Run flask application
    app.run(debug=True)


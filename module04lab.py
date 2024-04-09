#Module 4 Lab - Case Study: Python APIs
#Created by Austin Stroud
#File name: module04lab.py 
#Description: CRUD API for a Book. 

#Import flask framework
from flask import Flask, request
#Import SQLAlchemy for database management
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  #Initialize Flask app

#Configure database URI (SQLite in this case)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)  #Initialize SQLAlchemy object with Flask app


class Book(db.Model):  #Define Book model
    id = db.Column(db.Integer, primary_key=True)  #Primary key column for unique identification
    book_name = db.Column(db.String(80), unique=True, nullable=False)  #Column for book name
    author = db.Column(db.String(80), nullable=False)  #Column for author name
    publisher = db.Column(db.String(120))  #Column for publisher name

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"


@app.route('/')  #Define route for homepage
def index():
    return 'Hello!'  #Return simple greeting


@app.route('/books')  #Define route to get all books
def get_books():
    books = Book.query.all()  #Query all books from database
    output = []  #Initialize an empty list to store book data
    for book in books:
        book_data = {'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}  #Extract book data
        output.append(book_data)  #Append book data to output list
    return {"books": output}  #Return a JSON object containing all books


@app.route('/books/<id>')  #Define route to get specific book by ID
def get_book(id):
    book = Book.query.get_or_404(id)  #Query book by its ID or return a 404 error if not found
    return {"book_name": book.book_name, "author": book.author, "publisher": book.publisher}  # Return book data


@app.route('/books', methods=['POST'])  #Define route to add a new book
def add_book():
    book = Book(book_name=request.json['book_name'],  #Extract book details from request JSON
                author=request.json['author'],
                publisher=request.json['publisher'])
    db.session.add(book)  #Add new book to database session
    db.session.commit()  #Commit changes to database
    return {'id': book.id}  #Return ID of newly added book


@app.route('/books/<id>', methods=['DELETE'])  #Define route to delete a book by its ID
def delete_book(id):
    book = Book.query.get(id)  #Query book by its ID
    if book is None:  #If book is not found
        return {"error": "not found"}  #Return an error message
    db.session.delete(book)  #Delete book from the database session
    db.session.commit()  #Commit changes to the database
    return {"message": "Book deleted successfully"}  #Return success message


from flask import Flask, render_template, request, redirect, url_for
from models import db, Book, Category, BorrowHistory
from datetime import datetime
import os
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def initialize_database():
    if not os.path.exists('library.db'):
        conn = sqlite3.connect('library.db')
        with open('init_db.sql', 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

@app.before_first_request
def setup():
    initialize_database()
    db.create_all()

@app.route('/')
def index():
    books = Book.query.all()
    categories = Category.query.all()
    return render_template('index.html', books=books, categories=categories)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        results = Book.query.filter(Book.title.contains(search_term) | Book.author.contains(search_term)).all()
        return render_template('search.html', results=results)
    return render_template('search.html', results=None)

@app.route('/history')
def history():
    borrow_history = BorrowHistory.query.all()
    return render_template('history.html', borrow_history=borrow_history)

@app.route('/borrow/<int:book_id>')
def borrow(book_id):
    book = Book.query.get(book_id)
    if book and not book.is_borrowed:
        book.is_borrowed = True
        borrow_entry = BorrowHistory(book_id=book_id, borrow_date=datetime.now())
        db.session.add(borrow_entry)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/return/<int:book_id>')
def return_book(book_id):
    book = Book.query.get(book_id)
    if book and book.is_borrowed:
        book.is_borrowed = False
        borrow_entry = BorrowHistory.query.filter_by(book_id=book_id, return_date=None).first()
        if borrow_entry:
            borrow_entry.return_date = datetime.now()
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

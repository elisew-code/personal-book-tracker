from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # creating Flask app object - routes, frontend, responses
# "use an SQLite database called books in the current directory"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
# initialises the connection, creates a db object, to run queries, define models, etc.
db = SQLAlchemy(app) # SQLAlchemy interface - querying and storing data

# routes handle web requests i.e., a user clicks
# e.g. showing all books in the database
@app.route('/')
def index():
    books = Book.query.all()  # Get all books from the database
    return render_template('index.html', books=books)  # Show the list on the webpage

# e.g. where a user adds a book
@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']   # Get the ‘title’ input from the form
    author = request.form['author'] # Get the ‘author’ input
    # Create a new Book object with this data
    new_book = Book(title=title, author=author)
    db.session.add(new_book)         # Add to the database session
    db.session.commit()              # Save changes to the database
    return redirect(url_for('index'))  # Redirect back to homepage to see updated list

# the route using example helper function
@app.route('/stats')
def stats():
    genre_counts = count_books_by_genre()
    return render_template('stats.html', data=genre_counts)
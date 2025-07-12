import os

PROJECT_ROOT_DIR = os.path.dirname(__file__) 
DATA_PATH = os.path.join(PROJECT_ROOT_DIR, 'data')
BOOK_DATA_PATH = os.path.join(DATA_PATH, 'books')
LIBRARY_DATA_PATH = os.path.join(DATA_PATH, 'libraries')

VALID_SCHEMA_COLUMNS = valid_columns = ['title', 'synopsis', 'author', 'isbn', 'genre', 'bookstore', 'review', 'rating', 'price', 'publisher', 'publication year']
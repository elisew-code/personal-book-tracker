-- sqlite3 books.db < schema.sql to create the db
-- will delete existing data if schema.sql has DROP TABLE

-- new table - book information (i.e., metadata)
DROP TABLE IF EXISTS book_metadata;
CREATE TABLE book_metadata (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT CHECK(status IN ('To Read', 'Reading', 'Completed', 'Abandoned')),       
    start_date TEXT,     -- Store as ISO string: "2024-07-07" (quality checks here?)
    end_date TEXT,
    banned TEXT CHECK(banned IN ('Yes', 'No')),
    bookstore_name TEXT, -- make this drop down, add existing options? or closest option functionality?
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (bookstore_name) REFERENCES bookstore(name)
);

DROP TABLE IF EXISTS books;
CREATE TABLE book (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title TEXT NOT NULL, 
    synopsis TEXT, 
    author TEXT,
    publisher TEXT,
    publication_year TEXT, -- BC? int? check? keep 
    isbn TEXT UNIQUE,
    genre_id INTEGER, 
);

DROP TABLE IF EXISTS reviews;
CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    book_id INTEGER NOT NULL,
    review TEXT,
    rating INTEGER CHECK(rating BETWEEN 0 AND 5),
    FOREIGN KEY book_id REFERENCES books(book_id)
);

DROP TABLE IF EXISTS budget;
CREATE TABLE purchases (
    purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    price REAL, -- REAL an SQLite type
    amount_spent REAL, 
    remaining_budget FLOAT CHECK(remaining_budget >= 0),
    FOREIGN KEY book_id REFERENCES books(book_id)
);

DROP TABLE IF EXISTS bookstore;
CREATE TABLE bookstore (
    name TEXT PRIMARY KEY,
    address TEXT
);

-- can also preload common genres, like insert values/use a csv to insert values
DROP TABLE IF EXISTS genres;
CREATE TABLE genres (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- book-genre linking table: to implement many to many between books and genres
DROP TABLE IF EXISTS book_genres;
CREATE TABLE book_genres (
    book_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (book_id, genre_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);
# logic/helper functions, can be called in routes e.g.,
def count_books_by_genre():
    genres = db.session.query(Book.genre, db.func.count(Book.genre)).group_by(Book.genre).all()
    return genres


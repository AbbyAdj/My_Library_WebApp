from sqlalchemy import insert
from ...models.models import Authors, Books, Genres, BooksAndGenres
from .... import db
from pprint import pprint

# BOOKS

def get_all_books():
    all_books = db.session.execute(db.select(Books).order_by(Books.book_id)).scalars().all()
    return all_books

def get_completed_books():
    completed_books = db.session.execute(db.select(Books).where(Books.completed == True)).scalars().all()
    return completed_books

def get_ongoing_books():
    ongoing_books = db.session.execute(db.select(Books).where(Books.completed == False)).scalars().all()
    return ongoing_books

def get_disliked_books():
    disliked_books = db.session.execute(db.select(Books).where(Books.given_up == True)).scalars().all()
    return disliked_books

# AUTHORS

def get_all_authors():
    all_authors = db.session.execute(db.select(Authors).order_by(Authors.author_id)).scalars().all()
    return all_authors

# GENRES

def get_all_genres():
    all_genres = db.session.execute(db.select(Genres).order_by(Genres.genre_id)).scalars().all()
    return all_genres







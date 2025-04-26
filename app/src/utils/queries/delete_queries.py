from sqlalchemy import insert
from ...models.models import Authors, Books, Genres, BooksAndGenres
from .... import db


def delete_book(book_id):
    """Takes the book id as an argument to delete from the database"""
    book_to_delete = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
from sqlalchemy import insert
from ...models.models import Authors, Books, Genres, BooksAndGenres
from .... import db

def edit_book(book_id, new_data: dict):
    book_to_edit = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    for field in new_data:
        setattr(book_to_edit, field, new_data[field])
    db.session.commit()

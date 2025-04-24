from .models import Books
from . import db

def get_all_books():
    all_books = db.session.execute(db.select(Books).order_by(Books.id)).scalars().all()
    return all_books

def get_completed_books():
    completed_books = db.session.execute(db.select(Books).where(Books.completed == 1)).scalars().all()
    return completed_books

def get_ongoing_books():
    # Completed column = False, 0
    ongoing_books = db.session.execute(db.select(Books).where(Books.completed == False)).scalars().all()
    return ongoing_books

def get_disliked_books():
    # Given_up column = True
    disliked_books = db.session.execute(db.select(Books).where(Books.given_up == True)).scalars().all()
    return disliked_books

def add_new_book(book_fields: dict, user_added=False):
    # Not all fields are added as some are not available with the google books api. These can be added by the user.
    if user_added:
        new_book = Books()
        for field in book_fields.keys():
            setattr(new_book, field, book_fields[field])
    else:
        title = book_fields["title"]
        author = book_fields["author"]
        isbn = book_fields["isbn"]
        number_of_pages = book_fields["number_of_pages"]
        cover_image = book_fields["cover_image"]
        synopsis = book_fields["synopsis"]
        new_book = Books(
            title = title,
            author = author,
            isbn = isbn,
            number_of_pages = number_of_pages,
            cover_image = cover_image,
            synopsis = synopsis
        )
    db.session.add(new_book)
    db.session.commit()
    new_book_id = new_book.id
    return new_book_id

def delete_book(book_id):
    """Takes the book id as an argument to delete from the database"""
    book_to_delete = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()

def edit_book(book_id, new_data: dict):
    book_to_edit = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    for field in new_data:
        setattr(book_to_edit, field, new_data[field])
    db.session.commit()
from sqlalchemy import insert
from ...models.models import Authors, Books, Genres, BooksAndGenres
from .... import db
from .get_queries import *

# BOOKS AND GENRES 
        
def add_new_books_and_genres(**books_and_genres_fields):
        new_book_and_genre = BooksAndGenres(book_id = books_and_genres_fields["book_id"],
                                   genre_id = books_and_genres_fields["genre_id"])

        db.session.add(new_book_and_genre)
        db.session.commit()
        
# BOOKS

def add_new_book(book_fields: dict, user_added=False):
    # Not all fields are added as some are not available with the google books api. These can be added by the user.
    if user_added:
        book_fields.pop("submit")
        book_fields.pop("cancel")
        book_fields.pop("csrf_token")

        author_id = add_new_author(author_name = book_fields.pop("author_name"))
        book_fields.update(author_id = author_id)

        genre_id = add_new_genre(genre_name = book_fields.pop("genre_name"))

        new_book = Books()
        for field in book_fields:
            if field in dir(new_book):
                setattr(new_book, field, book_fields[field]) 
        
        db.session.add(new_book)
        db.session.commit()
        new_book_id = new_book.book_id

        add_new_books_and_genres(book_id=new_book_id, genre_id=genre_id)

    else:
        pass
        # TODO COmmented out for a reason, refactor/rewrite
    #     title = book_fields["title"]
    #     author = book_fields["author"]
    #     isbn = book_fields["isbn"]
    #     number_of_pages = book_fields["number_of_pages"]
    #     cover_image = book_fields["cover_image"]
    #     synopsis = book_fields["synopsis"]
    #     new_book = Books(
    #         title = title,
    #         author = author,
    #         isbn = isbn,
    #         number_of_pages = number_of_pages,
    #         cover_image = cover_image,
    #         synopsis = synopsis
    #     )
    # db.session.add(new_book)
    # db.session.commit()
    # new_book_id = new_book.id
    return new_book_id


# AUTHORS 


def add_new_author(**author_fields):
        new_author = Authors(author_name = author_fields["author_name"])

        all_authors = get_all_authors()
        for author in all_authors:
            if new_author.author_name == author.author_name:
                return author.author_id
        else:    
            db.session.add(new_author)
            db.session.commit()
            return new_author.author_id
        
# GENRES

def add_new_genre(**genre_fields):
        new_genre = Genres(genre_name = genre_fields["genre_name"])

        all_genres = get_all_genres()
        for genre in all_genres:
            if new_genre.genre_name == genre.genre_name:
                return genre.genre_id
        else:    
            db.session.add(new_genre)
            db.session.commit()
            return new_genre.genre_id
        


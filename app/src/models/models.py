from ... import db


    
class Authors(db.Model):
    __tablename__ = "authors"
    author_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.Integer)
    # Foreign key relationships
    books = db.relationship("Books", backref="author")

    def __str__(self):
        return f"<{self.id}: {self.author_name}>"

class Books(db.Model):
    __tablename__ = "books"
    # CHANGE TO BOOK_ID INSTEAD OF ID
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.author_id"), nullable=False)
    synopsis = db.Column(db.Text, nullable=True)
    number_of_pages = db.Column(db.Integer, nullable=True)
    isbn = db.Column(db.String, nullable=True)
    completed = db.Column(db.Boolean, nullable=True)
    given_up = db.Column(db.Boolean, nullable=True)
    year_finished = db.Column(db.String, nullable=True)  #Can be left null if book hasn't been completed
    rating = db.Column(db.Float, nullable=True)  #out of 5 stars
    personal_notes = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.Text, nullable=True)
    # Foreign key relationships
    book_genres = db.relationship("BooksAndGenres", backref="book")
    # TODO This part is left blank on purpose. Add later the book series column, that is, if the book is part of a series.
    

    def __str__(self):
        return f"<{self.id}: {self.title} written by {self.author}>"

    
class Genres(db.Model):
    __tablename__ = "genres"
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String, nullable=True)
    book_genres = db.relationship("BooksAndGenres", backref="genre")

    def __str__(self):
        return f"<{self.id}: {self.genre_name}>"


class BooksAndGenres(db.Model):
    __tablename__ = "books_and_genres"
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.genre_id"), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint(
            book_id, genre_id
        ),
    )



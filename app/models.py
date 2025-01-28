from . import db


# TODO: Create different tables for the multiple authors and genres

class Books(db.Model):
    __tablename__ = "MyBooks"
    # CHANGE TO BOOK_ID INSTEAD OF ID
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, nullable=True)
    genre = db.Column(db.String, nullable=True)  # you might need to create a separate table for this later on
    completed = db.Column(db.String, nullable=True)
    given_up = db.Column(db.Boolean, nullable=True)
    year_finished = db.Column(db.String, nullable=True)  #Can be left null if book hasn't been completed
    rating = db.Column(db.Float, nullable=True)  #out of 5 stars
    number_of_pages = db.Column(db.Integer, nullable=True)
    # This part is left blank on purpose. Add later the book series column, that is, if the book is part of a series.
    cover_image = db.Column(db.Text, nullable=True)
    synopsis = db.Column(db.Text, nullable=True)
    personal_notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<{self.id}: {self.title} written by {self.author}>"

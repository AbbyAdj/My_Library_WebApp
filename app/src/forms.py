from wsgiref.validate import validator

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

# FORMS CREATION
# TODO: Create separate table for books with multiple authors. Books with single authors must be used for now.
# TODO: Use single genres for now, multiple genres will be added and referenced using another table
# TODO: Change genre to a drop down select

class EditBookForm(FlaskForm):
    title = StringField("What is the book title?", validators=[DataRequired()])
    author = StringField("Who wrote the book?", description="Who wrote the book?", validators=[DataRequired()])
    synopsis = StringField("What is this book about?")
    number_of_pages = IntegerField("How many pages are in the book?", default=0)
    genre = StringField("What is the book Genre (Only type the main genre)")
    isbn = StringField("What is the ISBN number?")
    completed = BooleanField("Are you done with the book?")
    given_up = BooleanField("Do you actually plan on completing this book?")
    year_finished = StringField("What year did you finish the book?")
    rating = FloatField("What is your rating?", default=0)
    personal_notes = StringField("Let out all your thoughts below......")
    cover_image = StringField("Enter the image url", default="https://picsum.photos/200")

    submit = SubmitField("Submit Changes")
    cancel = SubmitField("Cancel")

class AddNewBookForm(FlaskForm):
    title = StringField("Book Title", validators=[DataRequired()])
    author = StringField("Author Name")

    api_add = SubmitField("Add Book")
    cancel = SubmitField("Cancel")
    user_add = SubmitField("Click Here To Input New Book Details")

from wsgiref.validate import validator

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

# FORMS CREATION

class EditBookForm(FlaskForm):
    title = StringField("What is the book title?", validators=[DataRequired()])
    # TODO: Create separate table for books with multiple authors. Books with single authors must be used for now.
    author = StringField("Who wrote the book?", description="Who wrote the book?", validators=[DataRequired()])
    isbn = StringField("What is the ISBN number?")
    # TODO: Use single genres for now, multiple genres will be added and referenced using another table
    # TODO: Change genre to a drop down select
    genre = StringField("What is the book Genre (Only type the main genre)")
    completed = BooleanField("Are you done with the book?")
    given_up = BooleanField("Do you actually plan on completing this book?")
    year_finished = StringField("What year did you finish the book?")
    rating = FloatField("What is your rating?", default=0)
    number_of_pages = IntegerField("How many pages are in the book?", default=0)
    # TODO:cover image was left out on purpose. You might need to upload the image
    cover_image = StringField("Enter the image url", default="https://picsum.photos/200")
    synopsis = StringField("What is this book about?")
    personal_notes = StringField("Let out all your thoughts below......")
    submit = SubmitField("Submit Changes")
    cancel = SubmitField("Cancel")

class AddNewBookForm(FlaskForm):
    title = StringField("Book Title", validators=[DataRequired()])
    author = StringField("Author Name")
    api_add = SubmitField("Add Book")
    cancel = SubmitField("Cancel")
    user_add = SubmitField("Click Here To Input New Book Details")

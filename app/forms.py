from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

# FORMS CREATION

class EditBookForm(FlaskForm):
    title = StringField("What is the book title?")
    # TODO: Create separate table for books with multiple authors. Books with single authors must be used for now.
    author = StringField("Who wrote the book?")
    isbn = IntegerField("What is the ISBN number?")
    # TODO: Use single genres for now, multiple genres will be added and referenced using another table
    # TODO: Change genre to a drop down select
    genre = StringField("What is the book Genre (Only type the main genre)", validators=[DataRequired()])
    completed = BooleanField("Are you done with the book?")
    given_up = BooleanField("Do you actually plan on completing this book?")
    year_finished = IntegerField("What year did you finish the book?")
    rating = FloatField("What is your rating?", validators=[DataRequired()])
    number_of_pages = IntegerField("How many pages are in the book?")
    # TODO:cover image was left out on purpose. You might need to upload the image
    synopsis = StringField("What is this book about?")
    personal_notes = StringField("Let out all your thoughts below......", validators=[DataRequired()])
    submit = SubmitField("Submit Changes")
    cancel = SubmitField("Cancel")

class AddNewBookForm(FlaskForm):
    title = StringField("Book Title", validators=[DataRequired()])
    author = StringField("Author Name")
    add = SubmitField("Add Book")
    cancel = SubmitField("Cancel")

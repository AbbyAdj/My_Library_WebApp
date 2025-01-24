from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, SelectField, DateField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
import requests, dotenv, os

dotenv.load_dotenv()

# VARIABLES
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

# FLASK APP CREATION AND BOOTSTRAP INTEGRATION
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
bootstrap = Bootstrap5(app)
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'journal'

# DATABASE CREATION
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_books.db"
# engine = create_engine('sqlite:///example.db', pool_size=5, max_overflow=10, pool_timeout=30)
db = SQLAlchemy(app)

class Books(db.Model):
    __tablename__ = "MyBooks"
    # CHANGE TO BOOK_ID INSTEAD OF ID
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    isbn = db.Column(db.Integer, nullable=True)
    genre = db.Column(db.String, nullable=True) # you might need to create a separate table for this later on
    completed = db.Column(db.String, nullable=True)
    given_up = db.Column(db.Boolean, nullable=True)
    year_finished = db.Column(db.SmallInteger, nullable=True)  #Can be left null if book hasn't been completed
    rating = db.Column(db.Float, nullable=True) #out of 5 stars
    number_of_pages = db.Column(db.Integer, nullable=True)
    # This part is left blank on purpose. Add later the book series column, that is, if the book is part of a series.
    cover_image = db.Column(db.Text, nullable=True)
    synopsis = db.Column(db.Text, nullable=True)
    personal_notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<{self.id}: {self.title} written by {self.author}>"

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

# ROUTES
# The TODOs below are for when the program is up and running.
# TODO: When you click on a book, it can take you to the ebook.
# TODO: Separate all methods into their respective files.
# TODO: Create different tables for the multiple authors and genres


@app.route("/", methods=["GET", "POST"])
def welcome():
    # TODO: Sorted by their ratings, show the top 3 or 4 books on the homepage before the buttons.

    if request.method == "POST":
        button_pressed = request.form["button"]
        if button_pressed == "completed":
            books = get_completed_books()
        elif button_pressed == "ongoing":
            books = get_ongoing_books()
        elif button_pressed == "no_comment":
            books = get_disliked_books()
        elif button_pressed == "all_books":
            books = get_all_books()
        else:
            return redirect(url_for("welcome"))
        return redirect(url_for("home", books=books))
    return render_template("index.html")

@app.route("/home")
def home():
    all_books_request = request.args.get("books")
    if all_books_request:
        all_books = all_books_request
    else:
        all_books = get_all_books()
    return render_template("home.html", all_books=all_books)

@app.route("/add", methods=["GET", "POST"])
def add_book():
    form = AddNewBookForm()
    redirected = request.args.get("redirected")
    if form.validate_on_submit():
        if form.add.data:
            title = form.title.data
            author = form.author.data
            query = {"intitle": title,
                     "inauthor": author}
            return redirect(url_for("select_book", query=query))
        if form.cancel.data:
            return redirect(url_for("welcome"))
    return render_template("add.html", form=form, redirected=redirected)

@app.route("/select_book")
def select_book():
    """Select which book you'd like added to the database."""
    # TODO: Find a way to incorporate books later. Use this tag:
    #  <img src="{{book['imageLinks']['medium']}}" class="d-block user-select-none" width="100%" height="200" alt="{{book.title}} book cover image">
    query = request.args.get("query")
    VOLUME_FIND_URL = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
    try:
        response = requests.get(url=VOLUME_FIND_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        # TODO: Create a custom error page that the user will be redirected to. They will have the option to go back to
        #  the home page from that error page.
        pass

    else:
        results = response.json()
        all_books = results["items"]
        return render_template("select.html", all_books=all_books)

@app.route("/add_to_database")
def add_to_database():
    volume_id = request.args.get("volume_id")[1:]
    # TODO: Rewrite code. The link to the book can be found in the json for the volume api
    BOOK_DETAILS_URL = f"https://www.googleapis.com/books/v1/volumes/{volume_id}"
    try:
        response = requests.get(BOOK_DETAILS_URL)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        # TODO: Create a custom error page that the user will be redirected to. They will have the option to go back to
        #  the home page from that error page.
        if response.status_code:
            print(response.json())
            redirected = True
            return redirect(url_for("add_book", redirected=redirected))
    else:
        results = response.json()
        print(results)
        book_fields = {"title": results["volumeInfo"]["title"],
                       "author": results["volumeInfo"]["authors"][0],
                       "isbn": results["volumeInfo"]["industryIdentifiers"][1]["identifier"],
                       "number_of_pages": results["volumeInfo"]["pageCount"],
                       "cover_image": results["volumeInfo"]["imageLinks"]["medium"],
                       "synopsis": results["volumeInfo"]["description"]
                       }
        book_id = add_new_book(book_fields=book_fields)
        return redirect(url_for("edit", book_id=book_id))

@app.route("/edit", methods=["GET", "POST"])
def edit():
    book_id = request.args.get("book_id")
    book = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    print(book)
    form = EditBookForm(obj=book)
    book_to_edit = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    if form.validate_on_submit():
        if form.submit.data:
            new_data = {field.name: field.data for field in form if form.data}
            print(new_data)
            edit_book(book_id=book_id, new_data=new_data)
            return redirect(url_for("welcome"))
        elif form.cancel.data:
            return redirect(url_for("welcome"))
    return render_template("edit.html", form=form, book_to_edit=book_to_edit)

@app.route("/delete")
def delete():
    # TODO: Add a page/condition that checks if the user is sure they want to delete the book in question.
    # TODO: Do not actually delete the record, figure out a better way to deal with this.
    book_id = request.args.get("book_id")
    delete_book(book_id=book_id)
    return redirect(url_for("home"))

@app.route("/view_book/")
def view_book():
    return "<h1>This page is not ready</h1>"

@app.route("/search")
def search():
    # Think about only getting the data from base.html. Research more on this.
    return "<h1>This page is not ready</h1>"

# NON-ROUTE METHODS

def get_all_books():
    all_books = db.session.execute(db.select(Books).order_by(Books.id)).scalars()
    return all_books

def get_completed_books():
    # Completed column = True
    completed_books = db.session.execute(db.select(Books).where(Books.completed == 1)).scalars().all()
    return completed_books

def get_ongoing_books():
    # Completed column = False, 1
    ongoing_books = db.session.execute(db.select(Books).where(Books.completed == 0)).scalars().all()
    return ongoing_books

def get_disliked_books():
    # Given_up column = True
    disliked_books = db.session.execute(db.select(Books).where(Books.given_up == 1)).scalars().all()
    return disliked_books

def add_new_book(book_fields):
    # Not all fields are added as some are not available with the google books api. These can be added by the user.
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

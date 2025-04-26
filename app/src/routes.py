import os
from flask import request, render_template, url_for, redirect, Blueprint
import requests


from .utils.queries.get_queries import *
from .utils.queries.insert_queries import *
from .utils.queries.update_queries import *
from .utils.queries.delete_queries import *
from .forms import *

# TODO: When you click on a book, it should take you to the ebook.

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def welcome():
    # TODO: Sorted by their ratings, show the top 3 or 4 books on the homepage before the buttons
    return render_template("index.html")

@main.route("/home/", methods=["GET"])
def home():
    button_pressed = request.args.get("button")
    books = []
    if button_pressed == "completed":
        books = get_completed_books()
    elif button_pressed == "ongoing":
        books = get_ongoing_books()
    elif button_pressed == "no_comment":
        books = get_disliked_books()
    elif button_pressed == "all_books":
        books = get_all_books()
    # else:
    #     return redirect(url_for("main.welcome"))
    return render_template("home.html", books=books)
    # return "Hi"

@main.route("/add", methods=["GET", "POST"])
def add_book():
    # TODO: Since the google API is acting weird, add another button for the user to add the books themselves.
    #       They don't need to have all the fields, just the important ones. Create a new form for this.
    #       They might need to upload image files though.
    form = AddNewBookForm()
    redirected = request.args.get("redirected")
    if form.user_add.data:
        return redirect(url_for("main.user_add_book"))
    if form.cancel.data:
        return redirect(url_for("main.welcome"))
    if form.validate_on_submit():
        if form.api_add.data:
            title = form.title.data
            author = form.author.data
            query = {"intitle": title,
                     "inauthor": author}
            return redirect(url_for("main.select_book", query=query))

    return render_template("add.html", form=form, redirected=redirected)

@main.route("/input", methods=["GET", "POST"])
def user_add_book():
    edit_true = False
    form = EditBookForm()
    if form.validate_on_submit():
        if form.submit.data:
            new_data = {field.name: field.data for field in form if form.data}
            # print(new_data)
            add_new_book(new_data, user_added=True)
            return redirect(url_for("main.welcome"))
        elif form.cancel.data:
            # Add flash
            return redirect(url_for("main.welcome"))
    return render_template("edit.html", form=form, edit_true=edit_true)

@main.route("/select_book")
def select_book():
    """Select which book you'd like added to the database."""
    # TODO: Find a way to incorporate books later. Use this tag:
    #  <img src="{{book['imageLinks']['medium']}}" class="d-block user-select-none" width="100%" height="200" alt="{{book.title}} book cover image">
    query = request.args.get("query")
    GOOGLE_BOOKS_API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")
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

@main.route("/add_to_database")
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
            return redirect(url_for("main.add_book", redirected=redirected))
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
        return redirect(url_for("main.edit", book_id=book_id))

@main.route("/edit", methods=["GET", "POST"])
def edit():
    edit_true = True
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
            return redirect(url_for("main.welcome"))
        elif form.cancel.data:
            return redirect(url_for("main.welcome"))
    return render_template("edit.html", form=form, book_to_edit=book_to_edit, edit_true=edit_true)

@main.route("/delete")
def delete():
    # TODO: Add a page/condition that checks if the user is sure they want to delete the book in question.
    # TODO: Do not actually delete the record, figure out a better way to deal with this.
    book_id = request.args.get("book_id")
    delete_book(book_id=book_id)
    return redirect(url_for("main.home"))

@main.route("/view_book/")
def view_book():
    return "<h1>This page is not ready</h1>"

@main.route("/search")
def search():
    # Think about only getting the data from base.html. Research more on this.
    return "<h1>This page is not ready</h1>"



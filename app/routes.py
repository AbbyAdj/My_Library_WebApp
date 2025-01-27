import os
from flask import request, render_template, url_for, redirect, current_app
import requests

from . import main
from methods import *
from forms import *

# TODO: When you click on a book, it should take you to the ebook.

@main.route("/", methods=["GET", "POST"])
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
    path = current_app.jinja_loader.searchpath[0]
    print(f"template path: {path}")
    return render_template("index.html")

@main.route("/home")
def home():
    all_books_request = request.args.get("books")
    if all_books_request:
        all_books = all_books_request
    else:
        all_books = get_all_books()
    return render_template("home.html", all_books=all_books)

@main.route("/add", methods=["GET", "POST"])
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

@main.route("/edit", methods=["GET", "POST"])
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

@main.route("/delete")
def delete():
    # TODO: Add a page/condition that checks if the user is sure they want to delete the book in question.
    # TODO: Do not actually delete the record, figure out a better way to deal with this.
    book_id = request.args.get("book_id")
    delete_book(book_id=book_id)
    return redirect(url_for("home"))

@main.route("/view_book/")
def view_book():
    return "<h1>This page is not ready</h1>"

@main.route("/search")
def search():
    # Think about only getting the data from base.html. Research more on this.
    return "<h1>This page is not ready</h1>"



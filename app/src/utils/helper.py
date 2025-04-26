import os
from flask import request, render_template, url_for, redirect, Blueprint
import requests

from .queries.get_queries import get_completed_books,get_ongoing_books,get_disliked_books,get_all_books,get_all_genres,get_all_authors
from .queries.insert_queries import add_new_book, add_new_author, add_new_genre, add_new_books_and_genres, get_all_books, get_all_authors, get_all_genres
from .queries.update_queries import edit_book
from .queries.delete_queries import delete_book
from ..forms import AddNewBookForm, EditBookForm


def home_route_books(button_pressed:str) -> list:
    books = []
    if button_pressed == "completed":
        books = get_completed_books()
    elif button_pressed == "ongoing":
        books = get_ongoing_books()
    elif button_pressed == "no_comment":
        books = get_disliked_books()
    elif button_pressed == "all_books":
        books = get_all_books()
    return books

# def
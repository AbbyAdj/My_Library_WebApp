import os

# This is simply for testing, other configurations will be added later.

class Config:
    GOOGLE_BOOKS_API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","sqlite:///my_books.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


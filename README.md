# My Library WebApp

Imagine this, you read a hundred amazing books in a year, you enjoy almost all of them and you are happy...right?
Well, wrong. Because suddenly someone asks what books you've read this year and you draw a blank. Sound familiar?

This webapp I created is meant to solve that program. With only a click (well, a few clicks) of a button, you can add all your favorite (and not so favorite)
books to the webapp. It features the ability to also write your thoughts about each single book and give them ratings. Think of it as your notes app  /favorite ebook app all in one place. This is a simple web application built with Flask which integrates the Google Books API to fetch book metadata with data stored locally in a SQLite database.

So if anyone now asks what books you've read so far, simply direct them to the website.

## Table of Contents
- Features

- Technologies

- Installation

- Usage

- Database Structure

- Future Enhancements

## Features
- **User Authentication**: Allows users to register, log in, and manage their personal book library.

- **Add/Edit/Delete Books**: Add books manually or retrieve information from Google Books API, edit details, or delete entries.

- **Book Categorization**: Sort and filter books by categories such as genre, author, or title.

- **SQLite Database**: Stores book data locally for efficient retrieval.

- **Responsive UI**: Built with Bootstrap for a clean, mobile-friendly user interface.

## Technologies
- **Backend**: Flask

- **Frontend**: HTML, CSS (Bootstrap)

- **Database**: SQLite

- **API Integration**: Google Books API

- **Version Control**: Git/GitHub

## Installation
1. Clone the repository:

```
git clone https://github.com/AbbyAdj/My_Library_WebApp.git
```

2. Install the necessary dependencies:

```
pip install -r requirements.txt
```

3. Set up the database:

- Ensure SQLite is installed.

- Run the application once to allow the database to be created automatically.

4. Run the Flask app:

```
flask run
```

Visit (http://localhost:5000) to use the app locally.

## Usage
- After running the app, you can register/login to start adding books.

- Search for books using the Google Books API integration by entering the book title or author.

- Categorize your books into genres or custom categories for easy access and organization.

- Modify or delete books from your collection.

## Database Structure
This app uses a SQLite database to store book data, including the following fields:

**Fields to be updated here soon**

The database is automatically created when the app is run for the first time.

## Future Enhancements
- **Advanced Search**: Improve search functionality to allow users to search by multiple fields (e.g., title, author, genre).

- **Reading Analytics**: Integrate analytics to track reading patterns such as the number of books read by month, or top genres.

- **API Integration with Goodreads**: Fetch additional metadata and reviews.

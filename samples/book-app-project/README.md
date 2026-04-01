# Book Collection App

A Python app for managing books you have or want to read.
It can add, remove, and list books. Mark them as read, rate them, and write reviews.

---

## Current Features

* Reads books from a JSON file (our database)
* Add, remove, list, and search books
* Mark books as read
* Rate books (1-5 stars) and write optional reviews
* View book ratings and reviews
* Input validation and error handling
* Comprehensive pytest test suite

---

## Files

* `book_app.py` - Main CLI entry point with command handlers
* `books.py` - BookCollection class with data logic
* `utils.py` - Helper functions for UI, input, and formatting
* `data.json` - Sample book data
* `tests/test_books.py` - pytest tests for all features

---

## Running the App

```bash
# List all books
python book_app.py list

# Add a new book
python book_app.py add
python book_app.py add --title "1984" --author "George Orwell" --year 1949

# Find books by author
python book_app.py find
python book_app.py find --author "Frank Herbert"

# Mark a book as read
python book_app.py mark
python book_app.py mark --title "1984"

# Rate a book and write a review
python book_app.py rate
python book_app.py rate --title "Dune" --rating 4

# View a book's rating and review
python book_app.py view-review
python book_app.py view-review --title "1984"

# Remove a book
python book_app.py remove
python book_app.py remove --title "The Hobbit"

# Show collection statistics
python book_app.py stats

# Show help
python book_app.py --help
python book_app.py rate --help
```

## Commands

### list
Display all books in your collection with titles, authors, years, read status, and ratings.

```bash
python book_app.py list
```

### add
Add a new book to your collection. You can provide details interactively or via command-line arguments.

```bash
python book_app.py add
python book_app.py add --title "Book Title" --author "Author Name" --year 2020
```

### find
Find all books by a specific author (case-insensitive substring matching).

```bash
python book_app.py find
python book_app.py find --author "Tolkien"
```

### mark
Mark a book as read. Uses fuzzy title matching (exact then substring).

```bash
python book_app.py mark
python book_app.py mark --title "1984"
```

### rate
Rate a book (1-5 stars) and optionally write a review. Each book can have one rating and one review.

```bash
python book_app.py rate
python book_app.py rate --title "Dune" --rating 4
```

### view-review
Display a book's rating and review details.

```bash
python book_app.py view-review
python book_app.py view-review --title "1984"
```

### remove
Remove a book from your collection. Uses fuzzy title matching.

```bash
python book_app.py remove
python book_app.py remove --title "The Hobbit"
```

### stats
Show collection statistics (total books, read/unread counts, oldest/newest books).

```bash
python book_app.py stats
```

## Running Tests

```bash
python -m pytest tests/
python -m pytest tests/ -v  # verbose output
```

---

## Design Notes

* **Ratings**: 1-5 stars, optional per book. Stored as integer in data.json.
* **Reviews**: Optional text, one per book. Stored as string in data.json.
* **Fuzzy matching**: Title searches use exact match first, then substring matching.
* **Validation**: All input is validated before storage (e.g., ratings must be 1-5).
* **Persistence**: All changes are immediately saved to data.json.
* **Backward compatibility**: Data files without rating/review fields load correctly.

---

## Notes

* Not production-ready (obviously)
* Some code could be improved
* Could add more commands later (e.g., export, search, filtering)

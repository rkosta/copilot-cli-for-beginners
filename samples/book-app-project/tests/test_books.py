import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


def test_set_rating():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    result = collection.set_rating("1984", 5)
    assert result is True
    rating = collection.get_rating("1984")
    assert rating == 5


def test_set_rating_with_review():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    review_text = "A masterpiece about totalitarianism"
    result = collection.set_rating("1984", 4, review_text)
    assert result is True
    rating = collection.get_rating("1984")
    assert rating == 4
    review = collection.get_review("1984")
    assert review == review_text


def test_set_rating_invalid_nonexistent_book():
    collection = BookCollection()
    result = collection.set_rating("Nonexistent Book", 5)
    assert result is False


def test_set_rating_invalid_value():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    with pytest.raises(ValueError):
        collection.set_rating("1984", 6)
    with pytest.raises(ValueError):
        collection.set_rating("1984", 0)


def test_get_rating_unrated_book():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    rating = collection.get_rating("1984")
    assert rating is None


def test_get_review_unrated_book():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    review = collection.get_review("1984")
    assert review is None


def test_update_rating():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.set_rating("1984", 4)
    assert collection.get_rating("1984") == 4
    collection.set_rating("1984", 5, "Updated to 5 stars!")
    assert collection.get_rating("1984") == 5
    assert collection.get_review("1984") == "Updated to 5 stars!"


def test_rating_persistence():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.set_rating("Dune", 4, "Epic world-building")
    
    new_collection = BookCollection()
    book = new_collection.find_book_by_title("Dune")
    assert book is not None
    assert book.rating == 4
    assert book.review == "Epic world-building"

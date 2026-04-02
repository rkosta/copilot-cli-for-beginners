import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from books import Book
from utils import format_rating, show_books


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def unread_book():
    return Book(title="1984", author="George Orwell", year=1949)


@pytest.fixture
def read_book():
    return Book(title="Dune", author="Frank Herbert", year=1965, read=True)


@pytest.fixture
def rated_book():
    return Book(title="The Hobbit", author="J.R.R. Tolkien", year=1937, read=True, rating=5)


@pytest.fixture
def capture():
    """Return a print_func that collects all output lines."""
    lines = []
    return lines, lines.append


# ---------------------------------------------------------------------------
# format_rating
# ---------------------------------------------------------------------------

class TestFormatRating:
    """Tests for format_rating."""

    @pytest.mark.parametrize("rating,expected", [
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    ])
    def test_valid_ratings_return_stars(self, rating, expected):
        assert format_rating(rating) == expected

    def test_none_returns_empty_string(self):
        assert format_rating(None) == ""

    @pytest.mark.parametrize("invalid", [0, 6, -1, -100, 100])
    def test_out_of_range_returns_empty_string(self, invalid):
        assert format_rating(invalid) == ""

    @pytest.mark.parametrize("invalid", ["5", "⭐", 3.5, [], {}])
    def test_non_integer_returns_empty_string(self, invalid):
        assert format_rating(invalid) == ""

    def test_star_count_matches_rating(self):
        for i in range(1, 6):
            assert format_rating(i).count("⭐") == i


# ---------------------------------------------------------------------------
# show_books — empty collection
# ---------------------------------------------------------------------------

class TestShowBooksEmpty:
    """Tests for show_books with an empty list."""

    def test_empty_list_prints_no_books_found(self, capture):
        lines, printer = capture
        show_books([], print_func=printer)
        assert any("No books found" in line for line in lines)

    def test_empty_list_prints_exactly_one_line(self, capture):
        lines, printer = capture
        show_books([], print_func=printer)
        assert len(lines) == 1

    def test_empty_list_no_book_entries(self, capture):
        lines, printer = capture
        show_books([], print_func=printer)
        assert not any(line.strip().startswith(("1.", "2.")) for line in lines)


# ---------------------------------------------------------------------------
# show_books — single book
# ---------------------------------------------------------------------------

class TestShowBooksSingle:
    """Tests for show_books with a single book."""

    def test_unread_book_shows_empty_checkbox(self, capture, unread_book):
        lines, printer = capture
        show_books([unread_book], print_func=printer)
        entry = next(l for l in lines if "1984" in l)
        assert "[ ]" in entry

    def test_read_book_shows_checkmark(self, capture, read_book):
        lines, printer = capture
        show_books([read_book], print_func=printer)
        entry = next(l for l in lines if "Dune" in l)
        assert "[✓]" in entry

    def test_book_title_appears_in_output(self, capture, unread_book):
        lines, printer = capture
        show_books([unread_book], print_func=printer)
        assert any("1984" in l for l in lines)

    def test_book_author_appears_in_output(self, capture, unread_book):
        lines, printer = capture
        show_books([unread_book], print_func=printer)
        assert any("George Orwell" in l for l in lines)

    def test_book_year_appears_in_output(self, capture, unread_book):
        lines, printer = capture
        show_books([unread_book], print_func=printer)
        assert any("1949" in l for l in lines)

    def test_rated_book_shows_stars(self, capture, rated_book):
        lines, printer = capture
        show_books([rated_book], print_func=printer)
        entry = next(l for l in lines if "The Hobbit" in l)
        assert "⭐" in entry

    def test_unrated_book_shows_no_stars(self, capture, unread_book):
        lines, printer = capture
        show_books([unread_book], print_func=printer)
        entry = next(l for l in lines if "1984" in l)
        assert "⭐" not in entry

    def test_entry_numbered_starting_at_one(self, capture, unread_book):
        lines, printer = capture
        show_books([unread_book], print_func=printer)
        assert any(l.strip().startswith("1.") for l in lines)


# ---------------------------------------------------------------------------
# show_books — multiple books
# ---------------------------------------------------------------------------

class TestShowBooksMultiple:
    """Tests for show_books with multiple books."""

    def test_all_books_appear_in_output(self, capture, unread_book, read_book, rated_book):
        lines, printer = capture
        show_books([unread_book, read_book, rated_book], print_func=printer)
        combined = "\n".join(lines)
        assert "1984" in combined
        assert "Dune" in combined
        assert "The Hobbit" in combined

    def test_books_are_numbered_sequentially(self, capture, unread_book, read_book, rated_book):
        lines, printer = capture
        show_books([unread_book, read_book, rated_book], print_func=printer)
        assert any(l.strip().startswith("1.") for l in lines)
        assert any(l.strip().startswith("2.") for l in lines)
        assert any(l.strip().startswith("3.") for l in lines)

    def test_order_matches_input_list(self, capture, unread_book, read_book):
        lines, printer = capture
        show_books([unread_book, read_book], print_func=printer)
        entry_lines = [l for l in lines if "1984" in l or "Dune" in l]
        assert "1984" in entry_lines[0]
        assert "Dune" in entry_lines[1]


# ---------------------------------------------------------------------------
# show_books — special characters & edge case inputs
# ---------------------------------------------------------------------------

class TestShowBooksEdgeCases:
    """Edge cases for show_books."""

    def test_very_long_title(self, capture):
        long_title = "A" * 500
        book = Book(title=long_title, author="Author", year=2000)
        lines, printer = capture
        show_books([book], print_func=printer)
        assert any(long_title in l for l in lines)

    @pytest.mark.parametrize("author", [
        "García Márquez",       # accented characters
        "Ōe Kenzaburō",         # Japanese romanisation with macrons
        "O'Brien",              # apostrophe
        "Smith-Jones",          # hyphen
        "Иван Тургенев",        # Cyrillic
        "著者名",               # CJK characters
    ])
    def test_special_characters_in_author_name(self, capture, author):
        book = Book(title="Some Title", author=author, year=2000)
        lines, printer = capture
        show_books([book], print_func=printer)
        assert any(author in l for l in lines)

    def test_book_with_year_zero(self, capture):
        """Year 0 represents an unknown publication year."""
        book = Book(title="Ancient Text", author="Unknown", year=0)
        lines, printer = capture
        show_books([book], print_func=printer)
        assert any("Ancient Text" in l for l in lines)

    def test_default_print_func_is_builtin_print(self, capsys):
        book = Book(title="1984", author="George Orwell", year=1949)
        show_books([book])
        captured = capsys.readouterr()
        assert "1984" in captured.out

    def test_custom_print_func_is_called(self):
        call_count = []
        show_books([], print_func=lambda _: call_count.append(1))
        assert len(call_count) == 1

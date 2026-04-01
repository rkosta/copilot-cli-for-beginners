import logging
from typing import Callable, List, Optional

from books import Book

logger = logging.getLogger(__name__)

PrintFunc = Callable[[str], None]


def format_rating(rating: Optional[int]) -> str:
    """Format a rating (1-5) as stars or text representation.
    
    Args:
        rating: Rating value (1-5) or None
        
    Returns:
        Formatted rating string (e.g., "⭐⭐⭐⭐⭐" or empty string if None)
    """
    if rating is None:
        return ""
    if isinstance(rating, int) and 1 <= rating <= 5:
        return "⭐" * rating
    logger.warning("format_rating received invalid value: %r", rating)
    return ""


def show_books(books: List[Book], print_func: PrintFunc = print) -> None:
    """Display books in a user-friendly format.

    Args:
        books: List of Book objects to display.
        print_func: Callable used for output; defaults to built-in print.
    """
    if not books:
        print_func("No books found.")
        return

    print_func("\nYour Book Collection:\n")
    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        rating = book.rating
        rating_str = f" {format_rating(rating)}" if rating else ""
        print_func(f"{index}. [{status}] {book.title} by {book.author} ({book.year}){rating_str}")
    print_func("")


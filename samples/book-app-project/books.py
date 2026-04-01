import json
import logging
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False

    def __post_init__(self):
        """Validate book data on creation."""
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Title must be a non-empty string")
        if not isinstance(self.author, str) or not self.author.strip():
            raise ValueError("Author must be a non-empty string")
        if not isinstance(self.year, int) or self.year < 1000 or self.year > 2100:
            raise ValueError("Year must be an integer between 1000 and 2100")

        # Normalize whitespace
        self.title = self.title.strip()
        self.author = self.author.strip()


class BookCollection:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            logger.warning("data.json is corrupted. Starting with empty collection.")
            self.books = []
        except ValueError as e:
            logger.error(f"Invalid book data: {e}")
            self.books = []

    def save_books(self):
        """Save the current book collection to JSON.
        
        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(DATA_FILE, "w") as f:
                json.dump([asdict(b) for b in self.books], f, indent=2)
        except (IOError, OSError) as e:
            logger.error(f"Failed to save books: {e}")
            raise

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new book to the collection.
        
        Args:
            title: Book title (non-empty string)
            author: Book author (non-empty string)
            year: Publication year (1000-2100)
            
        Returns:
            The created Book object
            
        Raises:
            ValueError: If book data is invalid
        """
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return all books in the collection.
        
        Returns:
            List of all Book objects
        """
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by title (case-insensitive).
        
        Args:
            title: The book title to search for
            
        Returns:
            Book object if found, None otherwise
        """
        return next(
            (b for b in self.books if b.title.lower() == title.lower()),
            None
        )

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read.
        
        Args:
            title: The title of the book to mark as read
            
        Returns:
            True if book was found and updated, False otherwise
        """
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title.
        
        Args:
            title: The title of the book to remove
            
        Returns:
            True if book was found and removed, False otherwise
        """
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author (case-insensitive).
        
        Args:
            author: The author name to search for
            
        Returns:
            List of books by the specified author
        """
        return [b for b in self.books if b.author.lower() == author.lower()]

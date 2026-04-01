def print_menu():
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    return input("Choose an option (1-5): ").strip()


def get_book_details():
    title = input("Enter book title: ").strip()
    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        year = 0

    return title, author, year


def print_books(books):
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        rating_str = format_rating(getattr(book, "rating", None))
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status} {rating_str}")


def format_rating(rating) -> str:
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
    return ""


def get_rating_input() -> int:
    """Get a valid rating input from user (1-5).
    
    Returns:
        Rating value (1-5)
    """
    while True:
        try:
            rating = int(input("Rating (1-5): ").strip())
            if 1 <= rating <= 5:
                return rating
            print("Rating must be between 1 and 5. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

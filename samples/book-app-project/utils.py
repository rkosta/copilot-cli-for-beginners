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

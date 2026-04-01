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


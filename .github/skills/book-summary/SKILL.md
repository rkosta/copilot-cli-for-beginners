---
name: book-summary
description: Generate a formatted markdown summary of a book collection - use when summarizing books, listing the collection, or creating a reading report
---

# Book Summary Skill

Generate a formatted markdown summary of a book collection from the `BookCollection` data.

## Formatting Rules

- Output a markdown table with columns: **Title**, **Author**, **Year**, **Read**, **Rating**, **Review**
- Sort rows by **year ascending** (oldest first); books with year `0` appear last under "Unknown Year"
- Use ✅ for read books, ❌ for unread
- Render rating as filled stars: 1=⭐, 2=⭐⭐, 3=⭐⭐⭐, 4=⭐⭐⭐⭐, 5=⭐⭐⭐⭐⭐; use `—` if unrated
- Truncate review text to 60 characters followed by `…` if longer; use `—` if no review
- Year `0` displays as `Unknown`

## Output Format

```
## 📚 Book Collection Summary

| Title | Author | Year | Read | Rating | Review |
|-------|--------|------|------|--------|--------|
| 1984 | George Orwell | 1949 | ✅ | ⭐⭐⭐⭐⭐ | A haunting vision of… |
| Dune | Frank Herbert | 1965 | ❌ | — | — |

**Total:** 5 books · **Read:** 3 ✅ · **Unread:** 2 ❌ · **Avg rating:** 4.2 ⭐
```

## Stats Block

Always include a one-line stats summary after the table:

- Total book count
- Number read (✅) and unread (❌)
- Average rating across rated books, rounded to 1 decimal (e.g., `Avg rating: 4.2 ⭐`); omit if no books are rated

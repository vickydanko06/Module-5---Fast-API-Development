# exercises/library-search/app/routers/books.py
# L4 — Library Search endpoints


from fastapi import APIRouter, Query, HTTPException, Path

# TODO: Import your schemas
from app.schemas.book import Book, SortField
from typing import Optional

router = APIRouter()

# Sample in-memory library — 10+ books across multiple genres
BOOKS: list[dict] = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "fantasy", "rating": 4.8, "year": 1937, "available": True},
    {"id": 2, "title": "1984", "author": "George Orwell", "genre": "dystopian", "rating": 4.7, "year": 1949, "available": False},
    {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "fiction", "rating": 4.6, "year": 1960, "available": True},
    {"id": 4, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "classic", "rating": 4.4, "year": 1925, "available": True},
    {"id": 5, "title": "Pride and Prejudice", "author": "Jane Austen", "genre": "romance", "rating": 4.7, "year": 1813, "available": False},
    {"id": 6, "title": "Dune", "author": "Frank Herbert", "genre": "science fiction", "rating": 4.8, "year": 1965, "available": True},
    {"id": 7, "title": "The Martian", "author": "Andy Weir", "genre": "science fiction", "rating": 4.6, "year": 2011, "available": True},
    {"id": 8, "title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "genre": "fantasy", "rating": 4.9, "year": 1997, "available": True},
    {"id": 9, "title": "The Shining", "author": "Stephen King", "genre": "horror", "rating": 4.5, "year": 1977, "available": False},
    {"id": 10, "title": "The Da Vinci Code", "author": "Dan Brown", "genre": "thriller", "rating": 4.2, "year": 2003, "available": True},
    {"id": 11, "title": "The Alchemist", "author": "Paulo Coelho", "genre": "fiction", "rating": 4.3, "year": 1988, "available": True},
    {"id": 12, "title": "Educated", "author": "Tara Westover", "genre": "memoir", "rating": 4.6, "year": 2018, "available": False},
    {"id": 13, "title": "Atomic Habits", "author": "James Clear", "genre": "self-help", "rating": 4.8, "year": 2018, "available": True},
    {"id": 14, "title": "Sapiens", "author": "Yuval Noah Harari", "genre": "history", "rating": 4.5, "year": 2011, "available": True},
    {"id": 15, "title": "The Name of the Wind", "author": "Patrick Rothfuss", "genre": "fantasy", "rating": 4.7, "year": 2007, "available": False},
]

# Key concept: Path vs Query parameters
#
# PATH params (/books/{id}) are used when:
#   - The value uniquely identifies a resource
#   - The resource doesn't "make sense" without it
#   - It forms part of a clean, RESTful URL hierarchy
#
# QUERY params (/books?genre=fiction) are used when:
#   - Filtering, sorting, or paginating a collection
#   - The value is optional or has a default
#   - Multiple independent filters make sense together


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int):
    """
    Returns a single book by ID.
    """
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail = f"Book {book_id} not found")


# TODO: Implement GET /books?genre=fiction&min_rating=4.0&sort_by=title&limit=10
# All query parameters are optional (have defaults)
# Use Query() with ge/le constraints for min_rating
# Use Query() with ge=1, le=100 for limit
@router.get("/", response_model=list[Book])
def search_books(
    genre: Optional[str] = Query(None, description="Filter by genre"),
    min_rating: float = Query(0.0, ge=0.0, le=5.0, description="Minimum rating"),
    sort_by: SortField = Query(SortField.title, description="Sort field"),
    limit: int = Query(10, ge=1, le=100, description="Max results to return"),
):
    results = BOOKS.copy()
    if genre:
        results = [p for p in results if p["genre"].lower() == genre.lower()]
    results = [p for p in results if p["rating"] >= min_rating]

    results.sort(key=lambda p: p[sort_by.value])

    return results[:limit]

    """
    Searches and filters books.
    """


# TODO: Implement GET /authors/{author_id}/books
# Return all books by a given author (use author_id as an index into a small
# hardcoded author list, or just treat it as a name lookup)
AUTHORS = {
    1: "George Orwell",
    2: "J.R.R. Tolkien",
    3: "Harper Lee",
}#hardcoded author list

@router.get("/authors/{author_id}/books", response_model=list[Book])
def get_books_by_author(author_id: int):
    """
    Returns all books by the specified author.
"""
    author = AUTHORS.get(author_id)
    if author is None:
        raise HTTPException(
            status_code=404,
            detail=f"Author {author_id} not found"
        )
    results = [
        book for book in BOOKS
        if book["author"] == author
    ]

    return results
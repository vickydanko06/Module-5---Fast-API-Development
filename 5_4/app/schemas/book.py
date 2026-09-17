# exercises/library-search/app/schemas/book.py
# L4 — Library Search — Book schema and sort enum

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


""" Defined SortField with the values of title, author, rating, and year"""
class SortField(str, Enum):
    title = "title" #title value
    author = "author" #author value
    rating = "rating" #rating value
    year = "year" #year value



class Book(BaseModel):
    """Represents a book in the library catalog."""
    id: int #id value
    title: str #title value
    author: str #author value
    genre: str #genre value
    rating: float = Field(ge=0, le=5) #rating value
    year: int #year value
    available: bool #available value
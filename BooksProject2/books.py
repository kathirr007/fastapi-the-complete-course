""" FastAPI for books practice 2 """

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


class BookRequest(BaseModel):
    id: int
    title: str = Field(min_length=3)
    author: str = Field(min_length=2)
    description: str = Field(min_length=10, max_length=300)
    rating: int = Field(gt=0, lt=5)


class Book:

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(
        1,
        "Computer Science Programming",
        "Kathiravan K",
        "A Book about computer programming",
        5,
    ),
    Book(
        2,
        "Engineering Mathematics",
        "Laxmanan",
        "A Book about engineering mathematics",
        4.5,
    ),
    Book(4, "Engineering Dynamics", "Joseph Daniel", "Engineering dynamics book", 3),
    Book(
        5, "Python Programming", "John Doe", "Python programming is very difficult", 4.4
    ),
    Book(
        6,
        "Python Programming 2",
        "John Doe",
        "Python programming is very difficult",
        4.4,
    ),
    Book(
        7,
        "Java Programming",
        "John Smith",
        "Java Programming book with very simple to understand examples",
        4.2,
    ),
    Book(3, "HTML/CSS Fundamentals", "John Doe", "Fundamentals of HTML/CSS", 4.6),
]


@app.get("/")
def books_api():
    return {"message": "Books API 2 working fine."}


@app.get("/books")
def read_books():
    return BOOKS


@app.post("/create_book")
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)

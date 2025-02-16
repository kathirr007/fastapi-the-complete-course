""" FastAPI for books practice 2 """

from http import HTTPStatus
from starlette import status
from typing import Optional

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="ID is not needed for creating book.", default=None
    )
    title: str = Field(min_length=3)
    author: str = Field(min_length=2)
    description: str = Field(min_length=10, max_length=300)
    rating: float = Field(gt=0, lt=6)
    published_date: int = Field(gt=1970, lt=2040)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "New title to the book",
                "author": "Kathiravan K",
                "description": "Short description about the book",
                "rating": 5,
            }
        }
    }


class Book:

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


BOOKS = [
    Book(
        1,
        "Computer Science Programming",
        "Kathiravan K",
        "A Book about computer programming",
        5,
        2020,
    ),
    Book(
        2,
        "Engineering Mathematics",
        "Laxmanan",
        "A Book about engineering mathematics",
        4.5,
        2013,
    ),
    Book(
        4, "Engineering Dynamics", "Joseph Daniel", "Engineering dynamics book", 3, 2021
    ),
    Book(
        5,
        "Python Programming",
        "John Doe",
        "Python programming is very difficult",
        4.4,
        2023,
    ),
    Book(
        6,
        "Python Programming 2",
        "John Doe",
        "Python programming is very difficult",
        4.4,
        2020,
    ),
    Book(
        7,
        "Java Programming",
        "John Smith",
        "Java Programming book with very simple to understand examples",
        4.2,
        2024,
    ),
    Book(3, "HTML/CSS Fundamentals", "John Doe", "Fundamentals of HTML/CSS", 4.6, 2023),
]


@app.get("/", status_code=status.HTTP_200_OK)
async def books_api():
    return {"message": "Books API 2 working fine."}


@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: float = Query(gt=0, lt=6)):

    return [book for book in BOOKS if book.rating == rating]


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def find_book_by_id(book_id: int = Path(gt=0)):
    found_book = next((book for book in BOOKS if book.id == book_id), None)
    if found_book:
        return found_book

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Book not found")
    # for book in BOOKS:
    #     if book.id == book_id:
    #         return book


@app.get("/books/published/", status_code=status.HTTP_200_OK)
async def get_books_by_published_date(published_date: int = Query(gt=1970, lt=2040)):
    return [book for book in BOOKS if book.published_date == published_date]


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(inc_book_id(new_book))


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(updated_book: BookRequest):
    new_book = Book(**updated_book.model_dump())

    for index, book in enumerate(BOOKS):
        if book.id == new_book.id:
            BOOKS[index] = new_book
            return new_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/books/delete_book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    # for i in range(len(BOOKS)):
    #     if BOOKS[i].id == book_id:
    #         BOOKS.pop(i)
    #         break
    # book_deleted = False
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            # BOOKS.pop(index)
            # book_deleted = True
            # return
            deleted_book = BOOKS.pop(index)
            return deleted_book
    # if not book_deleted:
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Book not found")


def extract_id(book: Book):
    return book.id


def inc_book_id(book: Book):

    book.id = book.id if len(BOOKS) == 0 else max(list(map(extract_id, BOOKS))) + 1

    return book

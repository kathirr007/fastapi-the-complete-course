"""
Fast API for Books
"""

from fastapi import FastAPI, Body

app = FastAPI()


BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]


@app.get("/")
def get_books_api():
    return {"message": "Books api working fine."}


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    # for book in BOOKS:
    #     if book.get("title").casefold() == book_title.casefold():
    #         return book

    # books_dict = {book["title"].casefold(): book for book in BOOKS}
    # print(books_dict)
    # return books_dict.get(book_title.casefold())

    found_book = next(
        (
            book
            for book in BOOKS
            if book.get("title").casefold() == book_title.casefold()
        ),
        None,
    )
    return found_book


@app.get("/books/")
async def read_category_by_query(category: str):
    # books_to_return = []
    # for book in BOOKS:
    #     if book.get("category").casefold() == category.casefold():
    #         books_to_return.append(book)
    # return books_to_return
    return [
        book for book in BOOKS if book["category"].casefold() == category.casefold()
    ]


# Get all books from a specific author using path or query parameters
@app.get("/books/byauthor/")
async def read_books_by_author_path(author: str):
    # books_to_return = []
    # for book in BOOKS:
    #     if book.get("author").casefold() == author.casefold():
    #         books_to_return.append(book)

    # return books_to_return
    return [book for book in BOOKS if book["author"].casefold() == author.casefold()]


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    # books_to_return = []
    # for book in BOOKS:
    #     if (
    #         book.get("author").casefold() == book_author.casefold()
    #         and book.get("category").casefold() == category.casefold()
    #     ):
    #         books_to_return.append(book)

    # return books_to_return
    return [
        book
        for book in BOOKS
        if book["author"].casefold() == book_author.casefold()
        and book["category"].casefold() == category.casefold()
    ]


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    # for i in range(len(BOOKS)):
    #     if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
    #         BOOKS[i] = updated_book
    # return [
    #     (
    #         updated_book
    #         if book["title"].casefold() == updated_book["title"].casefold()
    #         else book
    #     )
    #     for book in BOOKS
    # ]
    for index, book in enumerate(BOOKS):
        if book.get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[index] = updated_book
            return updated_book
    return {"error": "Book not found"}


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    # for i in range(len(BOOKS)):
    #     if BOOKS[i].get("title").casefold() == book_title.casefold():
    #         BOOKS.pop(i)
    #         break
    for index, book in enumerate(BOOKS):
        if book["title"].casefold() == book_title.casefold():
            deleted_book = BOOKS.pop(index)
            return deleted_book
        return {"error": "Book not found"}

from typing import Optional, Union
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from starlette.responses import JSONResponse
from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID



class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book",
                             max_length=100,
                             min_length=1)
    rating: int = Field(gt=-1, lt=101)
    
    class Config:
        schema_extra = {
            "example":{
                "id" : "637d1b93-0174-48e7-8959-e17530b6c690",
                "title" : "Computer Science Pro",
                "author" : "Codingwithroby",
                "description" : "A very nice description of a book",
                "rating" : 75
            }
        }

class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(
        None,
        title='Description of the Book',
        max_length=100,
        min_length=1
    )


BOOKS =[]
app = FastAPI()

class NegativeNumberException(Exception):
    def __init__(self, books_to_return: int):
        self.books_to_return = books_to_return


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request, exception: NegativeNumberException):

    return JSONResponse(
        status_code=418,
        content={"message":f"Hey, why do you want {exception.books_to_return}"
                           f"books? you need to read more!"}
    )








@app.post("/noapi")
def create_books_no_api():
    book_1 = Book(id="db6d5c1f-0460-4bab-8aa1-a801bf843273",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60)
    book_2 = Book(id="637d1b93-0174-48e7-8959-e17530b6c691",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=60)
    book_3 = Book(id="637d1b93-0174-48e7-8959-e17530b6c690",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=60)
    book_4 = Book(id="637d1b93-0174-48e7-8959-e17530b6c690",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=60)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
    






class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None



@app.get("/books/{book_id}")
async def read_all_books(book_id : UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x

@app.get("/books/{book_name}")
async def read_all_books(book_name : str):
    return BOOKS[book_name]

@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):

    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)


    if len(BOOKS) < 1:
        create_books_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"

@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction":direction_name, "sub":"Up"}
    if direction_name == DirectionName.south:
        return {"Direction":direction_name, "sub":"Down"}
    if direction_name == DirectionName.west:
        return {"Direction":direction_name, "sub":"Left"}
    return {"Direction":direction_name, "sub":"Right"}

@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book

@app.put("/{book_id}")
async def update_book(book_id:UUID, book:Book):
    counter = 0
    for BOOK in BOOKS:
        counter+=1
        if BOOK.id == book_id:
            BOOKS[counter - 1] =book
            return BOOKS[counter - 1]

@app.put("/{book_name}")
async def update_book(book_name:str, book_title:str, book_author:str):
    book_information ={'title':book_title,'author':book_author}
    BOOKS[book_name] =book_information
    return book_information

@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id:UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x



@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for BOOK in BOOKS:
        counter += 1
        if BOOK.id == book_id:
            del BOOKS[counter - 1]
            return f'ID:{book_id} deleted'
    raise HTTPException(status_code=404, detail='Book not found')

@app.post("/books/login")
async def book_login(book_id: int, username: Optional[str] = Header(None), password: Optional[str] = Header(None)):
    if username == 'FastAPIUser' and password == "test1234!":
        return BOOKS[book_id]
    return "Invalid User"


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None, convert_underscores=False)):
    return {"Random-Header" : random_header}

# Здесь хранятся классы для каталогизации книг и читателей, а также инструментарий для работы с ними
from json import *
from os import path

class json:
    def encoder(book):
        if not type(book) == Book: raise TypeError()
        else: return {"GENRE": book.genre, "AUTHOR": book.author, "TITLE": book.title, "YEAR": book.year, "STATUS": book.status }

class Book:
    def create(genre=None, author=None, title=None, year=None):
        if any([genre, author, title, year]) in [None, "", " "]: raise ValueError(print("ERROR: missing paramethers"))
        if not year.strip().isnumeric(): raise ValueError("ERROR: year must conntain numbers only")
        book = Book()
        book.genre = genre.strip()
        book.author = author.strip()
        book.title = title.strip()
        book.year = year.strip()
        book.status = "FREE"
        return book
        
    def add_base(book):
        if not type(book) == Book: raise TypeError()
        book = json.encoder(book)
        if not path.exists("book_database.json"):
            database = {1: book}
        else:
            with open("book_database.json") as file:
                database = load(file)
                database[int(max(database.keys()))+1] = book
        with open("book_database.json", "w") as file:
            dump(database, file, indent=4, ensure_ascii=False)

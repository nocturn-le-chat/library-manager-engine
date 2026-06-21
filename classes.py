# Здесь хранятся классы для каталогизации книг и читателей, а также инструментарий для работы с ними
from json import *
from os import path

class json:
    def encoder(book):
        if not type(book) == Book: raise TypeError()
        else: return {"genre": book.genre, "author": book.author, "title": book.title, "year": book.year, "status": book.status }
    
    def decoder(dictionary):
        if not type(dictionary) == dict: raise TypeError()
        if not list(dictionary.keys()) == ["genre", "author", "title", "year", "status"]: raise ValueError()

        return Book.create(dictionary["genre"], dictionary["author"], dictionary["title"], dictionary["year"], status=dictionary["status"])

class Book:
    def create(genre=None, author=None, title=None, year=None, **kwargs):
        if not list(kwargs.keys()) in [[], ["status"]]: raise ValueError()
        status = kwargs["status"] if "status" in kwargs.keys() else "FREE"

        if any([genre, author, title, year]) in [None, "", " "]: raise ValueError(print("ERROR: missing paramethers"))
        if not year.strip().isnumeric(): raise ValueError("ERROR: year must conntain numbers only")
        book = Book()
        book.genre  = genre.strip()
        book.author = author.strip()
        book.title  = title.strip()
        book.year   = year.strip()
        book.status = status
        return book


    def add_base(book):
        if type(book) == Book: book = json.encoder(book)
        elif type(book) == dict:
            book["status"] = "FREE"
            if not list(book.keys()) == ["genre", "author", "title", "year", "status"]: raise ValueError()
        else: raise TypeError()

        if not path.exists("book_database.json"):
            database = {1: book}
        else:
            with open("book_database.json", "r") as file:
                database = load(file)
                database[int(max(database.keys()))+1] = book
        
        with open("book_database.json", "w") as file:
            dump(database, file, indent=4, ensure_ascii=False)


    def edit_book(id, **kwargs):
        id = str(id)
        if any([k not in ["genre", "author", "title", "year"] for k in kwargs.keys()]): raise ValueError()
        
        with open("book_database.json", "r") as file:
            book = (database:=load(file))[id]

        book["genre"]  = kwargs["genre"] if "genre" in kwargs.keys() else book["genre"]
        book["author"] = kwargs["author"] if "author" in kwargs.keys() else book["author"]
        book["title"]  = kwargs["title"] if "title" in kwargs.keys() else book["title"]
        book["year"]   = kwargs["year"] if "year" in kwargs.keys() else book["year"]
        
        database[id] = book

        with open("book_database.json", "w") as file:
            dump(database, file, indent=4, ensure_ascii=False)


    def st_change(id, **kwargs):
        if not id > 0: raise ValueError()
        id = str(id)
        if not list(kwargs.keys()) == ["status"]: raise ValueError()
        elif not type(kwargs["status"]) == str: raise TypeError()
        elif not kwargs["status"].lower() in ["free", "taken"]: raise ValueError()

        with open("book_database.json", "r") as file:
            book = (database:=load(file))[id]
        
        book["status"] = kwargs["status"].upper()
        database[id] = book

        with open("book_database.json", "w") as file:
            dump(database, file, indent=4, ensure_ascii=False)


    def del_base(id):
        if not id > 0: raise ValueError()
        id = str(id)
        if not path.exists("book_database.json"): raise ValueError()
        with open("book_database.json", "r") as file:
            database = load(file)
        if not id in database.keys(): raise ValueError()
        del database[id]
        with open("book_database.json", "w") as file:
            dump(database, file, indent=4, ensure_ascii=False)

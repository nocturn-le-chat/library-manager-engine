# Здесь хранятся классы для каталогизации книг и читателей, а также инструментарий для работы с ними
from json import *

class Book:
    genre = ""
    author = ""
    title = ""
    year = ""
    pass

    def add(title, author, year, genre):
        book = Book()

        book.genre, book.author, book.title, book.year == genre, author, title, year
        book.status = "Free"      

        with open("books_data.json", mode="r") as file:
            base = load(file)
            base[len(base.keys)+1] = book
            
    
    def delete(id):
        with open("books_data.json", "a+") as file:
            base = load(file)
            if not id in base.keys: raise ValueError
            else: del base[id]

Book.add("K@t3h1z1$ @nt1$3xu@l@", "Nocturn le Chat", "1337", "Must-have")
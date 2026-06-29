# Здесь хранятся классы для каталогизации книг и читателей, а также инструментарий для работы с ними
from json import *
from os import path
from datetime import date


def hash(password, *mode):
    if mode == ("encrypt",):
        p_hash = 0
        for k in range(len(password)):
            p_hash += ord(password[k])*65599**(len(password) - k)
            return p_hash
    elif mode == ("decrypt",):
            
        return None

class book:
    def create(genre=str, author=str, title=str, year=int, *status):
        if any([type(k) != str for k in [genre, author, title]]) or type(year)!=int: raise TypeError()
        
        if not len(status) in [0, 1]: raise ValueError()
        else:
            if len(status) == 1 and list(status)[0].lower() in ["free", "taken"]: raise ValueError()

        book = {"genre": genre, 
                "author": author, 
                "title": title, "year": year, 
                "status": "FREE" if len(status) == 0 else list(status)[0].upper()
                    }
        database.add(book, "book")
    
class user:
    def create(first_name='', last_name='', contacts={}, login='', password=''):
        if any([type(k)!=str for k in [first_name, last_name, login, password]]) or type(contacts)!=dict: raise TypeError
        if all([k not in ["email", "phone"] for k in contacts.keys()]): raise ValueError()

        user = {"first_name": first_name,
                "last_name":  last_name,
                "phone":      contacts["phone"] if "phone" in contacts.keys() else None,
                "email":      contacts["email"] if "email" in contacts.keys() else None,
                "login":      login,
                "password":   hash(password, "encrypt"),
                "books":      {}
                    }
        database.add(user, "user")
    

    def add_book(user_id, book_id):
        if any([type(k)!=int for k in [user_id, book_id]]): raise TypeError()
        elif user_id<1 or book_id<1: raise ValueError()
        user_books = load(open("user_database.json", "r"))[f"{user_id}"]["books"]
        user_books[f"{book_id}"] = str(date.today())
        database.edit("user", user_id, books=user_books)
        database.edit("book", book_id, status="TAKEN")


    def delete_book(user_id, book_id):
        if any([type(k)!=int for k in [user_id, book_id]]): raise TypeError()
        elif user_id<1 or book_id<1: raise ValueError()
        books = load(open("user_database.json", "r"))[f"{user_id}"]["books"]
        database.edit("user", user_id, books=books.remove(book_id) if len(books)>1 else [])
        database.edit("book", book_id, status="FREE")
    

    def ban(id):
        user = load(open("user_database.json", "r"))[str(id)]
        database.delete("user", id)
        database.add(user, "banned")

class database:
    def add(object={}, category=''):
        if list(map(type, [object, category])) != [dict, str]: raise TypeError()
        elif any([len(k)==0 for k in [object, category]]): raise ValueError()

        if not path.exists(f"{category}_database.json"):
            database = {"1": object}
        else:
            database = load(open(f"{category}_database.json", "r"))
            database[int(max(database.keys()))+1] = object
        
        with open(f"{category}_database.json", "w") as file: dump(database, file, indent=4, ensure_ascii=False)


    def edit(category='', id=0, **changes):
        if list(map(type, [category, id, changes])) != [str, int, dict]: raise TypeError()
        elif category == "" or not id > 0 or len(changes) == 0: raise ValueError()
        id = str(id)

        if not path.exists(pth:=f"{category.lower()}_database.json"): raise ValueError()
        database = load(open(pth, "r"))
                
        changes = {k.lower(): changes[k] for k in changes.keys() if k in database[id].keys()}
        if len(changes) == 0: raise ValueError()
        for attribute in changes.keys():
            database[id][attribute] = changes[attribute]
        
        with open(pth, "w") as file: dump(database, file, indent=4, ensure_ascii=False)


    def delete(category=str, id=int):
        id = str(id)
        if not path.exists(pth:=f"{category}_database.json"): raise ValueError()

        database = load(open(pth, "r"))
        if not id in database.keys(): raise ValueError()
        database.remove(id)
        
        with open(pth, "w") as file: dump(database, file, indent=4, ensure_ascii=False)

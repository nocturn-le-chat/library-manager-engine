from classes import *
import npyscreen
from os import path

## Описание окон и действий в каждом
class Terminal(npyscreen.StandardApp):
    def onStart(self):
        # Подготовка индексных списков для быстрого поиска
        self.addForm("MAIN", main_menu, name="Library search engine ver.0.1")
        self.addForm("BOOKS", book_catalog, name="Catalogs\>Books")
        self.addForm("ADD_BOOK", add_book, name="Catalogs\>Books\>Add")
        self.addForm("SEARCH_BOOK", search_book, name="Catalogs\>Books\>Search")
        self.addForm("EDIT_BOOK", edit_book, name="Catalogs\>Books\>Edit")
        self.addForm("DEL_BOOK", delete_book, name="Catalogs\>Books\>Delete")

        self.addForm("USERS", user_catalog, name="Catalogs\>Users")
        self.addForm("SEARCH_USER", search_user, name="Catalogs\>Users\>Search")
        self.addForm("BAN_USER", ban_user, name="Catalogs\>Users\>Ban")

class add_book(npyscreen.FormBaseNew):
    def create(self):
        global process_flag
        process_flag = False

        self.add(npyscreen.FixedText, editable=False, value="===== Paramethers =======================", relx=3, rely=3)
        self.genre_field   = self.add(npyscreen.TitleText,
                                 name="Genre:  >>> ",
                                 relx=3, rely=5)
        self.author_field  = self.add(npyscreen.TitleText,
                                 name="Author: >>> ",
                                 relx=3, rely=7)
        self.title_field   = self.add(npyscreen.TitleText,
                                 name="Title:  >>> ",
                                 relx=3, rely=9)
        self.year_field    = self.add(npyscreen.TitleText,
                                 name="Year:   >>> ",
                                 relx=3, rely=11)
        
        submit_button = self.add(npyscreen.ButtonPress,
                                 name=">>> 9. Submit",
                                 relx=3, rely=13)
        submit_button.whenPressed = self.confirm

        self.status = self.add(npyscreen.FixedText, editable=False, value=" ", relx=3, rely=15, color="Important")
        
        self.add(npyscreen.FixedText, editable=False, value="===== Extras ============================", relx=3, rely=18)
        back         = self.add(npyscreen.ButtonPress, 
                                name=">>> 0. Back", 
                                relx=3, rely=20)
        back.whenPressed = self.back


    def confirm(self):
        global process_flag
        process_flag = True
        self.editing = False

    def afterEditing(self):
        global process_flag
        if process_flag:
            global genres; global authors; global titles; global years 
            genre  = self.genre_field.value.strip()
            author = self.author_field.value.strip()
            title  = self.title_field.value.strip()
            year   = self.year_field.value.strip()

            if any([k=="" for k in [genre, author, title, year]]):
                self.status.value = "Must not contain empty values"
                self.display()
            elif not year.isnumeric() or int(year)<=0:
                self.status.value = "Incorrect year input"
                self.display()

            flag = False
            if path.exists("book_database.json"):
                flag = True
                checkbox = [genre.lower() in genres.keys(),
                            author.lower() in authors.keys(),
                            title.lower() in titles.keys(),
                            year.strip() in years.keys()]
            if flag and all(checkbox):
                self.status.value = "Already exists in catalog"
                self.display()
            else:
                book.create(genre, author, title, int(year))
                self.status.value = "Added to database"
                self.display()
        

    def back(self):
        self.parentApp.switchForm("BOOKS")

class search_book(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.FixedText, editable=False, value="===== ID search ========================", relx=3, rely=3)
        self.id_field     = self.add(npyscreen.TitleText,
                                     name="ID:       >>> ", relx=3, rely=5)
        
        self.add(npyscreen.FixedText, editable=False, value="===== Paramether search ================", relx=3, rely=7)
        self.genre_field   = self.add(npyscreen.TitleText,
                                      name="Genre:    >>> ", relx=3, rely=9)
        self.author_field  = self.add(npyscreen.TitleText,
                                      name="Author:   >>> ", relx=3, rely=11)
        self.title_field   = self.add(npyscreen.TitleText,
                                      name="Title:    >>> ", relx=3, rely=13)
        self.year_field    = self.add(npyscreen.TitleText,
                                      name="Year:     >>> ", relx=3, rely=15)
        submit_button = self.add(npyscreen.ButtonPress,
                                      name=">>>  9. Search", relx=3 ,rely=17)
        submit_button.whenPressed = self.on_submit
        
        self.add(npyscreen.FixedText, editable=False, value="===== Extras ===========================", relx=3, rely=18)
        back_button   = self.add(npyscreen.ButtonPress,
                                 name=">>>  0. Back", relx=3, rely=20)
        back_button.whenPressed = self.back

    def on_submit(self):
        global search_flag
        search_flag = True
        self.editing = False

    def afterEditing(self):
        global search_flag
        if search_flag:
            if not path.exists("book_database.json"):
                self.add(npyscreen.FixedText, value="Empty catalog", relx=50, rely=3)
                search_flag = False
        
        if search_flag:
            id = self.id_field.value.strip()
            genre = self.genre_field.value.strip().lower()
            author = self.author_field.value.strip().lower()
            title = self.title_field.value.strip().lower()
            year = self.year_field.value.strip()

            if all([k=="" for k in [id, genre, author, title, year]]):
                self.add(npyscreen.FixedText, value="Empty ID and paramethers", relx=50, rely=3)
                self.display()
            elif not id.isnumeric or not year.isnumeric:
                self.add(npyscreen.FixedText, value="Incorrect ID/year", relx=50, rely=3)
                self.display()
            elif int(id)<0:
                self.add(npyscreen.FixedText, value="Incorrect ID", relx=50, rely=3)
                self.display()
            elif id!="" and any([k!="" for k in [genre, author, title, year]]):
                self.add(npyscreen.FixedText, value="Can search by only ID or only by paramethers", relx=50, rely=3)
                self.display()
            if id != "":
                global book_ids
                if id in book_ids:
                    book = load(open("book_database.json"))[id]
                    self.add(npyscreen.FixedText, value=str(book), relx=50, rely=3)
                    self.display()
            else:
                global genres; global authors; global titles; global years
                g_res = genres[genre] if genre!="" and genre in genres.keys() else []
                a_res = authors[author] if author!="" and author in authors.keys() else []
                t_res = titles[title] if title!="" and title in titles.keys() else []
                y_res = years[year] if year!="" and year in years.keys() else []
                result = list(set(g_res) & set(a_res) & set(t_res) & set(y_res))

                if result==[]:
                    self.add(npyscreen.FixedText, value="Nothing found", relx=50, rely=3)
                    self.display()
                else:
                    counter, books = 1, []
                    for res in result:
                        books.append(load(open("book_database.json"))[res])
                    for book in books:
                        if counter < 8:
                            self.add(npyscreen.FixedText, value=str(book), relx=50, rely=2*counter+1)
                    self.display()
                    

    def back(self):
        global search_flag
        search_flag = False
        self.parentApp.switchForm("BOOKS")

## Подготовительная часть
if path.exists("book_database.json"):
    genres, authors, titles, years = {}, {}, {}, {}
    database = load(open("book_database.json", "r"))
    book_ids = list(database.keys())
    for id in database.keys():
        genre  = database[id]["genre"].lower()
        author = database[id]["author"].lower()
        title  = database[id]["title"].lower()
        year   = str(database[id]["year"])

        genres[genre]   = genres[genre]+[id]   if genre in genres.keys()   else [id]
        authors[author] = authors[author]+[id] if author in authors.keys() else [id]
        titles[title]   = titles[title]+[id]   if title in titles.keys()   else [id]
        years[year]     = years[year]+[id]     if year in years.keys()     else [id]

if path.exists("user_database.json"):
    first_names, last_names = {}, {}
    database = load(open("user_database.json"))
    user_ids = list(database.keys())
    for id in database.keys():
        first_name = database[id]["first_name"].lower()
        last_name = database[id]["last_name"].lower()

        first_names[first_name] = first_names[first_name]+id if first_name in first_names.keys() else [id]
        last_names[last_name] = last_names[last_name]+id if last_name in last_names.keys() else [id]
    

## Запуск терминала
MyTerminal = Terminal()
MyTerminal.run()

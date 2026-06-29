from classes import *
import npyscreen

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

# Главное меню
class main_menu(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.FixedText, editable=False, value="===== Catalog Management ===============", relx=3, rely=3)
        books = self.add(npyscreen.ButtonPress, 
                 name=">>>  1. Manage books catalog",
                 relx=3, rely=5)
        books.whenPressed = self.open_books

        users = self.add(npyscreen.ButtonPress,
                 name=">>>  2. Manage users catalog",
                 relx=3, rely=7)
        users.whenPressed = self.open_users

        self.add(npyscreen.FixedText, editable=False, value="===== Extras ===========================", relx=3, rely=18)
        exit = self.add(npyscreen.ButtonPress,
                 name=">>>  0. Exit",
                 relx=3, rely=20)
        exit.whenPressed = self.exit

    def open_books(self):
        self.parentApp.switchForm('BOOKS')
    def open_users(self):
        self.parentApp.switchForm('USERS')
    def exit(self):
        self.parentApp.switchForm(None)

# Книжный каталог
class book_catalog(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.FixedText, editable=False, value="===== Books management =================", relx=3, rely=3)
        add_button    = self.add(npyscreen.ButtonPress, 
                                name=">>>  1. Add book",
                                relx=3, rely=5)
        add_button.whenPressed = self.add_book

        search_button = self.add(npyscreen.ButtonPress,
                                 name=">>>  2. Search Book",
                                 relx=3, rely=7)
        search_button.whenPressed = self.search_book

        edit_button   = self.add(npyscreen.ButtonPress,
                                 name=">>>  3. Edit book",
                                 relx=3, rely=9)
        edit_button.whenPressed = self.edit_book

        delete_button = self.add(npyscreen.ButtonPress,
                                 name=">>>  4. Delete book",
                                 relx=3, rely=11)
        delete_button.whenPressed = self.delete_book

        self.add(npyscreen.FixedText, editable=False, value="===== Extras ===========================", relx=3, rely=18)
        menu_button   = self.add(npyscreen.ButtonPress,
                                 name=">>>  0. Exit to menu",
                                 relx=3, rely=20)
        menu_button.whenPressed = self.main_menu


    def add_book(self):
        self.parentApp.switchForm("ADD_BOOK")
    def search_book(self):
        self.parentApp.switchForm("SEARCH_BOOK")
    def edit_book(self):
        self.parentApp.switchForm("EDIT_BOOK")
    def delete_book(self):
        self.parentApp.switchForm("DEL_BOOK")
    def main_menu(self):
        self.parentApp.switchForm("MAIN")

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
                global id_s
                if id in id_s:
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

class edit_book(npyscreen.FormBaseNew):
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
                                      name=">>>  9. Edit", relx=3 ,rely=17)
        submit_button.whenPressed = self.on_submit
        
        self.add(npyscreen.FixedText, editable=False, value="===== Extras ===========================", relx=3, rely=18)
        back_button   = self.add(npyscreen.ButtonPress,
                                 name=">>>  0. Back", relx=3, rely=20)
        back_button.whenPressed = self.back

    def on_submit(self):
        global edit_flag
        edit_flag = True
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
            elif not (id!="" and any([k!="" for k in [genre, author, title, year]])):
                self.add(npyscreen.FixedText, value="Missing editable book index or edited paramethers", relx=50, rely=3)
                self.display()
            elif not id in id_s:
                self.add(npyscreen.FixedText, value="No such book", relx=50, rely=3)
                self.display()
            else:
                changes = {}
                if genre!="":  changes["genre"] = genre
                if author!="": changes["author"] = author
                if title!="":  changes["title"] = title
                if year!="":   changes["year"] = year
                database.edit("book", int(id), changes=changes)
                self.add(npyscreen.FixedText, value="Edited", relx=50, rely=3)
                self.display()

    def back(self):
        global search_flag
        search_flag = False
        self.parentApp.switchForm("BOOKS")   

class delete_book(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.FixedText, editable=False, value="===== ID ===============================", relx=3, rely=3)
        self.id_field = self.add(npyscreen.TitleText,
                                 name="ID:  >>> ", relx=3, rely=5)
        submit_button = self.add(npyscreen.ButtonPress,
                                 name=">>>  1. Delete", relx=3, rely=7)
        submit_button.whenPressed = self.on_submit

        self.add(npyscreen.FixedText, ediatble=False, value="===== Extras ===========================", relx=3, rely=18)
        back_button   = self.add(npyscreen.ButtonPress,
                                 name=">>>  0. Back", relx=3, rely=20)
        back_button.whenPressed = self.back

    def on_submit(self):
        global delete_flag
        delete_flag = True
        self.editing = False
    
    def back(self):
        global delete_flag
        delete_flag = False
        self.parentApp.switchForm("BOOKS")

    def afterEditing(self):
        global delete_flag
        if delete_flag:
            id = self.id_field.value.strip()
            if id=="":
                self.add(npyscreen.FixedText, editable=False, value="Empty ID", relx=3, rely=15)
                self.display()
            elif not id.isnumerical() or int(id)<1:
                self.add(npyscreen.FixedText, editable=False, value="Incorrect ID", relx=3, rely=15)
                self.display()
            elif not id in id_s:
                self.add(npyscreen.FixedText, editable=False, value="ID doesn't exist", relx=3, rely=15)
                self.display()
            else:
                database.delete("book", id)
                self.add(npyscreen.FixedText, editable=False, value="Deleted", relx=3, rely=15)
                self.display()


# Читательский каталог
class user_catalog(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.FixedText, editable=False, value="===== Users management =================", relx=3, rely=3)
        search_button = self.add(npyscreen.ButtonPress,
                                 name=">>>  1. Search user",
                                 relx=3, rely=5)
        search_button.whenPressed = self.search_user

        delete_button = self.add(npyscreen.ButtonPress,
                                 name=">>>  2. Ban user",
                                 relx=3, rely=7)
        delete_button.whenPressed = self.ban_user

        self.add(npyscreen.FixedText, editable=False, value="===== Extras ===========================", relx=3, rely=18)
        menu_button   = self.add(npyscreen.ButtonPress,
                                 name=">>>  0. Exit to menu",
                                 relx=3, rely=20)
        menu_button.whenPressed = self.main_menu


    def search_user(self):
        pass
    def ban_user(self):
        pass
    def main_menu(self):
        self.parentApp.switchForm("MAIN")

class search_user(npyscreen.FormBaseNew):
    pass

class ban_user(npyscreen.FormBaseNew):
    pass

## Подготовительная часть
if path.exists("book_database.json"):
            genres, authors, titles, years = {}, {}, {}, {}
            database = load(open("book_database.json", "r"))
            id_s = list(database.keys())
            for id in database.keys():
                genre  = database[id]["genre"].lower()
                author = database[id]["author"].lower()
                title  = database[id]["title"].lower()
                year   = str(database[id]["year"])

                genres[genre]   = genres[genre]+[id]   if genre in genres.keys()   else [id]
                authors[author] = authors[author]+[id] if author in authors.keys() else [id]
                titles[title]   = titles[title]+[id]   if title in titles.keys()   else [id]
                years[year]     = years[year]+[id]     if year in years.keys()     else [id]

## Запуск терминала
MyTerminal = Terminal()
MyTerminal.run()

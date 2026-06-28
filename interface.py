from classes import *
import npyscreen

## Описание окон и действий в каждом
class Terminal(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", main_menu, name="Library search engine ver.0.1")
        self.addForm("BOOKS", book_catalog, name="Catalogs\>Books")
        self.addForm("USERS", user_catalog, name="Catalogs\>Users")

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
        pass
    def search_book(self):
        pass
    def edit_book(self):
        pass
    def delete_book(self):
        pass
    def main_menu(self):
        self.parentApp.switchForm("MAIN")

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

## Подготовительные процессы и запуск

# Подготовка индексных списков для быстрого поиска
if path.exists("book_database.json"):

    genres, authors, titles, years = {}
    database = load(open("book_database.json", "r"))
    for id in database.keys():
        genre  = database[id]["genre"]
        author = database[id]["author"]
        title  = database[id]["title"]
        year   = database[id]["year"]

        genres[genre]   = genres[genre]+[id]   if genre in genres.keys()   else [id]
        authors[author] = authors[author]+[id] if author in authors.keys() else [id]
        titles[title]   = titles[title]+[id]   if title in titles.keys()   else [id]
        years[year]     = years[year]+[id]     if year in years.keys()     else [id]


# Запуск терминала
MyTerminal = Terminal()
MyTerminal.run()

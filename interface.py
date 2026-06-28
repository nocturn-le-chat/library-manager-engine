from classes import *
import npyscreen

## Описание окон и действий в каждом
class Terminal(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", main_menu, name="Library search engine ver.0.1")
        self.addForm("BOOKS", book_catalogue, name="Books cataogue")
        self.addForm("USERS", user_catalogue, name="User cataogue")

# Главное меню
class main_menu(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.FixedText, editable=False, value="===== Catalog Management ===============", relx=3, rely=3)
        books = self.add(npyscreen.ButtonPress, 
                 name=">>>  1.Manage books catalog",
                 relx=3, rely=5)
        books.whenPressed = self.open_books

        users = self.add(npyscreen.ButtonPress,
                 name=">>>  2.Manage users catalog",
                 relx=3, rely=7)
        users.whenPressed = self.open_users

        self.add(npyscreen.FixedText, editable=False, value="===== Extras ===========================", relx=3, rely=18)
        exit = self.add(npyscreen.ButtonPress,
                 name=">>>  0.Exit",
                 relx=3, rely=20)
        exit.whenPressed = self.exit

    def open_books(self):
        self.parentApp.switchForm('BOOKS')

    def open_users(self):
        self.parentApp.switchForm('USERS')
    def exit(self):
        self.parentApp.switchForm(None)

# Книжный каталог
class book_catalogue(npyscreen.ActionForm):
    def create(self):
        self.add(npyscreen.TitleText,
                 name="Books catalog",
                 value="Nothing here!")
    
    def on_ok(self):
        self.parentApp.switchForm('MAIN')

# Читательский каталог
class user_catalogue(npyscreen.ActionForm):
    def create(self):
        self.add(npyscreen.TitleText,
                 name="Users catalog",
                 value="Nothing here!")
        
    def on_ok(self):
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

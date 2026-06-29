from classes import *
import npyscreen
from os import path

## Описание окон и действий в каждом
class Terminal(npyscreen.StandardApp):
    def onStart(self):
        # Подготовка индексных списков для быстрого поиска
        self.addForm("MAIN", entry, name="Wellcome!")
        self.addForm("SIGNUP", signup, name="Sign up")
        self.addForm("SIGNIN", signin, name="Sign in")
        self.addForm("MENU", menu, "Library search engine ver.0.1")
        self.addForm("CATALOG", search_book, name="BOOKS CATALOG")

class entry(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.FixedText, editable=False, value="===== Choose option ====================", relx=3, rely=3)
        self.sign_up = self.add(npyscreen.ButtonPress,
                                name=">>> 1. Sign up", relx=3, rely=5)
        self.sign_up.whenPressed = self.on_signup
        self.sign_in = self.add(npyscreen.ButtonPress,
                                name=">>> 1. Sign in", relx=3, rely=7)
        self.sign_in.whenPressed = self.on_signin

        self.add(npyscreen.FixedText, editable=False, value="===== Extras ===========================", relx=3, rely=18)
        self.exit_button = self.add(npyscreen.ButtonPress,
                                    name=">>> 0. Exit", relx=3, rely=20)
        self.exit_button.whenPressed = self.exit

    def on_signup(self):
        self.parentApp.switchForm("SIGNUP")
    
    def on_signin(self):
        self.parentApp.switchForm("SIGNIN")
    
    def exit(self):
        self.parentApp.switchForm(None)

class signup(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.FixedText, editable=False, value="===== Enter paramethers ================", relx=3, rely=3)
        self.first_field    = self.add(npyscreen.TitleText,
                                       name="First name:   >>> ", relx=3, rely=5)
        self.last_field     = self.add(npyscreen.TitleText,
                                       name="Last name:    >>> ", relx=3, rely=7)
        self.phone_field    = self.add(npyscreen.TitleText,
                                       name="Phone:        >>> ", relx=3, rely=9)
        self.email_field    = self.add(npyscreen.TitleText,
                                       name="Email:        >>> ", relx=3, rely=11)
        self.login_field    = self.add(npyscreen.TitleText,
                                       name="Login:        >>> ", relx=50, rely=5)
        self.password_field = self.add(npyscreen.TitleText,
                                       name="Password:     >>> ", relx=50, rely=7)
        self.submit_button  = self.add(npyscreen.ButtonPress,
                                       name=">>> 9. Sign in", relx=3, rely=13)
        self.submit_button.whenPressed = self.submit

        self.add(npyscreen.FixedText, editable=False, value="===== Extras ===========================", relx=3, rely=18)
        self.back_button = self.add(npyscreen.ButtonPress,
                                    name=">>> 0. Back", relx=3, rely=20)
        self.back_button.whenPressed = self.back

    def submit(self):
        global signin_flag
        signin_flag = True
        self.editing = False

    def afterEditing(self):
        if signin_flag:
            first_name = self.first_field.value.strip()
            last_name = self.last_field.value.strip()
            phone = self.phone_field.value.strip()
            email = self.email_field.value.strip()
            login = self.login_field.value.strip()
            password = self.password_field.value.strip()

            if any([k=="" for k in [first_name, last_name, phone, email, login, password]]):
                self.add(npyscreen.FixedText, value="Empty paramethers", relx=50, rely=3)
                self.display()
            elif not phone.isnumerical():
                self.add(npyscreen.FixedText, value="Incorrect phone", relx=50, rely=3)
                self.display()
            elif list(set(first_names[first_name]) & set(last_names[last_name]))!=[]:
                self.add(npyscreen.FixedText, value="Already exists", relx=50, rely=3)
                self.display()
            else:
                user.create(first_name, last_name, {"phone": phone, "email": email}, login, password)
                global entry_data; global user_id
                entry_data[id] = [login, password]
                user_id = id
                self.add(npyscreen.FixedText, value="Signed up!", relx=50, rely=3)
                self.display()
                self.parentApp.switchForm("MENU")
                

    def back(self):
        global signin_flag
        signin_flag = False
        self.parentApp.switchForm("MAIN")

class signin(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.FixedText, editable=False, value="===== Enter paramethers ================", relx=3, rely=3)
        self.login_field    = self.add(npyscreen.TitleText,
                                       name="Login:        >>> ", relx=3, rely=5)
        self.password_field = self.add(npyscreen.TitleText,
                                       name="Password:     >>> ", relx=3, rely=7) 
        self.submit_button  = self.add(npyscreen.ButtonPress,
                                       name=">>> 9. Sign in", relx=3, rely=13)
        self.submit_button.whenPressed = self.submit

        self.add(npyscreen.FixedText, editable=False, value="===== Extras ===========================", relx=3, rely=18)
        self.back_button = self.add(npyscreen.ButtonPress,
                                    name=">>> 0. Back", relx=3, rely=20)
        self.back_button.whenPressed = self.back

    def submit(self):
        global signin_flag
        signin_flag = True
        self.editing = False

    def back(self):
        global signin_flag
        signin_flag = False
        self.parentApp.switchForm("MAIN")
        
class menu(npyscreen.FormBaseNew):
    pass

class search_book(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.FixedText, editable=False, value="===== ID search ========================", relx=3, rely=3)
        self.id_field     = self.add(npyscreen.TitleText,
                                     name="ID:        >>> ", relx=3, rely=5)
        
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
        self.parentApp.switchForm("MENU")

class add_book(npyscreen.FormBaseNew):
    def create(self):
        global process_flag
        process_flag = False

        self.add(npyscreen.FixedText, editable=False, value="===== Paramethers =======================", relx=3, rely=3)
        self.id_field = self.add(npyscreen.TitleText,
                                 name="ID:  >>> ",
                                 relx=3, rely=5)
        
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
                user.add_book(user_id, id)
                self.status.value = "Added to your profile"
                self.display()
        

    def back(self):
        self.parentApp.switchForm("CATALOG")



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
    first_names, last_names, entry_data = {}, {}, {}
    database = load(open("user_database.json"))
    user_ids = list(database.keys())
    for id in database.keys():
        first_name = database[id]["first_name"].lower()
        last_name = database[id]["last_name"].lower()
        login = database[id]["login"].lower()
        password = database[id]["password"]

        first_names[first_name] = first_names[first_name]+id if first_name in first_names.keys() else [id]
        last_names[last_name] = last_names[last_name]+id if last_name in last_names.keys() else [id]
        entry_data[id] = [login, password]
    

## Запуск терминала
MyTerminal = Terminal()
MyTerminal.run()

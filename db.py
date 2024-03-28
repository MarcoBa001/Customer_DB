import tkinter
import tkcalendar
import tkinter.messagebox
import mysql.connector

# Manage a db of customers. Each customer is characterized by:
#   name, surname, dateOfBirth, genre, email, phoneNumber
# The user has the possibility of:
#   add a new customer
#   remove a precise customer
#   select customers of genre M
#   select the phoneNumber of a precise customer, given his/her name and surname
# *** DB CONNECTION ***
db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "customer_db"
)

cursor = db.cursor()
# Interrogazione db -> estrarre tutti i clienti contenuti nel db
# cursor.execute("SELECT * FROM customers")
# print(cursor.fetchall())

def add_customer():
    """
    Extracts all information of the customer, creates an object of type Customer,
    adds it in a Python list and store the customer in CUSTOMERS Table in the db.
    """
    customer_name = name_entry.get().strip().title()
    customer_surname = surname_entry.get().strip().title()
    customer_date_birth = dateOfBirth_entry.get_date()
    customer_genre = select_option.get()
    customer_email = email_entry.get().strip().lower()
    customer_phone = phone_entry.get().strip()
    if (customer_name and customer_surname and customer_date_birth and 
        customer_genre and customer_email and customer_phone):
        # Create an object of class Customer
        customer = Customer(customer_name, customer_surname, customer_date_birth, 
                            customer_genre, customer_email, customer_phone)
        # Add this customer to a list of customers
        customers_list.append(customer)
        print(customers_list)
        # Insert customer in db
        query = f"INSERT INTO customers(Name, Surname, DateOfBirth, Genre, Email, PhoneNumber) VALUES(%s, %s, %s, %s, %s, %s)"
        valori = (customer_name, customer_surname, customer_date_birth, customer_genre, customer_email, customer_phone)
        cursor.execute(query, valori)
        db.commit()
        # Create a label of success
        print(customer_genre)
        success_label = tkinter.Label(window, text = "Customer added with success", fg="green")
        success_label.grid(row = 7, column = 0, columnspan = 2)
    else:
        tkinter.messagebox.showwarning("Error in add customer", "Not all fields are compiled")


def remove_customer():
    name_removed=name_entry_rem.get().strip().title()
    surname_removed=surname_entry_rem.get().strip().title()
    if name_removed and surname_removed:
        #cancellare dal db
        query=f"DELETE from customers where name = %s AND Surname = %s"
        valori = (name_removed, surname_removed)
        cursor.execute(query,valori)
        db.commit()
        #label
        label_rem=tkinter.Label(window,text=f"The customer {name_removed} is removed", fg = "red")
        label_rem.grid(row = 3, column = 2 , columnspan = 2)
    else:
        tkinter.messagebox.showwarning("Error in delete customer", "Complete all the fields")

customers_list = []     # initialize an empty list of customers

class Customer(object):
    def __init__(self, name: str, surname: str, dateOfBirth: str, genre: str, 
                 email: str, phoneNumber: str) -> None:
        self.__name = name
        self.__surname = surname
        self.__dateOfBirth = dateOfBirth
        self.__genre = genre
        self.__email = email
        self.__phoneNumber = phoneNumber

    def __str__(self) -> str:
        return f"Name: {self.__name}, Surname: {self.__surname}, DateOfBirth: {self.__dateOfBirth} " \
            f"Genre: {self.__genre}, Email: {self.__email}, PhoneNumber: {self.__phoneNumber}"
    
    # metodi getter
    def getName(self) -> str:
        return self.__name
    
    def getSurname(self) -> str:
        return self.__surname
    
    def getDateOfBirth(self) -> str:
        return self.__dateOfBirth
    
    def getGenre(self) -> str:
        return self.__genre
    
    def getEmail(self) -> str:
        return self.__email
    
    def getPhoneNumber(self) -> str:
        return self.__phoneNumber
    
    # metodi setter (accesso in scrittura)
    def setName(self, newName: str) -> None:
        # Se il parametro passato 'newName' è un'istanza, un oggetto della classe 'str'
        if isinstance(newName, str):
            self.__name = newName

    def setSurname(self, newSurname: str) -> None:
        if isinstance(newSurname, str):
            self.__surname = newSurname

    def setGenre(self, newGenre: str) -> None:
        if isinstance(newGenre, str):
            self.__genre = newGenre

    def setDateOfBirth(self, newDateOfBirth: str) -> None:
        # TODO: check if the new date matches a RegEx
        if isinstance(newDateOfBirth, str):
            self.__dateOfBirth = newDateOfBirth

    def setEmail(self, newEmail: str) -> None:
        # TODO: check if the new email matches a RegEx
        if isinstance(newEmail, str):
            self.__email = newEmail

    def setPhoneNumber(self, newPhoneNumber: str) -> None:
        # TODO: check if the new phone number matches a RegEx
        if isinstance(newPhoneNumber, str):
            self.__phoneNumber = newPhoneNumber
    
window = tkinter.Tk()

# 1. Realization of widgets (Label + Entry)
name_label = tkinter.Label(window, text = "Name: ")
surname_label = tkinter.Label(window, text = "Surname: ")
dateOfBirth_label = tkinter.Label(window, text = "Date of birth: ")
genre_label = tkinter.Label(window, text = "Genre: ")
email_label = tkinter.Label(window, text = "Email: ")
phone_label = tkinter.Label(window, text = "Phone number (xxx-xxxxxxx): ")

# *** ADD CUSTOMER SECTION ***
# Entries and calendar for name, surname and date of birth fields
name_entry = tkinter.Entry(window, borderwidth = 3)
surname_entry = tkinter.Entry(window, borderwidth = 3)
dateOfBirth_entry = tkcalendar.DateEntry(window, width = 18)
# For managing genre (creation of an option menu)
options_list = ["Male", "Female", "Other"]
select_option = tkinter.StringVar(window)  
select_option.set("Select an Option")   # default value
genre_entry = tkinter.OptionMenu(window, select_option, *options_list)
# Entries for email and phone fields
email_entry = tkinter.Entry(window, borderwidth = 3)
phone_entry = tkinter.Entry(window, borderwidth = 3)
button_add = tkinter.Button(window, text = "Add Customer", background = "green",
                            foreground = "#FFFFFF", command = add_customer)

# *** REMOVE CUSTOMER SECTION ***
name_label_rem = tkinter.Label(window, text = "Removed name: ")
surname_label_rem = tkinter.Label(window, text = "Removed surname: ")
name_entry_rem = tkinter.Entry(window, borderwidth = 3)
surname_entry_rem = tkinter.Entry(window, borderwidth = 3)
button_remove = tkinter.Button(window, text = "Remove Customer",  background = "red",
                               foreground = "#FFFFFF", command = remove_customer)


# 2. Visualization of widgets on the window
# *** ADD CUSTOMER SECTION ***
name_label.grid(row = 0, column = 0)
surname_label.grid(row = 1, column = 0)
dateOfBirth_label.grid(row = 2, column = 0)
genre_label.grid(row = 3, column = 0)
email_label.grid(row = 4, column = 0)
phone_label.grid(row = 5, column = 0)
name_entry.grid(row = 0, column = 1)
surname_entry.grid(row = 1, column = 1)
dateOfBirth_entry.grid(row = 2, column = 1)
genre_entry.grid(row = 3, column = 1)
email_entry.grid(row = 4, column = 1)
phone_entry.grid(row = 5, column = 1)
button_add.grid(row = 6, column = 0, columnspan = 2)
# *** REMOVE CUSTOMER SECTION ***
name_label_rem.grid(row = 0, column = 2)
surname_label_rem.grid(row = 1, column = 2)
name_entry_rem.grid(row = 0, column = 3)
surname_entry_rem.grid(row = 1, column = 3)
button_remove.grid(row = 2, column = 2, columnspan = 2)


window.mainloop()  
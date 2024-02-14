import os  # for creating directories Admin/Customer if it is not exists.

# for date of account creation when new customer account is created.
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import messagebox


# Backend python functions code starts :
def is_valid(customer_account_number):
    try:
        customer_database = open("./database/Customer/customerDatabase.txt")
    except FileNotFoundError:
        os.makedirs("./database/Customer/customerDatabase.txt", exist_ok=True)
        print(
            "# Customer database doesn't exists!\n# New Customer database created automatically."
        )
        customer_database = open("./database/Customer/customerDatabase.txt", "a")
    else:  # if customer account  number is already allocated then this will return false. otherwise true.
        if check_credentials(customer_account_number, "DO_NOT_CHECK", 2, True):
            return False
        else:
            return True
    customer_database.close()


def check_date(date):
    try:
        birthdate_obj = datetime.strptime(date, "%d/%m/%Y")
        current_date = datetime.now()
        if current_date.date() >= birthdate_obj.date():
            return True
        else:
            return False
    except ValueError:
        return False


def is_valid_mobile(mobile_number):
    if mobile_number.__len__() == 11 and mobile_number.isnumeric():
        return True
    else:
        return False


def append_data(database_path, data):
    customer_database = open(database_path, "a")
    customer_database.write(data)


def display_account_summary(
    identity, choice
):  # choice 1 for full summary; choice 2 for only account balance.
    flag = 0
    customer_database = open("./database/Customer/customerDatabase.txt")
    output_message = ""
    for line in customer_database:
        if identity == line.replace("\n", ""):
            if choice == 1:
                output_message += "Account number : " + line.replace("\n", "") + "\n"
                customer_database.__next__()  # skipping pin
                output_message += (
                    "Current balance : "
                    + customer_database.__next__().replace("\n", "")
                    + "\n"
                )
                output_message += (
                    "Date of account creation : "
                    + customer_database.__next__().replace("\n", "")
                    + "\n"
                )
                output_message += (
                    "Name of account holder : "
                    + customer_database.__next__().replace("\n", "")
                    + "\n"
                )
                output_message += (
                    "Type of account : "
                    + customer_database.__next__().replace("\n", "")
                    + "\n"
                )
                output_message += (
                    "Date of Birth : "
                    + customer_database.__next__().replace("\n", "")
                    + "\n"
                )
                output_message += (
                    "Mobile number : "
                    + customer_database.__next__().replace("\n", "")
                    + "\n"
                )
                output_message += (
                    "Gender : " + customer_database.__next__().replace("\n", "") + "\n"
                )
                output_message += (
                    "Nationality : "
                    + customer_database.__next__().replace("\n", "")
                    + "\n"
                )
                output_message += (
                    "KYC : " + customer_database.__next__().replace("\n", "") + "\n"
                )
            else:
                customer_database.readline()  # skipped pin
                output_message += (
                    "Current balance : "
                    + customer_database.readline().replace("\n", "")
                    + "\n"
                )
            flag = 1
            break

        else:
            for index in range(11):
                fetched_line = customer_database.readline()
                if fetched_line is not None:
                    continue
                else:
                    break
    if flag == 0:
        print("\n# No account associated with the entered account number exists! #")
    return output_message


def delete_customer_account(
    identity, choice
):  # choice 1 for admin, choice 2 for customer
    customer_database = open("./database/Customer/customerDatabase.txt")
    data_collector = ""
    flag = 0
    for line in customer_database:
        if identity == line.replace("\n", ""):
            flag = 1
            for index in range(11):
                customer_database.readline()  # skipping the line
        else:
            data_collector += line
            for index in range(11):
                data_collector += customer_database.readline()
    customer_database = open("./database/Customer/customerDatabase.txt", "w")
    customer_database.write(data_collector)
    if flag == 1:
        output_message = (
            "Account with account no." + str(identity) + " closed successfully!"
        )
        if choice == 1:
            adminMenu.printMessage_outside(output_message)
        print(output_message)
    else:
        output_message = "Account not found !"
        if choice == 1:
            adminMenu.printMessage_outside(output_message)
        print(output_message)


def create_admin_account(identity, password):
    admin_database = open("./database/Admin/adminDatabase.txt", "a")
    admin_id = identity
    admin_password = password
    append_data(
        "./database/Admin/adminDatabase.txt",
        admin_id + "\n" + admin_password + "\n" + "*\n",
    )
    output_message = "Admin account created successfully !"
    adminMenu.printMessage_outside(output_message)
    print(output_message)
    admin_database.close()


def delete_admin_account(identity):
    admin_database = open("./database/Admin/adminDatabase.txt")
    data_collector = ""
    flag = 0
    for line in admin_database:
        if identity == line.replace("\n", ""):
            flag = 1
            for index in range(2):
                admin_database.readline()
        else:
            data_collector += line
            for index in range(2):
                data_collector += admin_database.readline()
    admin_database = open("./database/Admin/adminDatabase.txt", "w")
    admin_database.write(data_collector)
    if flag == 1:
        output_message = "Account with account id " + identity + " closed successfully!"
        print(output_message)
        adminMenu.printMessage_outside(output_message)
    else:
        output_message = "Account not found :("
        adminMenu.printMessage_outside(output_message)
        print(output_message)


def change_PIN(identity, new_PIN):
    customer_database = open("./database/Customer/customerDatabase.txt")
    data_collector = ""
    for line in customer_database:
        if identity == line.replace("\n", ""):
            data_collector += line  # ID
            data_collector += str(new_PIN) + "\n"  # PIN changed
            customer_database.readline()
            for index in range(10):
                data_collector += customer_database.readline()
        else:
            data_collector += line
            for index in range(11):
                data_collector += customer_database.readline()
    customer_database.close()
    customer_database = open("./database/Customer/customerDatabase.txt", "w")
    customer_database.write(data_collector)

    output_message = "PIN changed successfully."
    customerMenu.printMessage_outside(output_message)
    print(output_message)


def transaction(
    identity, amount, choice
):  # choice 1 for deposit; choice 2 for withdraw
    customer_database = open("./database/Customer/customerDatabase.txt")
    data_collector = ""
    balance = 0
    for line in customer_database:
        if identity == line.replace("\n", ""):
            data_collector += line  # ID
            data_collector += customer_database.readline()  # PIN
            balance = float(customer_database.readline().replace("\n", ""))
            if choice == 2 and balance - amount < 10000:  # Minimum balance 10000
                return -1
            else:
                if choice == 1:
                    balance += amount
                else:
                    balance -= amount
            data_collector += str(balance) + "\n"
            for index in range(9):
                data_collector += customer_database.readline()
        else:
            data_collector += line
            for index in range(11):
                data_collector += customer_database.readline()

    customer_database.close()
    customer_database = open("./database/Customer/customerDatabase.txt", "w")
    customer_database.write(data_collector)
    return balance


def check_credentials(
    identity, password, choice, admin_access
):  # checks credentials of admin/customer and returns True or False
    folder_name = "./database/Admin" if (choice == 1) else "./database/Customer"
    file_name = "/adminDatabase.txt" if (choice == 1) else "/customerDatabase.txt"

    try:
        os.makedirs(folder_name, exist_ok=True)
        database = open(folder_name + file_name, "r")
    except FileNotFoundError:
        print(
            "#",
            folder_name[2:],
            "database doesn't exists!\n# New",
            folder_name[2:],
            "database created automatically.",
        )
        database = open(folder_name + file_name, "a")
        if choice == 1:
            database.write("admin\nadmin@123\n*\n")
    else:
        is_credentials_correct = False
        for line in database:
            id_fetched = line.replace("\n", "")
            password_fetched = database.__next__().replace("\n", "")
            if id_fetched == identity:
                if (
                    (
                        password == "DO_NOT_CHECK_ADMIN"
                        and choice == 1
                        and admin_access == False
                    )
                    or (
                        password == "DO_NOT_CHECK"
                        and choice == 2
                        and admin_access == True
                    )
                    or password_fetched == password
                ):
                    is_credentials_correct = True
                    database.close()
                    return True
            if choice == 1:  # skips unnecessary lines in admin database.
                database.__next__()  # skipping line
            else:  # skips unnecessary lines in customer database.
                for index in range(10):
                    fetched_line = database.readline()
                    if fetched_line is not None:
                        continue
                    else:
                        break
        if is_credentials_correct:
            print("Success!")
        else:
            print("Failure!")

    database.close()
    return False


# Backend python functions code ends.


# Tkinter GUI code starts :
class welcomeScreen:
    def __init__(
        self, window
    ):  # __init__ is method called every time you create object from class
        # self refer to current instance from class
        self.master = window
        window.title("Bank Management System")
        window.geometry("950x445")
        window.configure(bg="#fff")

        self.img = tk.PhotoImage(file="bank99.png")
        self.Label1 = Label(window, image=self.img, bg="white").place(x=530, y=0.15222)

        self.Label2 = tk.Label(
            window,
            text="Login as:",
            fg="#57a1f8",
            bg="white",
            font=("-family {Segoe UI} -size 30 -weight bold"),
        )
        self.Label2.place(x=100, y=5)

        self.Button1 = tk.Button(
            window,
            width=30,
            pady=7,
            text="Manager",
            font=("arial", 14, "bold"),
            bg="#57a1f8",
            fg="white",
            border=0,
            command=self.selectEmployee,
        ).place(x=60, y=290)

        self.Button2 = tk.Button(
            window,
            width=15,
            pady=7,
            text="Employee",
            font=("arial", 14, "bold"),
            bg="#57a1f8",
            fg="white",
            border=0,
            command=self.a,
        ).place(x=30, y=170)

        self.Button3 = tk.Button(
            window,
            width=15,
            pady=7,
            text="custumer",
            font=("arial", 14, "bold"),
            bg="#57a1f8",
            fg="white",
            border=0,
            command=self.selectCustomer,
        ).place(x=290, y=170)

    def selectEmployee(self):
        self.master.withdraw()
        adminLogin(Toplevel(self.master))

    def selectCustomer(self):
        self.master.withdraw()
        CustomerLogin(Toplevel(self.master))

    def a(self):
        self.master.withdraw()
        b(Toplevel(self.master))


class adminLogin:
    def __init__(self, window):
        self.master = window
        self.master = window
        window.title("Manager Login")
        window.geometry("925x500+300+200")
        window.configure(bg="#fff")

        self.img = tk.PhotoImage(file="login.png")
        self.Label1 = tk.Label(window, image=self.img, bg="white").place(x=50, y=50)

        self.frame = tk.Frame(window, width=350, height=350, bg="white")
        self.frame.place(x=480, y=70)

        self.heading = tk.Label(
            self.frame,
            text="Sign in",
            fg="#57a1f8",
            bg="white",
            font=("Microsoft YaHei UI Light", 23, "bold"),
        )
        self.heading.place(x=100, y=5)

        def on_enter(e):
            self.Entry1.delete(0, "end")

        def on_leave(e):
            name = self.Entry1.get()
            if name == "":
                self.Entry1.insert(0, "Username")

        self.Entry1 = Entry(
            self.frame,
            width=25,
            fg="black",
            border=0,
            bg="white",
            font=("Microsoft YaHei UI Light", 11),
        )
        self.Entry1.place(x=30, y=80)
        self.Entry1.insert(0, "Username")
        self.Entry1.bind("<FocusIn>", on_enter)
        self.Entry1.bind("<FocusOut>", on_leave)

        tk.Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=107)

        def on_enter(e):
            self.Entry1_1.delete(0, "end")

        def on_leave(e):
            name = self.Entry1_1.get()
            if name == "":
                self.Entry1_1.insert(0, "Password")

        self.Entry1_1 = Entry(
            self.frame,
            width=25,
            fg="black",
            border=0,
            bg="white",
            font=("Microsoft YaHei UI Light", 11),
            show="*",
        )
        self.Entry1_1.place(x=30, y=150)
        self.Entry1_1.insert(0, "Password")
        self.Entry1_1.bind("<FocusIn>", on_enter)
        self.Entry1_1.bind("<FocusOut>", on_leave)

        tk.Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=177)

        self.Button = tk.Button(
            self.frame,
            width=39,
            pady=7,
            text="Sign in",
            bg="#57a1f8",
            fg="white",
            border=0,
            command=lambda: self.login(self.Entry1.get(), self.Entry1_1.get()),
        ).place(x=35, y=204)

        self.Button_back = tk.Button(
            self.frame,
            width=29,
            pady=7,
            text="Back",
            bg="#57a1f8",
            fg="white",
            border=0,
            command=self.back,
        ).place(x=65, y=290)

    def back(self):
        self.master.withdraw()
        welcomeScreen(Toplevel(self.master))

    def login(self, username, password):
        global admin_idNO
        admin_idNO = username
        if username == "admin" and password == "1234":
            self.master.withdraw()
            adminMenu(Toplevel(self.master))

        elif username != "admin" and password != "1234":
            messagebox.showerror("Invalid", "invalid username and password")

        elif password != "1234":
            messagebox.showerror("Invalid", "invalid password")

        elif username != "admin":
            messagebox.showerror("Invalid", "invalid username")


class b:
    def __init__(self, window):
        self.master = window
        self.master = window
        window.title("Employee Login")
        window.geometry("925x500+300+200")
        window.configure(bg="#fff")

        self.img = tk.PhotoImage(file="login.png")
        self.Label1 = tk.Label(window, image=self.img, bg="white").place(x=50, y=50)

        self.frame = tk.Frame(window, width=350, height=350, bg="white")
        self.frame.place(x=480, y=70)

        self.heading = tk.Label(
            self.frame,
            text="Sign in",
            fg="#57a1f8",
            bg="white",
            font=("Microsoft YaHei UI Light", 23, "bold"),
        )
        self.heading.place(x=100, y=5)

        def on_enter(e):
            self.Entry1.delete(0, "end")

        def on_leave(e):
            name = self.Entry1.get()
            if name == "":
                self.Entry1.insert(0, "Username")

        self.Entry1 = Entry(
            self.frame,
            width=25,
            fg="black",
            border=0,
            bg="white",
            font=("Microsoft YaHei UI Light", 11),
        )
        self.Entry1.place(x=30, y=80)
        self.Entry1.insert(0, "Username")
        self.Entry1.bind("<FocusIn>", on_enter)
        self.Entry1.bind("<FocusOut>", on_leave)

        tk.Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=107)

        def on_enter(e):
            self.Entry1_1.delete(0, "end")

        def on_leave(e):
            name = self.Entry1_1.get()
            if name == "":
                self.Entry1_1.insert(0, "Password")

        self.Entry1_1 = Entry(
            self.frame,
            width=25,
            fg="black",
            border=0,
            bg="white",
            font=("Microsoft YaHei UI Light", 11),
            show="*",
        )
        self.Entry1_1.place(x=30, y=150)
        self.Entry1_1.insert(0, "Password")
        self.Entry1_1.bind("<FocusIn>", on_enter)
        self.Entry1_1.bind("<FocusOut>", on_leave)

        tk.Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=177)

        self.Button = tk.Button(
            self.frame,
            width=39,
            pady=7,
            text="Sign in",
            bg="#57a1f8",
            fg="white",
            border=0,
            command=lambda: self.login(self.Entry1.get(), self.Entry1_1.get()),
        ).place(x=35, y=204)

        self.Button_back = tk.Button(
            self.frame,
            width=29,
            pady=7,
            text="Back",
            bg="#57a1f8",
            fg="white",
            border=0,
            command=self.back,
        ).place(x=65, y=290)

    def back(self):
        self.master.withdraw()
        welcomeScreen(Toplevel(self.master))

    def login(self, admin_id, admin_password):
        global admin_idNO
        admin_idNO = admin_id
        if check_credentials(admin_id, admin_password, 1, True):
            self.master.withdraw()
            cMenu(Toplevel(self.master))
        else:
            messagebox.showerror("Invalid", "Invalid Credentials!")


class CustomerLogin:
    def __init__(self, window):
        self.master = window
        window.title("Customer Login")
        window.geometry("925x500+300+200")
        window.configure(bg="#fff")

        self.img = tk.PhotoImage(file="login.png")
        self.Label1 = tk.Label(window, image=self.img, bg="white").place(x=50, y=50)

        self.frame = tk.Frame(window, width=350, height=350, bg="white")
        self.frame.place(x=480, y=70)

        self.heading = tk.Label(
            self.frame,
            text="Sign in",
            fg="#57a1f8",
            bg="white",
            font=("Microsoft YaHei UI Light", 23, "bold"),
        )
        self.heading.place(x=100, y=5)

        def on_enter(e):
            self.Entry1.delete(0, "end")

        def on_leave(e):
            name = self.Entry1.get()
            if name == "":
                self.Entry1.insert(0, "Acc-Number")

        self.Entry1 = Entry(
            self.frame,
            width=25,
            fg="black",
            border=0,
            bg="white",
            font=("Microsoft YaHei UI Light", 11),
        )
        self.Entry1.place(x=30, y=80)
        self.Entry1.insert(0, "Acc-Number")
        self.Entry1.bind("<FocusIn>", on_enter)
        self.Entry1.bind("<FocusOut>", on_leave)

        tk.Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=107)

        def on_enter(e):
            self.Entry1_1.delete(0, "end")

        def on_leave(e):
            name = self.Entry1_1.get()
            if name == "":
                self.Entry1_1.insert(0, "Password")

        self.Entry1_1 = Entry(
            self.frame,
            width=25,
            fg="black",
            border=0,
            bg="white",
            font=("Microsoft YaHei UI Light", 11),
            show="*",
        )
        self.Entry1_1.place(x=30, y=150)
        self.Entry1_1.insert(0, "Password")
        self.Entry1_1.bind("<FocusIn>", on_enter)
        self.Entry1_1.bind("<FocusOut>", on_leave)

        tk.Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=177)

        self.Button = tk.Button(
            self.frame,
            width=39,
            pady=7,
            text="Sign in",
            bg="#57a1f8",
            fg="white",
            border=0,
            command=lambda: self.login(self.Entry1.get(), self.Entry1_1.get()),
        ).place(x=35, y=204)

        self.Button_back = tk.Button(
            self.frame,
            width=29,
            pady=7,
            text="Back",
            bg="#57a1f8",
            fg="white",
            border=0,
            command=self.back,
        ).place(x=65, y=290)

    def back(self):
        self.master.withdraw()
        welcomeScreen(Toplevel(self.master))

    def login(self, customer_account_number, customer_PIN):
        if check_credentials(customer_account_number, customer_PIN, 2, False):
            global customer_accNO
            customer_accNO = str(customer_account_number)
            self.master.withdraw()
            customerMenu(Toplevel(self.master))
        else:
            messagebox.showerror("Invalid", "Invalid Credentials!")


class cMenu:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+329+153")
        window.title("Admin Section")
        window.configure(background="#d8d8d8")

        self.Labelframe1 = tk.LabelFrame(
            window,
            relief="groove",
            font="-family {Segoe UI} -size 13 -weight bold",
            foreground="#001c37",
            text="Select your option",
            background="#fffffe",
        )
        self.Labelframe1.place(relx=0.081, rely=0.081, relheight=0.415, relwidth=0.848)

        self.Button1 = tk.Button(
            self.Labelframe1,
            background="#00254a",
            foreground="#ffffff",
            borderwidth="0",
            font="-family {Segoe UI} -size 11",
            text="Close bank account",
            command=self.closeAccount,
        )
        self.Button1.place(
            relx=0.667, rely=0.195, height=34, width=181, bordermode="ignore"
        )

        self.Button2 = tk.Button(
            self.Labelframe1,
            background="#00254a",
            foreground="#ffffff",
            borderwidth="0",
            font="-family {Segoe UI} -size 11",
            text="Create bank account",
            command=self.createCustaccount,
        )
        self.Button2.place(
            relx=0.04, rely=0.195, height=34, width=181, bordermode="ignore"
        )

        self.Button3 = tk.Button(
            self.Labelframe1,
            background="#00254a",
            foreground="#ffffff",
            borderwidth="0",
            font="-family {Segoe UI} -size 11",
            text="Exit",
            command=self.exit,
        )
        self.Button3.place(
            relx=0.667, rely=0.683, height=34, width=181, bordermode="ignore"
        )

        self.Button6 = tk.Button(
            self.Labelframe1,
            background="#00254a",
            foreground="#ffffff",
            borderwidth="0",
            font="-family {Segoe UI} -size 11",
            text="Check account summary",
            command=self.showAccountSummary,
        )
        self.Button6.place(
            relx=0.04, rely=0.683, height=34, width=181, bordermode="ignore"
        )

        global Frame1
        Frame1 = tk.Frame(
            window, relief="groove", borderwidth="2", background="#fffffe"
        )
        Frame1.place(relx=0.081, rely=0.547, relheight=0.415, relwidth=0.848)

    def closeAccount(self):
        CloseAccountByAdmin(Toplevel(self.master))

    def createCustaccount(self):
        createCustomerAccount(Toplevel(self.master))

    def showAccountSummary(self):
        checkAccountSummary(Toplevel(self.master))

    def printAccountSummary(identity):
        # clearing the frame
        for widget in Frame1.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output = display_account_summary(identity, 1)
        output_message = Label(Frame1, text=output, background="#fffffe")
        output_message.pack(pady=20)

    def printMessage_outside(output):
        # clearing the frame
        for widget in Frame1.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output_message = Label(Frame1, text=output, background="#fffffe")
        output_message.pack(pady=20)

    def exit(self):
        self.master.withdraw()
        adminLogin(Toplevel(self.master))


class adminMenu:
    def __init__(self, window):
        self.master = window
        window.geometry("743x494+329+153")
        window.title("Admin Section")
        window.configure(background="#d8d8d8")

        self.Labelframe1 = tk.LabelFrame(
            window,
            relief="groove",
            font="-family {Segoe UI} -size 13 -weight bold",
            foreground="#001c37",
            text="Select your option",
            background="#fffffe",
        )
        self.Labelframe1.place(relx=0.081, rely=0.081, relheight=0.415, relwidth=0.848)

        self.Button1 = tk.Button(
            self.Labelframe1,
            background="#00254a",
            foreground="#ffffff",
            borderwidth="0",
            font="-family {Segoe UI} -size 11",
            text="Close bank account",
            command=self.closeAccount,
        )
        self.Button1.place(
            relx=0.667, rely=0.195, height=34, width=181, bordermode="ignore"
        )

        self.Button2 = tk.Button(
            self.Labelframe1,
            background="#00254a",
            foreground="#ffffff",
            borderwidth="0",
            font="-family {Segoe UI} -size 11",
            text="Create bank account",
            command=self.createCustaccount,
        )
        self.Button2.place(
            relx=0.04, rely=0.195, height=34, width=181, bordermode="ignore"
        )

        self.Button3 = tk.Button(
            self.Labelframe1,
            background="#00254a",
            foreground="#ffffff",
            borderwidth="0",
            font="-family {Segoe UI} -size 11",
            text="Exit",
            command=self.exit,
        )
        self.Button3.place(
            relx=0.667, rely=0.683, height=34, width=181, bordermode="ignore"
        )

        self.Button4 = tk.Button(
            self.Labelframe1,
            background="#00254a",
            foreground="#ffffff",
            borderwidth="0",
            font="-family {Segoe UI} -size 11",
            text="Create admin account",
            command=self.createAdmin,
        )
        self.Button4.place(
            relx=0.04, rely=0.439, height=34, width=181, bordermode="ignore"
        )

        self.Button5 = tk.Button(
            self.Labelframe1,
            background="#00254a",
            foreground="#ffffff",
            borderwidth="0",
            font="-family {Segoe UI} -size 11",
            text="Close admin account",
            command=self.deleteAdmin,
        )
        self.Button5.place(
            relx=0.667, rely=0.439, height=34, width=181, bordermode="ignore"
        )

        self.Button6 = tk.Button(
            self.Labelframe1,
            background="#00254a",
            foreground="#ffffff",
            borderwidth="0",
            font="-family {Segoe UI} -size 11",
            text="Check account summary",
            command=self.showAccountSummary,
        )
        self.Button6.place(
            relx=0.04, rely=0.683, height=34, width=181, bordermode="ignore"
        )

        global Frame1
        Frame1 = tk.Frame(
            window, relief="groove", borderwidth="2", background="#fffffe"
        )
        Frame1.place(relx=0.081, rely=0.547, relheight=0.415, relwidth=0.848)

    def closeAccount(self):
        CloseAccountByAdmin(Toplevel(self.master))

    def createCustaccount(self):
        createCustomerAccount(Toplevel(self.master))

    def createAdmin(self):
        createAdmin(Toplevel(self.master))

    def deleteAdmin(self):
        deleteAdmin(Toplevel(self.master))

    def showAccountSummary(self):
        checkAccountSummary(Toplevel(self.master))

    def printAccountSummary(identity):
        # clearing the frame
        for widget in Frame1.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output = display_account_summary(identity, 1)
        output_message = Label(Frame1, text=output, background="#fffffe")
        output_message.pack(pady=20)

    def printMessage_outside(output):
        # clearing the frame
        for widget in Frame1.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output_message = Label(Frame1, text=output, background="#fffffe")
        output_message.pack(pady=20)

    def exit(self):
        self.master.withdraw()
        adminLogin(Toplevel(self.master))


class CloseAccountByAdmin:
    def __init__(self, window):
        self.master = window
        window.geometry("411x117+498+261")
        window.title("Close customer account")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(
            window,
            background="#f2f3f4",
            text="Enter account number:",
        )
        self.Label1.place(relx=0.232, rely=0.220, height=20, width=120)

        self.Entry1 = tk.Entry(
            window,
            background="#cae4ff",
        )
        self.Entry1.place(relx=0.536, rely=0.220, height=20, relwidth=0.232)

        self.Button1 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Back",
            command=self.back,
        )
        self.Button1.place(relx=0.230, rely=0.598, height=24, width=67)

        self.Button2 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Proceed",
            command=lambda: self.submit(self.Entry1.get()),
        )
        self.Button2.place(relx=0.598, rely=0.598, height=24, width=67)

    def back(self):
        self.master.withdraw()

    def submit(self, identity):
        if not is_valid(identity):
            delete_customer_account(identity, 1)
        else:
            messagebox.showerror("Invalid", "Account doesn't exist!")
            return
        self.master.withdraw()


class createCustomerAccount:
    def __init__(self, window):
        self.master = window
        window.geometry("411x403+437+152")
        window.title("Create account")
        window.configure(background="#f2f3f4")

        self.Entry1 = tk.Entry(
            window,
            background="#cae4ff",
        )
        self.Entry1.place(relx=0.511, rely=0.027, height=20, relwidth=0.302)

        self.Label1 = tk.Label(
            window,
            background="#f2f3f4",
            text="Account number:",
        )
        self.Label1.place(relx=0.219, rely=0.025, height=26, width=120)

        self.Label2 = tk.Label(
            window,
            background="#f2f3f4",
            text="Full name:",
        )
        self.Label2.place(relx=0.316, rely=0.099, height=27, width=75)

        self.Entry2 = tk.Entry(
            window,
            background="#cae4ff",
        )
        self.Entry2.place(relx=0.511, rely=0.099, height=20, relwidth=0.302)

        self.Label3 = tk.Label(
            window,
            background="#f2f3f4",
            text="Account type:",
        )
        self.Label3.place(relx=0.287, rely=0.169, height=26, width=83)

        global acc_type
        acc_type = StringVar()

        self.Radiobutton1 = tk.Radiobutton(
            window,
            background="#f2f3f4",
            justify="left",
            text="Savings",
            variable=acc_type,
            value="Savings",
        )
        self.Radiobutton1.place(relx=0.511, rely=0.174, relheight=0.057, relwidth=0.151)

        self.Radiobutton1_1 = tk.Radiobutton(
            window,
            background="#f2f3f4",
            justify="left",
            text="Current",
            variable=acc_type,
            value="Current",
        )
        self.Radiobutton1_1.place(
            relx=0.706, rely=0.174, relheight=0.057, relwidth=0.175
        )

        self.Radiobutton1.deselect()
        self.Radiobutton1_1.deselect()

        self.Label5 = tk.Label(
            window,
            background="#f2f3f4",
            text="Mobile number:",
        )
        self.Label5.place(relx=0.268, rely=0.323, height=22, width=85)

        self.Label4 = tk.Label(
            window,
            background="#f2f3f4",
            text="Birth date (DD/MM/YYYY):",
        )
        self.Label4.place(relx=0.090, rely=0.238, height=27, width=175)

        self.Entry5 = tk.Entry(
            window,
            background="#cae4ff",
        )
        self.Entry5.place(relx=0.511, rely=0.323, height=20, relwidth=0.302)

        self.Entry4 = tk.Entry(
            window,
            background="#cae4ff",
        )
        self.Entry4.place(relx=0.511, rely=0.248, height=20, relwidth=0.302)

        self.Label6 = tk.Label(
            window,
            background="#f2f3f4",
            text="Gender:",
        )
        self.Label6.place(relx=0.345, rely=0.402, height=15, width=65)

        global gender
        gender = StringVar()

        self.Radiobutton3 = tk.Radiobutton(
            window,
            background="#f2f3f4",
            justify="left",
            text="""Male""",
            variable=gender,
            value="Male",
        )
        self.Radiobutton3.place(relx=0.481, rely=0.397, relheight=0.055, relwidth=0.175)

        self.Radiobutton4 = tk.Radiobutton(
            window,
            background="#f2f3f4",
            justify="left",
            text="Female",
            variable=gender,
            value="Female",
        )
        self.Radiobutton4.place(relx=0.706, rely=0.397, relheight=0.055, relwidth=0.175)

        self.Radiobutton3.deselect()
        self.Radiobutton4.deselect()

        self.Label7 = tk.Label(
            window,
            background="#f2f3f4",
            text="Nationality:",
        )
        self.Label7.place(relx=0.309, rely=0.471, height=21, width=75)

        self.Entry7 = tk.Entry(
            window,
            background="#cae4ff",
        )
        self.Entry7.place(relx=0.511, rely=0.471, height=20, relwidth=0.302)

        self.Entry9 = tk.Entry(
            window,
            show="*",
            background="#cae4ff",
        )
        self.Entry9.place(relx=0.511, rely=0.623, height=20, relwidth=0.302)

        self.Entry10 = tk.Entry(
            window,
            show="*",
            background="#cae4ff",
        )
        self.Entry10.place(relx=0.511, rely=0.7, height=20, relwidth=0.302)

        self.Entry11 = tk.Entry(
            window,
            background="#cae4ff",
        )
        self.Entry11.place(relx=0.511, rely=0.777, height=20, relwidth=0.302)

        self.Label9 = tk.Label(
            window,
            background="#f2f3f4",
            text="PIN:",
        )
        self.Label9.place(relx=0.399, rely=0.62, height=21, width=35)

        self.Label10 = tk.Label(
            window,
            background="#f2f3f4",
            text="Re-enter PIN:",
        )
        self.Label10.place(relx=0.292, rely=0.695, height=21, width=75)

        self.Label11 = tk.Label(
            window,
            background="#f2f3f4",
            text="Initial balance:",
        )
        self.Label11.place(relx=0.292, rely=0.779, height=21, width=75)

        self.Button1 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Back",
            command=self.back,
        )
        self.Button1.place(relx=0.243, rely=0.893, height=24, width=67)

        self.Button2 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Proceed",
            command=lambda: self.create_acc(
                self.Entry1.get(),
                self.Entry2.get(),
                acc_type.get(),
                self.Entry4.get(),
                self.Entry5.get(),
                gender.get(),
                self.Entry7.get(),
                self.Entry8.get(),
                self.Entry9.get(),
                self.Entry10.get(),
                self.Entry11.get(),
            ),
        )
        self.Button2.place(relx=0.633, rely=0.893, height=24, width=67)

        self.Label8 = tk.Label(
            window,
            background="#f2f3f4",
            text="KYC document name:",
        )
        self.Label8.place(relx=0.18, rely=0.546, height=24, width=122)

        self.Entry8 = tk.Entry(
            window,
            background="#cae4ff",
        )
        self.Entry8.place(relx=0.511, rely=0.546, height=20, relwidth=0.302)

    def back(self):
        self.master.withdraw()

    def create_acc(
        self,
        customer_account_number,
        name,
        account_type,
        date_of_birth,
        mobile_number,
        gender,
        nationality,
        KYC_document,
        PIN,
        confirm_PIN,
        initial_balance,
    ):
        if is_valid(customer_account_number) and customer_account_number.isnumeric():
            if name != "":
                if account_type == "Savings" or account_type == "Current":
                    if check_date(date_of_birth):
                        if is_valid_mobile(mobile_number):
                            if gender == "Male" or gender == "Female":
                                if nationality.__len__() != 0:
                                    if KYC_document.__len__() != 0:
                                        if PIN.isnumeric() and PIN.__len__() == 4:
                                            if confirm_PIN == PIN:
                                                if initial_balance.isnumeric():
                                                    output_message = "Customer account created successfully!"
                                                    print(output_message)
                                                    adminMenu.printMessage_outside(
                                                        output_message
                                                    )
                                                else:
                                                    messagebox.showerror(
                                                        "Invalid",
                                                        "Invalid balance!",
                                                    )
                                                    return
                                            else:
                                                messagebox.showerror(
                                                    "Invalid", "PIN mismatch!"
                                                )
                                                return
                                        else:
                                            messagebox.showerror(
                                                "Invalid", "Invalid PIN!"
                                            )
                                            return
                                    else:
                                        messagebox.showerror(
                                            "Invalid", "Enter KYC document!"
                                        )
                                        return
                                else:
                                    messagebox.showerror(
                                        "Invalid", "Enter Nationality!"
                                    )
                                    return
                            else:
                                messagebox.showerror("Invalid", "Select gender!")
                                return
                        else:
                            messagebox.showerror("Invalid", "Invalid mobile number!")
                            return
                    else:
                        messagebox.showerror("Invalid", "Invalid date!")
                        return
                else:
                    messagebox.showerror("Invalid", "Select account type!")
                    return
            else:
                messagebox.showerror("Invalid", "Name can't be empty!")
                return
        else:
            messagebox.showerror("Invalid", "Acc-number is invalid!")
            return

        today = datetime.today()  # set date of account creation
        date_of_account_creation = today.strftime("%d/%m/%Y")

        # adding in database
        data = (
            customer_account_number
            + "\n"
            + PIN
            + "\n"
            + initial_balance
            + "\n"
            + date_of_account_creation
            + "\n"
            + name
            + "\n"
            + account_type
            + "\n"
            + date_of_birth
            + "\n"
            + mobile_number
            + "\n"
            + gender
            + "\n"
            + nationality
            + "\n"
            + KYC_document
            + "\n"
            + "*\n"
        )
        append_data("./database/Customer/customerDatabase.txt", data)

        self.master.withdraw()


class createAdmin:
    def __init__(self, window):
        self.master = window
        window.geometry("411x150+512+237")
        window.title("Create admin account")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(
            window,
            background="#f2f3f4",
            text="Enter admin ID:",
        )
        self.Label1.place(relx=0.219, rely=0.067, height=27, width=104)

        self.Label2 = tk.Label(
            window,
            background="#f2f3f4",
            text="Enter password:",
        )
        self.Label2.place(relx=0.219, rely=0.267, height=27, width=104)

        self.Entry1 = tk.Entry(
            window,
            background="#cae4ff",
        )
        self.Entry1.place(relx=0.487, rely=0.087, height=20, relwidth=0.326)

        self.Entry2 = tk.Entry(
            window,
            show="*",
            background="#cae4ff",
        )
        self.Entry2.place(relx=0.487, rely=0.287, height=20, relwidth=0.326)

        self.Label3 = tk.Label(
            window,
            background="#f2f3f4",
            text="Confirm password:",
        )
        self.Label3.place(relx=0.195, rely=0.467, height=27, width=104)

        self.Entry3 = tk.Entry(
            window,
            show="*",
            background="#cae4ff",
        )
        self.Entry3.place(relx=0.487, rely=0.487, height=20, relwidth=0.326)

        self.Button1 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Proceed",
            command=lambda: self.create_admin_account(
                self.Entry1.get(), self.Entry2.get(), self.Entry3.get()
            ),
        )
        self.Button1.place(relx=0.598, rely=0.733, height=24, width=67)

        self.Button2 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Back",
            command=self.back,
        )
        self.Button2.place(relx=0.230, rely=0.733, height=24, width=67)

    def back(self):
        self.master.withdraw()

    def create_admin_account(self, identity, password, confirm_password):
        if check_credentials(identity, "DO_NOT_CHECK_ADMIN", 1, False):
            messagebox.showerror("Invalid", "ID is unavailable!")
        else:
            if password == confirm_password and len(password) != 0:
                create_admin_account(identity, password)
                self.master.withdraw()
            else:
                if password != confirm_password:
                    messagebox.showerror("Invalid", "Password Mismatch!")
                else:
                    messagebox.showerror("Invalid", "Invalid password!")


class deleteAdmin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x117+504+268")
        window.title("Delete admin account")
        window.configure(background="#f2f3f4")

        self.Entry1 = tk.Entry(
            window,
            background="#cae4ff",
        )
        self.Entry1.place(relx=0.487, rely=0.092, height=20, relwidth=0.277)

        self.Label1 = tk.Label(
            window,
            background="#f2f3f4",
            text="Enter admin ID:",
        )
        self.Label1.place(relx=0.219, rely=0.092, height=21, width=104)

        self.Label2 = tk.Label(
            window,
            background="#f2f3f4",
            text="Enter password:",
        )
        self.Label2.place(relx=0.209, rely=0.33, height=21, width=109)

        self.Entry1_1 = tk.Entry(
            window,
            show="*",
            background="#cae4ff",
        )
        self.Entry1_1.place(relx=0.487, rely=0.33, height=20, relwidth=0.277)

        self.Button1 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Back",
            command=self.back,
        )
        self.Button1.place(relx=0.243, rely=0.642, height=24, width=67)

        self.Button2 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Proceed",
            command=lambda: self.delete_admin(self.Entry1.get(), self.Entry1_1.get()),
        )
        self.Button2.place(relx=0.608, rely=0.642, height=24, width=67)

    def delete_admin(self, admin_id, password):
        if check_credentials(admin_id, password, 1, True):
            delete_admin_account(admin_id)
            self.master.withdraw()
        else:
            messagebox.showerror("Invalid", "Invalid Credentials!")

    def back(self):
        self.master.withdraw()


class customerMenu:
    def __init__(self, window):
        self.master = window
        window.geometry("743x494+329+153")
        window.title("Customer Section")
        window.configure(background="#d8d8d8")

        self.Labelframe1 = tk.LabelFrame(
            window,
            font="-family {Segoe UI} -size 13 -weight bold",
            text="Select your option",
            background="#fffffe",
        )
        self.Labelframe1.place(relx=0.081, rely=0.081, relheight=0.415, relwidth=0.848)

        self.Button1 = tk.Button(
            self.Labelframe1,
            command=self.selectWithdraw,
            background="#39a9fc",
            foreground="#ffffff",
            font="-family {Segoe UI} -size 11",
            borderwidth="0",
            text="Withdraw",
        )
        self.Button1.place(
            relx=0.667, rely=0.195, height=34, width=181, bordermode="ignore"
        )

        self.Button2 = tk.Button(
            self.Labelframe1,
            command=self.selectDeposit,
            background="#39a9fc",
            foreground="#ffffff",
            font="-family {Segoe UI} -size 11",
            borderwidth="0",
            text="Deposit",
        )
        self.Button2.place(
            relx=0.04, rely=0.195, height=34, width=181, bordermode="ignore"
        )

        self.Button3 = tk.Button(
            self.Labelframe1,
            command=self.exit,
            background="#39a9fc",
            foreground="#ffffff",
            font="-family {Segoe UI} -size 11",
            borderwidth="0",
            text="Exit",
        )
        self.Button3.place(
            relx=0.667, rely=0.683, height=34, width=181, bordermode="ignore"
        )

        self.Button4 = tk.Button(
            self.Labelframe1,
            command=self.selectChangePIN,
            background="#39a9fc",
            foreground="#ffffff",
            font="-family {Segoe UI} -size 11",
            borderwidth="0",
            text="Change PIN",
        )
        self.Button4.place(
            relx=0.04, rely=0.439, height=34, width=181, bordermode="ignore"
        )

        self.Button5 = tk.Button(
            self.Labelframe1,
            command=self.selectCloseAccount,
            background="#39a9fc",
            foreground="#ffffff",
            font="-family {Segoe UI} -size 11",
            borderwidth="0",
            text="Close account",
        )
        self.Button5.place(
            relx=0.667, rely=0.439, height=34, width=181, bordermode="ignore"
        )

        self.Button6 = tk.Button(
            self.Labelframe1,
            background="#39a9fc",
            foreground="#ffffff",
            font="-family {Segoe UI} -size 11",
            borderwidth="0",
            text="Check your balance",
            command=self.checkBalance,
        )
        self.Button6.place(
            relx=0.04, rely=0.683, height=34, width=181, bordermode="ignore"
        )

        global Frame1_1_2
        Frame1_1_2 = tk.Frame(
            window, relief="groove", borderwidth="2", background="#fffffe"
        )
        Frame1_1_2.place(relx=0.081, rely=0.547, relheight=0.415, relwidth=0.848)

    def selectDeposit(self):
        depositMoney(Toplevel(self.master))

    def selectWithdraw(self):
        withdrawMoney(Toplevel(self.master))

    def selectChangePIN(self):
        changePIN(Toplevel(self.master))

    def selectCloseAccount(self):
        self.master.withdraw()
        closeAccount(Toplevel(self.master))

    def exit(self):
        self.master.withdraw()
        CustomerLogin(Toplevel(self.master))

    def checkBalance(self):
        output = display_account_summary(customer_accNO, 2)
        self.printMessage(output)
        print("check balance function called.")

    def printMessage(self, output):
        # clearing the frame
        for widget in Frame1_1_2.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output_message = Label(Frame1_1_2, text=output, background="#fffffe")
        output_message.pack(pady=20)

    def printMessage_outside(output):
        # clearing the frame
        for widget in Frame1_1_2.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output_message = Label(Frame1_1_2, text=output, background="#fffffe")
        output_message.pack(pady=20)


class depositMoney:
    def __init__(self, window):
        self.master = window
        window.geometry("411x117+519+278")
        window.title("Deposit money")
        window.configure(borderwidth="2")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(
            window,
            background="#f2f3f4",
            text="Enter amount to deposit :",
        )
        self.Label1.place(relx=0.146, rely=0.171, height=21, width=164)

        self.Entry1 = tk.Entry(
            window,
            background="#cae4ff",
        )
        self.Entry1.place(relx=0.535, rely=0.171, height=20, relwidth=0.253)

        self.Button1 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Proceed",
            command=lambda: self.submit(self.Entry1.get()),
        )
        self.Button1.place(relx=0.56, rely=0.598, height=24, width=67)

        self.Button2 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Back",
            command=self.back,
        )
        self.Button2.place(relx=0.268, rely=0.598, height=24, width=67)

    def submit(self, amount):
        if amount.isnumeric():
            if 25000 >= float(amount) > 0:
                output = transaction(customer_accNO, float(amount), 1)
            else:
                if float(amount) > 25000:
                    messagebox.showerror("Invalid", "Limit exceeded!")
                else:
                    messagebox.showerror("Invalid", "Positive value expected!")
                return
        else:
            messagebox.showerror("Invalid", "Invalid amount!")
            return
        if output == -1:
            messagebox.showerror("Invalid", "Transaction failed!")
            return
        else:
            output = (
                "Amount of pounds "
                + str(amount)
                + " deposited successfully.\nUpdated balance : "
                + str(output)
            )
            customerMenu.printMessage_outside(output)
            self.master.withdraw()

    def back(self):
        self.master.withdraw()


class withdrawMoney:
    def __init__(self, window):
        self.master = window
        window.geometry("411x117+519+278")
        window.title("Withdraw money")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(
            window,
            background="#f2f3f4",
            font="-family {Segoe UI} -size 9",
            text="Enter amount to withdraw :",
        )
        self.Label1.place(relx=0.146, rely=0.171, height=21, width=164)

        self.Entry1 = tk.Entry(
            window,
            background="#cae4ff",
        )
        self.Entry1.place(relx=0.535, rely=0.171, height=20, relwidth=0.253)

        self.Button1 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Proceed",
            command=lambda: self.submit(self.Entry1.get()),
        )
        self.Button1.place(relx=0.56, rely=0.598, height=24, width=67)

        self.Button2 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Back",
            command=self.back,
        )
        self.Button2.place(relx=0.268, rely=0.598, height=24, width=67)

    def submit(self, amount):
        if amount.isnumeric():
            if 25000 >= float(amount) > 0:
                output = transaction(customer_accNO, float(amount), 2)
            else:
                if float(amount) > 25000:
                    messagebox.showerror("Invalid", "Limit exceeded!")
                else:
                    messagebox.showerror("Invalid", "Positive value expected!")
                return
        else:
            messagebox.showerror("Invalid", "Invalid amount!")
            return
        if output == -1:
            messagebox.showerror("Invalid", "Transaction failed!")
            return
        else:
            output = (
                "Amount of pounds "
                + str(amount)
                + " withdrawn successfully.\nUpdated balance : "
                + str(output)
            )
            customerMenu.printMessage_outside(output)
            self.master.withdraw()

    def back(self):
        self.master.withdraw()


class changePIN:
    def __init__(self, window):
        self.master = window
        window.geometry("411x111+505+223")
        window.title("Change PIN")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(
            window,
            background="#f2f3f4",
            text="Enter new PIN:",
        )
        self.Label1.place(relx=0.243, rely=0.144, height=21, width=93)

        self.Label2 = tk.Label(
            window,
            background="#f2f3f4",
            text="""Confirm PIN:""",
        )
        self.Label2.place(relx=0.268, rely=0.414, height=21, width=82)

        self.Entry1 = tk.Entry(
            window,
            show="*",
            background="#cae4ff",
        )
        self.Entry1.place(relx=0.528, rely=0.144, height=20, relwidth=0.229)

        self.Entry2 = tk.Entry(
            window,
            show="*",
            background="#cae4ff",
        )
        self.Entry2.place(relx=0.528, rely=0.414, height=20, relwidth=0.229)

        self.Button1 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Proceed",
            command=lambda: self.submit(self.Entry1.get(), self.Entry2.get()),
        )
        self.Button1.place(relx=0.614, rely=0.721, height=24, width=67)

        self.Button2 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Back",
            command=self.back,
        )
        self.Button2.place(relx=0.214, rely=0.721, height=24, width=67)

    def submit(self, new_PIN, confirm_new_PIN):
        if (
            new_PIN == confirm_new_PIN
            and str(new_PIN).__len__() == 4
            and new_PIN.isnumeric()
        ):
            change_PIN(customer_accNO, new_PIN)
            self.master.withdraw()
        else:
            if new_PIN != confirm_new_PIN:
                messagebox.showerror("Invalid", "PIN mismatch!")
            elif str(new_PIN).__len__() != 4:
                messagebox.showerror("Invalid", "PIN length must be 4!")
            else:
                messagebox.showerror("Invalid", "Invalid PIN!")
            return

    def back(self):
        self.master.withdraw()


class closeAccount:  # close account by customer
    def __init__(self, window):
        self.master = window
        window.geometry("411x117+498+261")
        window.title("Close Account")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(
            window,
            background="#f2f3f4",
            text="Enter your PIN:",
        )
        self.Label1.place(relx=0.268, rely=0.256, height=21, width=94)

        self.Entry1 = tk.Entry(
            window,
            show="*",
            background="#cae4ff",
        )
        self.Entry1.place(relx=0.511, rely=0.256, height=20, relwidth=0.229)

        self.Button1 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Proceed",
            command=lambda: self.submit(self.Entry1.get()),
        )
        self.Button1.place(relx=0.614, rely=0.712, height=24, width=67)

        self.Button2 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Back",
            command=self.back,
        )
        self.Button2.place(relx=0.214, rely=0.712, height=24, width=67)

    def submit(self, PIN):
        print("Submit pressed.")
        print(customer_accNO, PIN)
        if check_credentials(customer_accNO, PIN, 2, False):
            print("Correct accepted.")
            delete_customer_account(customer_accNO, 2)
            self.master.withdraw()
            CustomerLogin(Toplevel(self.master))
        else:
            print("Incorrect accepted.")
            messagebox.showerror("Invalid", "Invalid PIN!")

    def back(self):
        self.master.withdraw()
        customerMenu(Toplevel(self.master))


class checkAccountSummary:
    def __init__(self, window):
        self.master = window
        window.geometry("411x117+498+261")
        window.title("Check Account Summary")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(
            window,
            background="#f2f3f4",
            text="Enter ID :",
        )
        self.Label1.place(relx=0.268, rely=0.256, height=21, width=94)

        self.Entry1 = tk.Entry(
            window,
            background="#cae4ff",
        )
        self.Entry1.place(relx=0.511, rely=0.256, height=20, relwidth=0.229)

        self.Button1 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Proceed",
            command=lambda: self.submit(self.Entry1.get()),
        )
        self.Button1.place(relx=0.614, rely=0.712, height=24, width=67)

        self.Button2 = tk.Button(
            window,
            background="#004080",
            foreground="#ffffff",
            borderwidth="0",
            text="Back",
            command=self.back,
        )
        self.Button2.place(relx=0.214, rely=0.712, height=24, width=67)

    def back(self):
        self.master.withdraw()

    def submit(self, identity):
        if not is_valid(identity):
            adminMenu.printAccountSummary(identity)
        else:
            messagebox.showerror("Invalid", "Id doesn't exist!")
            return
        self.master.withdraw()


root = tk.Tk()
top = welcomeScreen(root)
root.mainloop()

# Tkinter GUI code ends.

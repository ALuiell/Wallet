import sqlite3

"""
                                                Database TABLE
User_accounts Table
Number: Unique account number (integer).
Type: Account type (text).
Name: Account holder's name (text).
Balance: Account balance (float).

TransactionAll Table
Number: Account number to which the transaction is associated (integer).
Type: Type of transaction (text).
Category: Transaction category (text).
TransactionDate: Transaction date (in the format "yyyy.mm.dd").
TransactionID: Unique transaction identifier (text).
Amount: Transaction amount (float).

Transaction_Transfer Table
From_number: Sender's account number (integer).
To_number: Receiver's account number (integer).
TransactionDate: Transaction date (in the format "yyyy.mm.dd").
TransactionID: Unique transaction identifier (text).
Amount: Transaction amount (float).

Category Table
Name: category name
"""


class DatabaseManager:

    def __init__(self, database_path):
        self.conn = None
        self.database_path = database_path

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.database_path)
            if self.conn:
                print('Підключення до бази даних пройшло успішно!')

        except sqlite3.Error as e:
            print('Виникла помилка під час підключення до бази даних:', str(e))

    def create_cursor(self):
        if self.conn:
            print(f"Курсор бази данних для шляха {self.database_path} створено")
            return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        print("DB Close")
        if self.conn:
            self.conn.close()


# ----------------------------------------PATH DATABASE FILE----------------------------------------------------
# database_path = input("Database path: ")
db = DatabaseManager("F:\\Python\\Wallet\\Wallet.db")
db.connect()
cursor = db.create_cursor()

# --------------------------------------------------------------------------------------------------------------
cursor.execute("SELECT Name FROM Category")
categories = cursor.fetchall()

# lst standard categories and user categories
user_categories = [category[0] for category in categories]

# ---------------------------------------------------------------------------------------------------------------
cursor.execute("SELECT Number FROM User_Accounts")
numbers = cursor.fetchall()

# lst number accounts for verification
lst_accounts = [str(number[0]) for number in numbers]

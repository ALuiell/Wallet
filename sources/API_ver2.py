import sqlite3

"""
1.rework under ORM
2. create class under Transaction, Category, Users
3. create class under display
"""


class DatabaseManager:
    def __init__(self, database_path):
        self.conn = None
        self.database_path = database_path
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.database_path)
            if self.conn:
                print('Підключення до бази даних пройшло успішно!')
        except sqlite3.Error as e:
            raise RuntimeError(f'Виникла помилка під час підключення до бази даних: {str(e)}')

    def create_cursor(self):
        if self.conn:
            return self.conn.cursor()

    def execute_query(self, query, params=None):
        cursor = self.create_cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
        except Exception as e:
            print(f'Помилка під час виконання запиту: {str(e)}')
        finally:
            cursor.close()

    def get_categories(self, cursor):
        query = "SELECT Name FROM Category"
        try:
            cursor.execute(query)
            categories = cursor.fetchall()
            return [category[0] for category in categories]
        except sqlite3.Error:
            return "Курсор не створено"

    def get_account_numbers(self, cursor):
        query = "SELECT Number FROM User_Accounts"
        try:
            cursor.execute(query)
            numbers = cursor.fetchall()
            return [str(number[0]) for number in numbers]
        except sqlite3.Error:
            return "Курсор не створено"

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()

    def close(self):
        print("DB Close")
        if self.conn:
            self.conn.close()


class DisplayManager:
    def __init__(self):
        pass


class Users:
    def __init__(self):
        pass

    def add_user(self):
        pass

    def update_user_info(self):
        pass

    def delete_user(self):
        pass


class CategoryManager:

    def __init__(self):
        pass

    def add_category(self):
        pass

    def update_category(self):
        pass

    def delete_category(self):
        pass


class TransactionManager(DatabaseManager):

    def add_transaction(self):
        pass

    def delete_transaction(self):
        pass

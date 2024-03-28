# https://docs.peewee-orm.com/en/latest/
from models import Category, TransactionAll, User_Accounts
from peewee import *


class DatabaseManager:
    def __init__(self, database_path):
        self.database_path = database_path
        self.database = SqliteDatabase(self.database_path)
        self.database.create_tables([Category, TransactionAll, User_Accounts], safe=True)

    def connect(self):
        try:
            self.database.connect()
        except Exception as e:
            raise RuntimeError(f'Виникла помилка під час підключення до бази даних: {str(e)}')

    @staticmethod
    def create(model_class, data):
        # update under transaction
        """
            Insert data into a table.

            Args:
                model_class: Peewee model class for the table where data will be inserted.
                data (dict): A dictionary containing column names as keys and values as values.

            Example:
                - For a single-column insertion:
                  create_record(Category, {"Name": "Pool"})

                - For multi-column insertion:
                  create_record(UserAccount, {"Number": '27412281', "Type": 'Дебетовий',
                  "Name": 'Alexander James Anderson', "Balance": "0"})
        """

        try:
            model_class.create(**data)
        except Exception as e:
            print(f"Error during data insertion: {e}")

    @staticmethod
    def update(model_class, set_column, set_value, where_column, where_value):
        """
            Update records in the database.

            Args:
                model_class: The Peewee model representing the database table.
                set_column (str): The name of the column to be updated.
                set_value: The new value to replace the existing values in the specified column.
                where_column (str): The name of the column used to determine which records to update.
                where_value: The value used in the condition to select records for updating.
        """
        try:
            query = model_class.update({set_column: set_value}).where(getattr(model_class, where_column) == where_value)
            query.execute()
        except Exception as e:
            print(f"Error during data updation: {e}")

    @staticmethod
    def delete(model_class, where_field, where_value):
        """
        Delete data into a table.

        Args:
             model_class: The Peewee model class for the table in which the data will be inserted.
             where_field (str): The name of the column where the desired value is located.
             where_value: The value used in the condition to select records for deleting.

        """
        try:
            query = model_class.delete().where(getattr(model_class, where_field) == where_value)
            query.execute()
        except Exception as e:
            print(f"Error during data deletion: {e}")

    @staticmethod
    def verify(model_class, where_field, where_value):
        """
        return True if exists
        return False if does not

        """
        return model_class.select().where(getattr(model_class, where_field) == where_value).exists()

    def close(self):
        self.database.close()
        print("Кінець")

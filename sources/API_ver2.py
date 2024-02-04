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

    def execute_select(self, query, params=None):
        cursor = self.create_cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f'Помилка під час виконання запиту SELECT: {str(e)}')
        finally:
            cursor.close()

    def select(self, column_name, table_name, where_field=None, where_value=None, start_date=None, end_date=None):
        """
         Retrieve and display data from a specific column in a table.

            Args:
                column_name (str or tuple): The name of the column to be retrieved.
                table_name (str): The name of the table from which data will be read.
                where_field (str): The column to use for the WHERE condition (optional).
                where_value: The value to match in the where_field (optional).
                start_date: The start date for filtering data (optional).
                end_date: The end date for filtering data (optional).

            Returns:
                list: A list containing the retrieved data.

            Conditions:
                1. If multiple columns are specified (column_name is a tuple), all columns will be retrieved:
                   Example: select(("Column1", "Column2"), "TableName")

                2. If where_field and where_value are provided, the query will include a WHERE condition:
                   Example: select("ColumnName", "TableName", where_field="FilterColumn", where_value="FilterValue")

                3. If only column_name is provided, and no WHERE condition is specified, all rows of the specified column
                   will be retrieved:
                   Example: select("ColumnName", "TableName", start_date="2022-01-01", end_date="2022-01-31")


        """
        if start_date and end_date is not None:
            query = f"SELECT {column_name} FROM {table_name} WHERE {where_field} = ? AND TransactionDate BETWEEN ? AND ?"
            info = self.execute_select(query, (where_value, start_date, end_date))
        else:
            if isinstance(column_name, tuple):
                query = f'SELECT {column_name[0]}, {column_name[1]} FROM {table_name}'
                info = self.execute_select(query)
            elif where_field and where_value is not None:
                query = f"SELECT {column_name} FROM {table_name} WHERE {where_field} = ?"
                info = self.execute_select(query, (where_value,))
            else:
                query = f"SELECT {column_name} FROM {table_name}"
                info = self.execute_select(query)

        return info

    def create(self, table_name, column_names, values):
        """
           Insert data into a table.

           Args:
               table_name (str): The name of the table where data will be inserted.
               column_names (str or tuple): A string or tuple containing the column names of the table.
               values (str or tuple): A string or tuple containing the values to be inserted into the table.

           Example:
               - For a single-column insertion:
                 create('Category', "Name", "Pool")

               - For multi-column insertion:
                 create('User_accounts', ('Number', 'Type', 'Name', 'Balance'),
                        ('27412281', 'Дебетовий', 'Alexander James Anderson', "0"))
           """
        try:
            if isinstance(column_names, str):
                # If only one column is provided, use a placeholder for the parameter
                query = f"INSERT INTO {table_name} ({column_names}) VALUES (?)"
                self.execute_query(query, (values,))

            else:
                # For multiple columns, directly use the provided column_names and values
                query = f"INSERT INTO {table_name} {column_names} VALUES {values}"
                self.execute_query(query)

            # Commit the changes to the database
            self.commit()
        except Exception as e:
            print(f"Error during data insertion: {e}")

    def update(self, table_name, set_column, set_value, where_column, where_value):
        """
        Update records in the specified table.

            :param table_name: Name of the table to update (str).
            :param set_column: Column to set (str).
            :param set_value: New value for the set_column (var).
            :param where_column: Column to use for the WHERE condition (str).
            :param where_value: Value to match in the where_column (var).

        Example:
            #  "UPDATE User_Accounts SET Balance = Balance - ? WHERE Number = ?"
            update("User_Accounts", "Balance", f"Balance - {100}", "Number", "74132896")

        """
        try:
            query = f"UPDATE {table_name} SET {set_column} = ? WHERE {where_column} = ?"
            self.execute_query(query, (set_value, where_value))
            self.commit()
        except Exception as e:
            print(f"Error during data updation: {e}")

    def update_balance(self, amount, number_account, operation=None):
        try:
            query = f"UPDATE User_accounts SET Balance = Balance {operation} ? WHERE Number = ?"
            self.execute_query(query, (amount, number_account))
            self.commit()
        except Exception as e:
            print(f"Error during data updation: {e}")

    def delete(self, table_name, field_name, value):
        """
        Deletes a record from the specified table where the given column has the specified value.

        :param table_name: The name of the table from which to delete.
        :param field_name: The field to check for the specified value.
        :param value: The value to match for deletion.
        Example:
            To delete a record from the "Category" table where "Name" is "Food":
            delete("Category", "Name", "Food")

        """
        try:
            query = f"DELETE FROM {table_name} WHERE {field_name} = ?"
            self.execute_query(query, (value,))
            self.commit()
        except Exception as e:
            print(f"Error during data deletion: {e}")

    def get_categories(self):
        query = "SELECT Name FROM Category"
        try:
            cursor = self.create_cursor()
            cursor.execute(query)
            categories = cursor.fetchall()
            cursor.close()
            return [category[0] for category in categories]
        except sqlite3.Error:
            return "Курсор не створено"

    def get_account_numbers(self):
        query = "SELECT Number FROM User_Accounts"
        try:
            cursor = self.create_cursor()
            cursor.execute(query)
            numbers = cursor.fetchall()
            cursor.close()
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

import re
from datetime import datetime, timedelta
import random
from abc import ABC
from sources import API_ver2

"""Version 3.0"""

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

# ----------------------------------------PATH DATABASE FILE----------------------------------------------------
# database_path = input("Database path: ")
api = API_ver2.DatabaseManager("F:\\Python\\Wallet\\DB\\Wallet.db")
api.connect()
cursor = api.create_cursor()

# --------------------------------------------------------------------------------------------------------------
user_categories = api.get_categories()
lst_accounts = api.get_account_numbers()


# ----------------------------------------------------------------------------------------------------------------


class Menu:

    def __init__(self):
        self.main_menu_options = ["Управління категоріями витрат та доходів", "Управління рахунками",
                                  "Управління витратами та доходами", "Вихід"]
        self.cat1 = CategoryOne
        self.cat2 = CategoryTwo
        self.cat3 = CategoryThree

    # functional cycle of the menu, responsible for the operation and calling functions selected by the user

    @staticmethod
    def menu_loop(name_var, end, dictionary, menu_name=None):
        if name_var > end:
            print("Ви ввели неправильне значення. Спробуйте ще раз")
            menu_name()
        elif name_var <= end:
            func = dictionary.get(name_var)
            func()

    @staticmethod
    def the_end():
        api.close()
        quit()

    def main_menu(self):
        print("1.{} \n2.{} \n3.{} \n4.{} \nОберіть потрібну цифру: от 1 до 4: "
              .format(*self.main_menu_options))
        menu_dict = {
            1: self.cat1().menu_cat1,
            2: self.cat2().menu_cat2,
            3: self.cat3().menu_cat3,
            4: self.the_end
        }
        try:
            choice = int(input("Введіть потрібний пункт: "))
            self.menu_loop(choice, 4, menu_dict, self.main_menu)
        except ValueError:
            print("\nВи ввели неправильне значення. Спробуйте ще раз.\n")
            self.main_menu()


class Categories(ABC):

    def __init__(self):
        # class Menu
        self.menu = Menu()

        # CategoryOne
        self.menu_categories = ["Додати категорію", "Видалити категорію", "Змінити дані про категорію",
                                "Перегляд списку категорій", "Назад\n"]
        self.user_categories = user_categories

        # CategoryTwo
        self.bank_account = ["Створити новий рахунок", "Видалити рахунок", "Змінити дані рахунку",
                             "Переглянути список рахунків", "Назад\n"]

        # CategoryThree
        self.income_expense_management = ["Додати транзакцію",
                                          "Видалити транзакцію",
                                          "Переведення грошей з рахунку на рахунок",
                                          "Перевірка витрат/прибутків за певний період",
                                          "Отримання статистики прибутків/витрат за певний період по днях та категоріях",
                                          "Назад\n"]

    # displaying menu items of the selected category
    @staticmethod
    def print_subcategory_menu(lst):
        for i, elem in enumerate(lst, start=1):
            print(f"{i}.{elem}")

    def return_to_menu(self):
        self.menu.main_menu()

    # checks for data type and sends to the menu_loop function
    def menu_universal(self, num, functional, menu_name):
        try:
            choice = int(input("Оберіть потрібний пункт: "))
            self.menu.menu_loop(choice, num, functional, menu_name)
        except ValueError:
            print("\nВи ввели неправильне значення. Спробуйте ще раз.\n")

    # checking the correctness of the account number
    @staticmethod
    def validate_account_num(num):
        if num in lst_accounts:
            return True
        else:
            print("Рахунок не знайдено")
            return False

    # You pass the second argument as True if you need to check for 3.
    # If you need to check for 2, then you don't pass anything.
    @staticmethod
    def validate_menu_choice(var, include_three=False):
        if not include_three:
            if var == "1" or var == "2":
                return True
            else:
                return False
        elif include_three:
            if var == "1" or var == "2" or var == "3":
                return True
            else:
                return False

    @staticmethod
    def display_balance(account_num):
        """

        Args:
            account_num:

        example sql query:
        "SELECT column_name FROM table_name WHERE where_field = ?", (account_num,)

        """
        balance_info = api.select("Balance", "User_Accounts", "Number", account_num)
        print("Баланс: {:,.2f} грн".format(balance_info[0][0]))

    def display_account_info(self, account_num):
        """
        Display account information: account_num, Name, Type, Balance
        Args:
            account_num:

        Example sql query:
        "SELECT * FROM User_accounts WHERE Number = ?", (account_num)
        """
        row = api.select("*", "User_Accounts", "Number", account_num)[0]
        print(f"Номер Рахунку: {row[0]}")
        print(f"Тип: {row[1]}")
        print(f"ПІБ: {row[2]}")
        self.display_balance(account_num)
        print()

    def display_number_and_balance(self):
        numbers_and_balance = api.select(("Number", "Name"), "User_Accounts")
        for elem in numbers_and_balance:
            print("Номер рахунку: {}".format(elem[0]))
            print("ПІБ: {}".format(elem[1]))
            self.display_balance(elem[0])
            print()

    @staticmethod
    def display_numbers_and_names():
        for elem in lst_accounts:
            # cursor.execute("SELECT Name FROM User_Accounts WHERE Number = ?", (elem,))
            info = api.select("Name", "User_Accounts", "Number", elem)
            print("Номер рахунку: {}".format(elem))
            print("ПІБ: {}\n".format(info[0][0]))

    def display_transactions(self, account_num):
        """Отображение транзакций"""
        # cursor.execute("SELECT * FROM TransactionAll WHERE Number = ?", (account_num,))
        transaction_list = api.select("*", "TransactionAll", "Number", account_num)
        if len(transaction_list) != 0:
            self.display_account_info(account_num)
            print("Транзакції: ")
            count = 0
            for elem in transaction_list:
                count += 1
                print(
                    f"{count}. {elem[3]} | {elem[2]} | {elem[1]} | {elem[5]}"
                    f" | id:{elem[4]}")
                self.visual()
            return True
        else:
            print("Транзакцій на рахунку: {} не знайдено\n".format(account_num))
            return False

    def input_num(self):
        while True:
            num = input("Введіть номер рахунку:")
            if self.validate_account_num(num):
                return num

    @staticmethod
    def visual():
        print("-------------------------------------------------------------------------------------------------------")

    @staticmethod
    def display_lst_user_cat():
        for elem in user_categories:
            print(elem)


class CategoryOne(Categories):

    def validation_name_category(self, name):
        if name in self.user_categories:
            return True
        else:
            return False

    def validate_name_categories(self, name):
        if name in self.user_categories:
            print("Категорія з назвою {} вже існує.".format(name))
            return False
        else:
            return True

    def add_category(self):
        print("\nІснуючі категорії:")
        self.display_lst_user_cat()
        name = input("Введіть назву нової категорії: ")
        if self.validate_name_categories(name):
            self.user_categories.append(name)
            api.create("Category", "Name", name)
            if name in self.user_categories:
                print(f"Категорія {name} додана")

    def remove_category(self):
        self.display_lst_user_cat()
        name = input("Введіть назву категорії: ")
        if name in self.user_categories:
            self.user_categories.remove(name)
            api.delete("Category", "Name", name)
            if name not in self.user_categories:
                print(f"Категорія {name} видалена")
        elif name not in self.user_categories:
            print(f"Категорію з назвою {name} не знайдено")

    def update_category(self):
        self.display_lst_user_cat()
        name = input("Введіть назву категорії, яку потрібно змінити: ")
        if name in self.user_categories:
            print(f"Категорія з назвою {name} знайдена.")
            index = self.user_categories.index(name)
            while True:
                new_name = input("Введіть нову назву: ")
                if self.validate_name_categories(new_name):
                    cursor.execute("UPDATE Category SET Name = ? WHERE Name = ?", (new_name, name))
                    api.commit()
                    self.user_categories[index] = new_name
                    print(f"Назва категорії {name} змінена на {new_name}")
                    break
        else:
            print(f"Категорія з назвою {name} не знайдена")

    def list_category(self):
        print("Список категорій:")
        print(", ".join(self.user_categories))

    def menu_cat1(self):
        functional = {
            1: self.add_category,
            2: self.remove_category,
            3: self.update_category,
            4: self.list_category,
            5: self.menu.main_menu
        }
        while True:
            self.print_subcategory_menu(self.menu_categories)
            self.menu_universal(5, functional, self.menu_cat1)


class CategoryTwo(Categories):
    # когда удаляют счет удалять из списка lst_account
    @staticmethod
    def generate_account_number():
        digits = list(range(10))
        random.shuffle(digits)
        account_number = ''.join(map(str, digits[:8]))
        return account_number

    def validate_new_account_num(self, account_num):
        if account_num not in lst_accounts:
            lst_accounts.append(account_num)
        else:
            account_num = self.generate_account_number()
            lst_accounts.append(account_num)
        return account_num

    @staticmethod
    def validate_name(name):
        # pattern = r'^[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+\s+([-\']?[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+\s+)?[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+$'
        pattern = r'^[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+\s+[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+\s+[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+$'
        match = re.match(pattern, name)
        if match:
            return True
        else:
            print("ПІБ введено неправильно")
            return False

    def input_name(self):
        while True:
            name = input("Введіть ПІБ: ")
            if self.validate_name(name):
                return name

    def input_type(self):
        while True:
            account_type = input("Оберіть тип: \n1.Дебетовий \n2.Кредитний \nВведіть цифру 1 або 2: ")
            if self.validate_menu_choice(account_type):
                if account_type == "1":
                    return "Дебетовий"
                elif account_type == "2":
                    return "Кредитний"

    def add_user_acc(self):
        account_num = self.generate_account_number()
        if len(account_num) == 8:
            account_num = self.validate_new_account_num(account_num)
            account_name = self.input_name()
            account_type = self.input_type()
            if account_num in lst_accounts:
                api.create("User_Accounts", ("Number", 'Type', 'Name', 'Balance'),
                           (account_num, account_type, account_name, 0))
            print('Рахунок створено\n')
            self.display_account_info(account_num)
            self.visual()
        else:
            print("Виникла помилка, спробуйте ще раз")
            return self.add_user_acc

    def remove_user_acc(self):
        self.lst_user_acc()
        num_acc = input("Введіть номер рахунку для видалення: ")
        if num_acc in lst_accounts:
            api.delete("User_Accounts", "Number", num_acc)
            lst_accounts.remove(num_acc)
            if num_acc not in lst_accounts:
                print(f"Рахунок {num_acc} видалено \n")
                api.delete("TransactionAll", "Number", num_acc)
        else:
            print("Рахунок не знайдено \n")
            self.remove_user_acc()

    def update_menu(self, input_acc):
        def update_account_type():
            update_acc_type = ["1.Дебетовий", "2.Кредитний", "3.Назад"]
            print("{} \n{} \n{}".format(*update_acc_type))
            while True:
                # проверять ввод через функцию  validate_menu_choice
                what_type = input("Оберіть пункт: ")
                if what_type == "1":
                    cursor.execute("UPDATE User_Accounts SET Type = ? WHERE Number = ?", ("Дебетовий", input_acc))
                    print("Тип рахунку змінено на Дебетовий \n")
                    self.display_account_info(input_acc)
                    return

                elif what_type == "2":
                    cursor.execute("UPDATE User_Accounts SET Type = ? WHERE Number = ?", ("Кредитний", input_acc))
                    print("Тип рахунку змінено на Кредитний \n")
                    self.display_account_info(input_acc)
                    return

                elif what_type == "3":
                    return

                else:
                    print("Неправильний вибір, спробуйте ще раз.")
                    update_account_type()

        def update_account_name():
            while True:
                new_name = input("Введіть новий ПІБ: ")
                if self.validate_name(new_name):
                    cursor.execute("UPDATE User_Accounts SET Name = ? WHERE Number = ?", (new_name, input_acc))
                    print("Інформацію оновлено")
                    self.display_account_info(input_acc)
                    self.update_menu(input_acc)
                    return "back"

                else:
                    print("Неправильне ім'я, спробуйте ще раз.")
                    continue

        while True:
            update_menu_lst = ["Що бажаєте змінити?", "1.Тип", "2.ПІБ", "3.Повернутись в меню"]
            print("{} \n{} \n{} \n{}".format(*update_menu_lst))
            what_change = input("Введіть номер опції: ")
            if what_change == "1":
                update_account_type()

            elif what_change == "2":
                result1 = update_account_name()
                if result1 == "back":
                    break

            elif what_change == "3":
                break

            else:
                print("Неправильний вибір, спробуйте ще раз.")
                self.update_menu(input_acc)

    def update_user_acc(self):
        self.lst_user_acc()
        input_acc = input("Введіть номер рахунку: ")
        if input_acc in lst_accounts:
            print("Рахунок знайдено")
            self.display_account_info(input_acc)
            print()
            self.update_menu(input_acc)
            api.commit()
        else:
            print("Рахунок не знайдено, спробуйте ще раз")
            self.update_user_acc()

    def lst_user_acc(self):
        if len(lst_accounts) == 0:
            print("Рахунків нема")
        for i in lst_accounts:
            self.display_account_info(i)

    def menu_cat2(self):
        functional = {
            1: self.add_user_acc,
            2: self.remove_user_acc,
            3: self.update_user_acc,
            4: self.lst_user_acc,
            5: self.menu.main_menu
        }
        while True:
            self.print_subcategory_menu(self.bank_account)
            self.menu_universal(5, functional, self.menu_cat2)


class CategoryThree(CategoryOne, CategoryTwo, Categories):

    @staticmethod
    def generate_random_date():
        """Генерация даты"""
        current_time = datetime.now()
        time_speed = random.uniform(0, 5)  # случайное значение скорости времени
        step = timedelta(days=1)
        current_time += step * time_speed
        return current_time.strftime("%Y-%m-%d")

    @staticmethod
    def generate_transaction_id():
        """Генерация id"""
        rand_num = random.randint(100000, 999999)
        new_transaction_id = f"TRX{rand_num}"
        return new_transaction_id

    def validate_money_input(self):
        date = self.generate_random_date()

        while True:
            self.list_category()
            category_input = input("Введіть одну з категорій: ")
            if category_input in self.user_categories:
                break
            print("Категорія не знайдена, Спробуйте ще раз.")

        pattern = r"^[+\-]\d{1,10}$"
        while True:
            amount = input("Введіть значення транзакції у наступному форматі: "
                           "+/- сума', наприклад, '+100' або '-100'."
                           "Максимальна довжина - 10 символів: ")

            trans = amount
            if re.match(pattern, amount):
                trans_type = "Дохід" if amount[0] == "+" else "Витрата"
                return date, category_input, int(amount[1:]), trans_type, trans

            print("Введено неправильно. \nПриклад: +100, -100 \nМаксимальна довжина - 10 символів ")

    @staticmethod
    def validate_date_input():
        pattern = r"\d{4}-\d{2}-\d{2}"  # Формат YYYY-MM-DD
        while True:
            date_start_input = input("Введіть дату початку періоду (в форматі YYYY-MM-DD): ")
            if re.match(pattern, date_start_input):
                date_start = datetime.strptime(date_start_input, "%Y-%m-%d").date()
                while True:
                    date_end_input = input("Введіть дату кінця початку періоду (в форматі YYYY-MM-DD): ")
                    if re.match(pattern, date_end_input):
                        date_end = datetime.strptime(date_end_input, "%Y-%m-%d").date()
                        if date_end > date_start:
                            return date_start, date_end
                        else:
                            print("Дата кінця періоду повинна бути більше дати початку періоду.")
                    else:
                        print("Введена неправильна дата")
            else:
                print("Введена неправильна дата")

    @staticmethod
    def input_id():
        pattern = r"^TRX\d{6}$"
        while True:
            transaction_id = input("Введіть id транзакції: ")
            if re.match(pattern, transaction_id):
                return transaction_id
            else:
                print("Невірний формат id транзакції. Спробуйте ще раз.")

    # adding  transactions
    def add_transaction(self):
        # Show a list of user accounts for selection
        self.lst_user_acc()
        trans_id = self.generate_transaction_id()
        # Get the account number from the user input
        account_num = self.input_num()
        self.display_balance(account_num)
        # Get the date, category, and transaction details from the user input
        date, category, amount, trans_type, trans = self.validate_money_input()
        api.create("TransactionAll", ("Number", "Type", "Category", "TransactionDate", "TransactionID", "Amount"),
                   (account_num, trans_type, category, date, trans_id, amount))
        if trans_type == "Витрата":
            cursor.execute("UPDATE User_Accounts SET Balance = Balance - ? WHERE Number = ?", (amount, account_num))
        elif trans_type == "Дохід":
            cursor.execute("UPDATE User_Accounts SET Balance = Balance + ? WHERE Number = ?", (amount, account_num))
        print("Транзакція додана: {} | {} | {}\n".format(date, category, trans))
        self.display_account_info(account_num)

    # delete transactions
    def delete_transactions(self):
        self.lst_user_acc()
        account_num = self.input_num()
        if self.display_transactions(account_num):
            transaction_id = self.input_id()
            # cursor.execute("SELECT * FROM TransactionAll WHERE TransactionID = ?", (transaction_id,))
            # list_transaction_del = cursor.fetchall()
            list_transaction_del = api.select("*", "TransactionAll", "TransactionID", transaction_id)
            for elem in list_transaction_del:
                if elem[1] == "Витрата":
                    cursor.execute("UPDATE User_Accounts SET Balance = Balance + ? WHERE Number = ? ",
                                   (elem[5], elem[0]))
                if elem[1] == "Дохід":
                    cursor.execute("UPDATE User_Accounts SET Balance = Balance - ? WHERE Number = ? ",
                                   (elem[5], elem[0]))
            api.delete("TransactionAll", "TransactionID", transaction_id)
            print("Транзакція видалена \n")

    # transfer money between accounts
    def transfer_money(self):
        self.display_number_and_balance()
        print("Номер відправника:")
        from_num1 = self.input_num()
        print("Номер рахунку: {}".format(from_num1))
        self.display_balance(from_num1)
        print()
        print("Номер одержувача:")
        to_num2 = self.input_num()
        transfer_id = self.generate_transaction_id()
        date1 = self.generate_random_date()
        category = "Перекази"
        balance_num1 = api.select("Balance", "User_Accounts", "Number", from_num1)
        if int(balance_num1[0][0]) != 0:
            while True:
                amount = float(input("Введіть суму для переводу: "))
                if amount > 0:
                    break
                else:
                    print("Сума повинна бути більше нуля. Будь ласка, введіть коректну суму.")

            # add the new transaction to the DB in Table | TransactionAll | Transaction_Transfer
            if int(balance_num1[0][0]) > amount:
                # INSERT DATA IN TransactionAll FROM_NUM
                api.create("TransactionAll",
                           ("Number", "Type", "Category", "TransactionDate", "TransactionID", "Amount"),
                           (from_num1, "Витрата", category, date1, transfer_id, amount))
                # INSERT DATA IN TransactionAll TO_NUM
                api.create("TransactionAll",
                           ("Number", "Type", "Category", "TransactionDate", "TransactionID", "Amount"),
                           (to_num2, "Дохід", category, date1, transfer_id, amount))
                # UPDATE BALANCE FROM_NUM
                cursor.execute(
                    "UPDATE User_Accounts SET Balance = Balance - {} WHERE Number = {}".format(amount, from_num1))
                # UPDATE BALANCE TO_NUM
                cursor.execute(
                    "UPDATE User_Accounts SET Balance = Balance + {} WHERE Number = {}".format(amount, to_num2))

                # INSERT DATA IN Transaction_Transfer
                api.create("Transaction_Transfer",
                           ("From_Number", "To_number", "TransactionDate", "TransactionID", "Amount"),
                           (from_num1, to_num2, date1, transfer_id, amount))

                print("Транзакція пройшла успішно")

            else:
                print("Недостатньо коштів на рахунку")
        else:
            print("Баланс рахунку: {} пустий".format(from_num1))

    # info about  expense\income time interval
    def get_expenses_income_by_period(self):
        self.display_numbers_and_names()
        num = self.input_num()
        print("Для перевірки витрат і прибутків за певний період, будь ласка, введіть дату початку періоду та дату "
              "його завершення. Формат дати має бути наступним: рік-місяць-день (наприклад, 2023-05-16)")
        start_date, end_date = self.validate_date_input()
        income = 0
        expense = 0
        list_transaction = api.select("*", "TransactionAll", "Number", num, start_date, end_date)
        for elem in list_transaction:
            if elem[1] == "Дохід":
                income += elem[5]
            else:
                expense += elem[5]
        print(f"Для введеного Вами періоду часу, загальна сума витрат становить {expense:,.2f} гривень.")
        print(f"Також, загальний прибуток за цей період склав {income:,.2f} гривень. ")
        print("Дякую, що користуєтесь нашим сервісом!")

    # info about all times expense\income in categories
    def get_statistics(self):
        self.display_numbers_and_names()
        num = self.input_num()
        statistics_data = api.select("*", "TransactionAll", "Number", num)
        for elem in statistics_data:
            print("Категорія: {} | Дата: {} | Тип: {} | Сумма: {}".format(elem[2], elem[3], elem[1], elem[5]))

        print()

    def menu_cat3(self):
        functional = {
            1: self.add_transaction,
            2: self.delete_transactions,
            3: self.transfer_money,
            4: self.get_expenses_income_by_period,
            5: self.get_statistics,
            6: self.menu.main_menu
        }
        while True:
            self.print_subcategory_menu(self.income_expense_management)
            self.menu_universal(6, functional, self.menu_cat3)


test = Menu()
test.main_menu()

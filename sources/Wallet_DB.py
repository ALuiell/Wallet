import re
from datetime import datetime, timedelta
import random
from abc import ABC
from sources import database_manager_ORM
from models import *

"""Version 3.
add refresh categories and number list
"""

# ----------------------------------------PATH DATABASE FILE----------------------------------------------------
db_path = "F:\\Python\\Wallet\\DB\\wallet_test.db"
db_manager = database_manager_ORM.DatabaseManager(db_path)

# --------------------------------------------------------------------------------------------------------------
user_categories = [elem.Name for elem in Category]
lst_accounts = [elem.Number for elem in User_Accounts]


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
    def generate_menu_dict(*list_menu_options):
        menu_dict = {}
        for index, option in enumerate(list_menu_options, start=1):
            menu_dict[index] = option
        return menu_dict

    @staticmethod
    def the_end():
        db_manager.close()
        quit()

    def main_menu(self):
        print("1.{} \n2.{} \n3.{} \n4.{} \nОберіть потрібну цифру: от 1 до 4: "
              .format(*self.main_menu_options))

        menu_dict = self.generate_menu_dict(self.cat1().menu_category1,
                                            self.cat2().menu_category2,
                                            self.cat3().menu_category3,
                                            self.the_end)

        try:
            choice = int(input("Введіть потрібний пункт: "))
            self.menu_loop(choice, len(menu_dict), menu_dict, self.main_menu)
        except ValueError:
            print("\nВи ввели неправильне значення. Спробуйте ще раз.\n")
            self.main_menu()


class BaseCategory(ABC):

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
                                          "Отримання статистики прибутків/витрат за певний період по категоріях",
                                          "Назад\n"]

    # displaying menu items of the selected category
    @staticmethod
    def print_subcategory_menu(lst):
        for i, elem in enumerate(lst, start=1):
            print(f"{i}.{elem}")

    def return_to_menu(self):
        self.menu.main_menu()

    # checks for a data type and sends to the menu_loop function
    def menu_universal(self, menu_dict, menu_name):
        menu_item_count = len(menu_dict)
        try:
            choice = int(input("Оберіть потрібний пункт: "))
            self.menu.menu_loop(choice, menu_item_count, menu_dict, menu_name)
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
        balance_info = User_Accounts.get(Number=account_num)
        print("Баланс: {:,.2f} грн".format(balance_info.Balance))

    def display_account_info(self, account_num):
        row = User_Accounts.get(Number=account_num)
        print(f"Номер Рахунку: {row.Number}")
        print(f"Тип: {row.Type}")
        print(f"ПІБ: {row.Name}")
        self.display_balance(row.Number)
        print()

    def display_number_and_balance(self):
        for elem in User_Accounts.select(User_Accounts.Number, User_Accounts.Name):
            print(f"Номер рахунку: {elem.Number}")
            print(f"ПІБ: {elem.Name}")
            self.display_balance(elem.Number)
            print()

    @staticmethod
    def show_list_users():
        for elem in User_Accounts.select(User_Accounts.Number, User_Accounts.Name):
            print(f"Номер рахунку: {elem.Number}")
            print(f"ПІБ: {elem.Name}\n")

    def display_user_transactions(self, account_num, show_for_user=False):
        list_transactions = (TransactionAll
                             .select()
                             .join_from(TransactionAll, User_Accounts)
                             .join_from(TransactionAll, Category)
                             .where(User_Accounts.Number == account_num))
        if list_transactions:
            if show_for_user:
                for transaction in list_transactions:
                    print(
                        f"Категорія: {transaction.Category.Name} | Дата: {transaction.Date} | Тип: {transaction.Type} "
                        f"| Сумма: {transaction.Amount}")
            else:
                self.display_account_info(account_num)
                print("Транзакції:")
                for count, transaction in enumerate(list_transactions, start=1):
                    print(
                        f"{count}. {transaction.Date} | {transaction.Category.Name} | {transaction.Type} "
                        f"| {transaction.Amount} "
                        f"| id:{transaction.TransactionID}")
                self.visual()
                return True
        else:
            print("Транзакцій на рахунку: {} не знайдено\n".format(account_num))
            return False

    def input_number(self):
        while True:
            num = input("Введіть номер рахунку:")
            if num.isnumeric():
                if self.validate_account_num(num):
                    return num
            else:
                print("Введено некоректні дані, спробуйте ще раз.")

    @staticmethod
    def update_global_lists():
        global user_categories, lst_accounts

        # Извлекаем новые значения из базы данных
        new_categories = [elem.Name for elem in Category]
        new_accounts = [elem.Number for elem in User_Accounts]

        # Обновляем глобальные списки
        user_categories = new_categories
        lst_accounts = new_accounts

    @staticmethod
    def visual():
        print("-------------------------------------------------------------------------------------------------------")

    @staticmethod
    def show_user_categories():
        for elem in user_categories:
            print(elem)


class CategoryOne(BaseCategory):

    @staticmethod
    def category_name_exists(name):
        return db_manager.verify(Category, "Name", name)

    def create_new_category(self):
        print("\nІснуючі категорії:")
        self.show_user_categories()
        name = input("Введіть назву нової категорії: ")
        if not self.category_name_exists(name):
            self.add_category_to_db(name)
            self.update_global_lists()
        else:
            print("Категорія з такою назвою вже існує")

    @staticmethod
    def add_category_to_db(name):
        db_manager.create(Category, {"Name": name})
        print(f"Категорія {name} додана")

    def remove_category(self):
        self.show_user_categories()
        name = input("Введіть назву категорії: ")
        if self.category_name_exists(name):
            self.delete_category_from_db(name)
            self.update_global_lists()
        else:
            print(f"Категорію з назвою {name} не знайдено")

    @staticmethod
    def delete_category_from_db(name):
        db_manager.delete(Category, "Name", name)
        print(f"Категорія {name} видалена")

    def update_category(self):
        self.show_user_categories()
        name = input("Введіть назву категорії, яку потрібно змінити: ")
        if self.category_name_exists(name):
            print(f"Категорія з назвою {name} знайдена.")
            while True:
                new_name = input("Введіть нову назву: ")
                if not self.category_name_exists(new_name):
                    self.update_name_category_in_db(name, new_name)
                    self.update_global_lists()
                    break
                else:
                    print(f"Категорія з назвою {new_name} вже існує. Будь ласка, введіть інше ім'я.")

        else:
            print(f"Категорія з назвою {name} не знайдена")

    @staticmethod
    def update_name_category_in_db(name, new_name):
        db_manager.update(Category, "Name", new_name, "Name", name)
        print(f"Назва категорії {name} змінена на {new_name}")

    def show_list_categories(self):
        print("Список категорій:")
        print(", ".join(self.user_categories))
        print()

    def menu_category1(self):
        menu_dict = self.menu.generate_menu_dict(self.create_new_category,
                                                 self.remove_category,
                                                 self.update_category,
                                                 self.show_list_categories,
                                                 self.menu.main_menu)
        while True:
            self.print_subcategory_menu(self.menu_categories)
            self.menu_universal(menu_dict, self.menu_category1)


class CategoryTwo(BaseCategory):

    def generate_account_number(self):
        digits = list(range(10))
        random.shuffle(digits)
        account_number = ''.join(map(str, digits[:8]))
        if len(account_number) == 8:
            if not self.account_number_exists(account_number):
                return account_number
        else:
            self.generate_account_number()

    @staticmethod
    def account_number_exists(account_num):
        return db_manager.verify(User_Accounts, "Number", account_num)

    @staticmethod
    def validate_name(name):
        # pattern = r'^[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+\s+([-\']?[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+\s+)?[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+$'
        pattern = r'^[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+\s+[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+\s+[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+$'
        # pattern = r'^[\p{Lu}][\p{L}\s]+[\p{Lu}][\p{L}\s]+[\p{Lu}][\p{L}\s]+$'
        match = re.match(pattern, name)
        if match:
            return True
        else:
            print("ПІБ введено неправильно, спробуйте ще.")
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

    def create_user_account(self):
        account_number = self.generate_account_number()
        account_name = self.input_name()
        account_type = self.input_type()
        data = {"Number": account_number,
                "Type": account_type,
                "Name": account_name,
                "Balance": 0}
        self.add_new_user_to_db(data)
        self.display_account_info(data["Number"])
        self.update_global_lists()
        self.visual()

    @staticmethod
    def add_new_user_to_db(data):
        db_manager.create(User_Accounts, data)
        print('Рахунок створено\n')

    def remove_user_account(self):
        self.show_list_users()
        number_for_delete = self.input_number()
        number_id = User_Accounts.get(Number=number_for_delete)
        if self.account_number_exists(number_for_delete):
            self.delete_user_account_from_db(number_for_delete, number_id)
            self.update_global_lists()
        else:
            self.remove_user_account()

    @staticmethod
    def delete_user_account_from_db(number, number_id):
        db_manager.delete(User_Accounts, "Number", number)
        db_manager.delete(TransactionAll, "Number", number_id)
        print(f"Рахунок {number} видалено \n")

    def update_user_name(self, account_number):
        while True:
            new_name = input("Введіть новий ПІБ: ")
            if self.validate_name(new_name):
                db_manager.update(User_Accounts, "Name", new_name, "Number", account_number)
                print("Інформацію оновлено")
                self.display_account_info(account_number)
                return

    def update_user_type_on_credit(self, account_number):
        db_manager.update(User_Accounts, "Type", "Кредитний", "Number", account_number)
        print("Тип рахунку змінено на Кредитний \n")
        self.display_account_info(account_number)

    def update_user_type_on_debit(self, account_number):
        db_manager.update(User_Accounts, "Type", "Дебетовий", "Number", account_number)
        print("Тип рахунку змінено на Дебетовий \n")
        self.display_account_info(account_number)

    def display_user_type_update_menu(self, account_number):
        update_menu_type_lst = ["Дебетовий", "Кредитний", "Назад"]
        menu_dict = self.menu.generate_menu_dict(
            lambda: self.update_user_type_on_debit(account_number),
            lambda: self.update_user_type_on_credit(account_number),
            lambda: self.display_user_data_update_menu(account_number)
        )

        while True:
            self.print_subcategory_menu(update_menu_type_lst)
            choice = input("Оберіть потрібний пункт: ")
            if choice.isdigit() and int(choice) in menu_dict:
                menu_dict[int(choice)]()
                break
            else:
                print("Неправильний вибір, спробуйте ще раз.")

    def display_user_data_update_menu(self, account_number=None):
        update_menu_lst = ["Тип", "ПІБ", "Повернутись в меню"]
        menu_dict = self.menu.generate_menu_dict(
            lambda: self.display_user_type_update_menu(account_number),
            lambda: self.update_user_name(account_number),
            self.menu_category2
        )
        while True:
            self.print_subcategory_menu(update_menu_lst)
            self.menu_universal(menu_dict, self.display_user_data_update_menu)

    def update_user_data(self):
        self.show_list_users()
        account_number = self.input_number()
        print("Рахунок знайдено")
        print()
        self.display_account_info(account_number)
        self.display_user_data_update_menu(account_number)

    def show_list_users(self):
        if len(lst_accounts) == 0:
            print("Рахунків нема")
        for i in lst_accounts:
            self.display_account_info(i)

    def menu_category2(self):
        menu_dict = self.menu.generate_menu_dict(self.create_user_account,
                                                 self.remove_user_account,
                                                 self.update_user_data,
                                                 self.show_list_users,
                                                 self.return_to_menu
                                                 )
        while True:
            self.print_subcategory_menu(self.bank_account)
            self.menu_universal(menu_dict, self.menu_category2)


class CategoryThree(CategoryOne, CategoryTwo, BaseCategory):

    @staticmethod
    def generate_random_date():
        """Генерация даты и времени с учетом случайной скорости времени"""
        current_time = datetime.now()
        time_speed = random.uniform(0, 5)  # случайное значение скорости времени
        step = timedelta(days=1)
        current_time += step * time_speed
        formatted_datetime = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_datetime

    @staticmethod
    def generate_transaction_id():
        """Генерация id"""
        rand_num = random.randint(100000, 999999)
        new_transaction_id = f"TRX{rand_num}"
        return new_transaction_id

    def validate_money_input(self):
        date = self.generate_random_date()

        while True:
            self.show_list_categories()
            category_input = input("Введіть одну з категорій: ")
            if category_input in self.user_categories:
                break
            print("Категорія не знайдена, Спробуйте ще раз.")

        pattern = r"^[+\-]\d{1,10}$"
        while True:
            amount = input("Введіть значення транзакції у наступному форматі: "
                           "+/- сума', наприклад, '+100' або '-100'."
                           "Максимальна довжина - 10 символів: ")

            transaction_str = amount
            if re.match(pattern, amount):
                trans_type = "Дохід" if amount[0] == "+" else "Витрата"
                return date, category_input, int(amount[1:]), trans_type, transaction_str

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
    def input_transaction_id():
        pattern = r"^TRX\d{6}$"
        while True:
            transaction_id = input("Введіть id транзакції: ")
            if re.match(pattern, transaction_id):
                return transaction_id
            else:
                print("Невірний формат id транзакції. Спробуйте ще раз.")

    @staticmethod
    def update_balance(transaction_type, account_number, amount, is_transaction_cancelled=False):
        if transaction_type == "Дохід":
            if is_transaction_cancelled:
                db_manager.update(User_Accounts, 'Balance', User_Accounts.Balance - amount, 'Number', account_number)
            else:
                db_manager.update(User_Accounts, 'Balance', User_Accounts.Balance + amount, 'Number', account_number)
        elif transaction_type == "Витрата":
            if is_transaction_cancelled:
                db_manager.update(User_Accounts, 'Balance', User_Accounts.Balance + amount, 'Number', account_number)
            else:
                db_manager.update(User_Accounts, 'Balance', User_Accounts.Balance - amount, 'Number', account_number)

    # adding new transactions
    def add_transaction(self):
        self.show_list_users()
        trans_id = self.generate_transaction_id()
        account_num = self.input_number()
        self.display_balance(account_num)
        date, category, amount, transaction_type, transaction_str = self.validate_money_input()
        num_id, cat_id = User_Accounts.get(Number=account_num), Category.get(Name=category)
        db_manager.create(TransactionAll, {"Number": num_id,
                                           "Type": transaction_type,
                                           "Category": cat_id,
                                           "Date": date,
                                           "TransactionID": trans_id,
                                           "Amount": amount})

        self.update_balance(transaction_type, account_num, amount)
        print("Транзакція додана: {} | {} | {}\n".format(date, category, transaction_str))
        self.display_account_info(account_num)

    # delete transactions
    def delete_transactions(self):
        self.show_list_users()
        account_num = self.input_number()
        if self.display_user_transactions(account_num):
            transaction_id = self.input_transaction_id()
            list_transaction_for_del = TransactionAll.select().where(TransactionAll.TransactionID == transaction_id)
            for elem in list_transaction_for_del:
                self.update_balance(elem.Type, elem.Number.Number, elem.Amount, is_transaction_cancelled=True)
            db_manager.delete(TransactionAll, "TransactionID", transaction_id)

    def transaction_transfer_(self):
        def get_transfer_info():
            self.display_number_and_balance()
            print("Номер відправника")
            from_num = self.input_number()
            print("Номер рахунку: {}".format(from_number))
            self.display_balance(from_number)
            print()
            print("Номер одержувача")
            to_num = self.input_number()
            transaction_transfer_id = self.generate_transaction_id()
            date = self.generate_random_date()
            return to_num, from_num, transaction_transfer_id, date

        def validate_transfer(account_object):
            if account_object.Balance != 0:
                while True:
                    amount_input = float(input("Введіть суму для переводу: "))
                    if 0 < amount_input <= account_object.Balance:
                        return amount_input
                    else:
                        print(
                            "Сума повинна бути більше нуля і не перевищувати баланс. Введіть коректну суму.")
            else:
                print("Недостатньо коштів на рахунку")

        def get_objects():
            from_number_object = User_Accounts.get(Number=from_number)
            to_number_object = User_Accounts.get(Number=to_number)
            cat_id = Category.get(Name="Перекази")
            return from_number_object, to_number_object, cat_id

        def create_transaction():
            db_manager.create(TransactionAll, {"Number": from_user_object,
                                               "Type": "Витрата",
                                               "Category": category_id,
                                               "Date": transaction_date,
                                               "TransactionID": transaction_id,
                                               "Amount": amount})

            db_manager.create(TransactionAll, {"Number": to_user_object,
                                               "Type": "Дохід",
                                               "Category": category_id,
                                               "Date": transaction_date,
                                               "TransactionID": transaction_id,
                                               "Amount": amount})

            self.update_balance("Витрата", from_number, amount)
            self.update_balance("Дохід", to_number, amount)
            print("Транзакція пройшла успішно")
            print(f"Відправник: {from_user_object.Name} | Отримувач: {to_user_object.Name}")

        to_number, from_number, transaction_id, transaction_date = get_transfer_info()
        from_user_object, to_user_object, category_id = get_objects()
        amount = validate_transfer(from_user_object)
        create_transaction()
        print()

    def get_expenses_income_by_period(self):
        self.show_list_users()
        num = self.input_number()
        print("Для перевірки витрат і прибутків за певний період, будь ласка, введіть дату початку періоду та дату "
              "його завершення. Формат дати має бути наступним: рік-місяць-день (наприклад, 2023-05-16)")
        start_date, end_date = self.validate_date_input()
        income = 0
        expense = 0
        list_transaction = (TransactionAll.select().join(User_Accounts).where(
            (User_Accounts.Number == num) &
            (TransactionAll.Date.between(start_date, end_date))))

        for elem in list_transaction:
            if elem.Type == "Дохід":
                income += elem.Amount
            else:
                expense += elem.Amount
        print(f"Для введеного Вами періоду часу, загальна сума витрат становить {expense:,.2f} гривень.")
        print(f"Також, загальний прибуток за цей період склав {income:,.2f} гривень. ")
        print("Дякую, що користуєтесь нашим сервісом!")

    # info about all times expense\income in categories
    def get_statistics(self):
        self.show_list_users()
        num = self.input_number()
        self.display_user_transactions(num, True)

        print()

    def menu_category3(self):
        menu_dict = self.menu.generate_menu_dict(
            self.add_transaction,
            self.delete_transactions,
            self.transaction_transfer_,
            self.get_expenses_income_by_period,
            self.get_statistics,
            self.return_to_menu
        )
        while True:
            self.print_subcategory_menu(self.income_expense_management)
            self.menu_universal(menu_dict, self.menu_category3)


if __name__ == '__main__':
    test = Menu()
    test.main_menu()

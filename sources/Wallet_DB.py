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
    def the_end():
        db_manager.close()
        quit()

    def main_menu(self):
        print("1.{} \n2.{} \n3.{} \n4.{} \nОберіть потрібну цифру: от 1 до 4: "
              .format(*self.main_menu_options))
        menu_dict = {
            1: self.cat1().menu_category1,
            2: self.cat2().menu_category2,
            3: self.cat3().menu_category3,
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
            if self.validate_account_num(num):
                return num

    @staticmethod
    def visual():
        print("-------------------------------------------------------------------------------------------------------")

    @staticmethod
    def show_user_categories():
        for elem in user_categories:
            print(elem)


class CategoryOne(Categories):

    def validate_name_categories(self, name):
        if name in self.user_categories:
            print("Категорія з назвою {} вже існує.".format(name))
            return False
        else:
            return True

    def add_category(self):
        print("\nІснуючі категорії:")
        self.show_user_categories()
        name = input("Введіть назву нової категорії: ")
        if self.validate_name_categories(name):
            self.user_categories.append(name)
            db_manager.create(Category, {"Name": name})
            if name in self.user_categories:
                print(f"Категорія {name} додана")

    def remove_category(self):
        self.show_user_categories()
        name = input("Введіть назву категорії: ")
        if name in self.user_categories:
            self.user_categories.remove(name)
            db_manager.delete(Category, "Name", name)
            if name not in self.user_categories:
                print(f"Категорія {name} видалена")
        elif name not in self.user_categories:
            print(f"Категорію з назвою {name} не знайдено")

    def update_category(self):
        self.show_user_categories()
        name = input("Введіть назву категорії, яку потрібно змінити: ")
        if name in self.user_categories:
            print(f"Категорія з назвою {name} знайдена.")
            index = self.user_categories.index(name)
            while True:
                new_name = input("Введіть нову назву: ")
                if self.validate_name_categories(new_name):
                    db_manager.update(Category, "Name", new_name, "Name", name)
                    self.user_categories[index] = new_name
                    print(f"Назва категорії {name} змінена на {new_name}")
                    break
        else:
            print(f"Категорія з назвою {name} не знайдена")

    def show_list_categories(self):
        print("Список категорій:")
        print(", ".join(self.user_categories))
        print()

    def menu_category1(self):
        functional = {
            1: self.add_category,
            2: self.remove_category,
            3: self.update_category,
            4: self.show_list_categories,
            5: self.menu.main_menu
        }
        while True:
            self.print_subcategory_menu(self.menu_categories)
            self.menu_universal(5, functional, self.menu_category1)


class CategoryTwo(Categories):
    # когда удаляют счет удалять из списка lst_account
    @staticmethod
    def generate_account_number():
        digits = list(range(10))
        random.shuffle(digits)
        account_number = ''.join(map(str, digits[:8]))
        return account_number

    def validate_new_account_number(self, account_num):
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

    def add_user_account(self):
        account_number = self.generate_account_number()
        if len(account_number) == 8:
            account_number = self.validate_new_account_number(account_number)
            account_name = self.input_name()
            account_type = self.input_type()
            if account_number in lst_accounts:
                db_manager.create(User_Accounts, {"Number": account_number,
                                                  "Type": account_type,
                                                  "Name": account_name,
                                                  "Balance": 0})
            print('Рахунок створено\n')
            self.display_account_info(account_number)
            self.visual()
        else:
            print("Виникла помилка, спробуйте ще раз")
            return self.add_user_account

    def remove_user_account(self):
        self.show_list_users()
        number_for_delete = input("Введіть номер рахунку для видалення: ")
        number_id = User_Accounts.get(Number=number_for_delete)

        if number_for_delete in lst_accounts:
            db_manager.delete(User_Accounts, "Number", number_for_delete)
            lst_accounts.remove(number_for_delete)
            if number_for_delete not in lst_accounts:
                print(f"Рахунок {number_for_delete} видалено \n")
                db_manager.delete(TransactionAll, "Number", number_id)
        else:
            print("Рахунок не знайдено \n")
            self.remove_user_account()

    def update_menu(self, input_acc):
        def update_account_type():
            update_acc_type = ["1.Дебетовий", "2.Кредитний", "3.Назад"]
            print("{} \n{} \n{}".format(*update_acc_type))
            while True:
                # проверять ввод через функцию  validate_menu_choice
                what_type = input("Оберіть пункт: ")
                if what_type == "1":
                    db_manager.update(User_Accounts, "Type", "Дебетовий", "Number", input_acc)
                    print("Тип рахунку змінено на Дебетовий \n")
                    self.display_account_info(input_acc)
                    return

                elif what_type == "2":
                    db_manager.update(User_Accounts, "Type", "Кредитний", "Number", input_acc)
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
                    # cursor.execute("UPDATE User_Accounts SET Name = ? WHERE Number = ?", (new_name, input_acc))
                    db_manager.update(User_Accounts, "Name", new_name, "Number", input_acc)
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

    def update_user_account(self):
        self.show_list_users()
        input_acc = input("Введіть номер рахунку: ")
        if input_acc in lst_accounts:
            print("Рахунок знайдено")
            self.display_account_info(input_acc)
            print()
            self.update_menu(input_acc)
        else:
            print("Рахунок не знайдено, спробуйте ще раз")
            self.update_user_account()

    def show_list_users(self):
        if len(lst_accounts) == 0:
            print("Рахунків нема")
        for i in lst_accounts:
            self.display_account_info(i)

    def menu_category2(self):
        functional = {
            1: self.add_user_account,
            2: self.remove_user_account,
            3: self.update_user_account,
            4: self.show_list_users,
            5: self.menu.main_menu
        }
        while True:
            self.print_subcategory_menu(self.bank_account)
            self.menu_universal(5, functional, self.menu_category2)


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

    # transfer money between accounts
    # update structure for func
    def transfer_money(self):
        self.display_number_and_balance()
        print("Номер відправника")
        from_num = self.input_number()
        print("Номер рахунку: {}".format(from_num))
        self.display_balance(from_num)
        print()
        print("Номер одержувача")
        to_num = self.input_number()
        transfer_id = self.generate_transaction_id()
        date = self.generate_random_date()
        from_num_object = User_Accounts.get(Number=from_num)
        if from_num_object.Balance != 0:
            while True:
                amount = float(input("Введіть суму для переводу: "))
                if amount > 0:
                    break
                else:
                    print("Сума повинна бути більше нуля. Будь ласка, введіть коректну суму.")

            if from_num_object.Balance > amount:

                cat_id = Category.get(Name="Перекази")
                db_manager.create(TransactionAll, {"Number": from_num_object,
                                                   "Type": "Витрата",
                                                   "Category": cat_id,
                                                   "Date": date,
                                                   "TransactionID": transfer_id,
                                                   "Amount": amount})

                to_num_object = User_Accounts.get(Number=to_num)
                db_manager.create(TransactionAll, {"Number": to_num_object,
                                                   "Type": "Дохід",
                                                   "Category": cat_id,
                                                   "Date": date,
                                                   "TransactionID": transfer_id,
                                                   "Amount": amount})

                self.update_balance("Витрата", from_num, amount)
                self.update_balance("Дохід", to_num, amount)

                print("Транзакція пройшла успішно")
                print(f"Відправник: {from_num_object.Name} | Отримувач: {to_num_object.Name}")
                print()

            else:
                print("Недостатньо коштів на рахунку")
        else:
            print("Баланс рахунку: {} пустий".format(from_num))

    # info about expense\income time interval
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
            self.menu_universal(6, functional, self.menu_category3)


test = Menu()
test.main_menu()

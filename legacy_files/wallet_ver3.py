import re
from datetime import datetime, timedelta
import random
from core.database_manager_ORM import DatabaseManager
from core.models import *
from menu_old import MenuManager
import os

# ----------------------------------------PATH DATABASE FILE----------------------------------------------------

db_path = os.path.join("db", "wallet_test.db")
db_manager = DatabaseManager(db_path)

# --------------------------------------------------------------------------------------------------------------
user_categories = [elem.Name for elem in Category]
lst_accounts = [elem.Number for elem in UserAccounts]


# ----------------------------------------------------------------------------------------------------------------


class BaseClass:

    def __init__(self):
        # class Menu
        self.menu = MenuManager(CategoryManager, UserManager, AccountManager)

        # CategoryManager
        self.menu_categories = ["Додати категорію", "Видалити категорію", "Змінити дані про категорію",
                                "Перегляд списку категорій", "Назад"]
        self.user_categories = user_categories

        # UserManager
        self.bank_account = ["Створити новий рахунок", "Видалити рахунок", "Змінити дані рахунку",
                             "Переглянути список рахунків", "Назад"]

        # AccountManager
        self.income_expense_management = ["Додати транзакцію",
                                          "Видалити транзакцію",
                                          "Переведення грошей з рахунку на рахунок",
                                          "Перевірка витрат/прибутків за певний період",
                                          "Отримання статистики прибутків/витрат за певний період по категоріях",
                                          "Назад"]

    @staticmethod
    def validate_account_num(number):
        if number in lst_accounts:
            return True
        else:
            print("Рахунок не знайдено")
            return False

    # You pass the second argument as True if you need to check for 3.
    # If you need to check for 2, then you don't pass anything.
    @staticmethod
    def validate_menu_choice(variable, include_three=True):
        choices = ["1", "2"]
        if include_three:
            choices.append("3")

        return variable in choices

    @staticmethod
    def display_balance(account_number):
        balance_info = UserAccounts.get(Number=account_number)
        print("Баланс: {:,.2f} грн".format(balance_info.Balance))

    @staticmethod
    def show_basic_user_info():
        # Account Number & Name
        for elem in UserAccounts.select(UserAccounts.Number, UserAccounts.Name):
            print(f"Номер рахунку: {elem.Number}")
            print(f"ПІБ: {elem.Name}\n")

    @staticmethod
    def update_global_lists():
        global user_categories, lst_accounts

        new_categories = [elem.Name for elem in Category]
        new_accounts = [elem.Number for elem in UserAccounts]

        user_categories = new_categories
        lst_accounts = new_accounts

    @staticmethod
    def show_user_categories():
        for elem in user_categories:
            print(elem)

    def display_account_info(self, account_number):
        row = UserAccounts.get(Number=account_number)
        print(f"Номер Рахунку: {row.Number}")
        print(f"Тип: {row.Type}")
        print(f"ПІБ: {row.Name}")
        self.display_balance(row.Number)
        print()

    def display_number_and_balance(self):
        for elem in UserAccounts.select(UserAccounts.Number, UserAccounts.Name):
            print(f"Номер рахунку: {elem.Number}")
            print(f"ПІБ: {elem.Name}")
            self.display_balance(elem.Number)
            print()

    def display_user_transactions(self, account_number, show_for_user=False):
        list_transactions = (TransactionAll
                             .select()
                             .join_from(TransactionAll, UserAccounts)
                             .join_from(TransactionAll, Category)
                             .where(UserAccounts.Number == account_number))
        if list_transactions:
            if show_for_user:
                for transaction in list_transactions:
                    print(
                        f"Категорія: {transaction.Category.Name} | Дата: {transaction.Date} | Тип: {transaction.Type} "
                        f"| Сумма: {transaction.Amount}")
            else:
                self.display_account_info(account_number)
                print("Транзакції:")
                for count, transaction in enumerate(list_transactions, start=1):
                    print(
                        f"{count}. {transaction.Date} | {transaction.Category.Name} | {transaction.Type} "
                        f"| {transaction.Amount} "
                        f"| id:{transaction.TransactionID}")
                self.menu.visual()
                return True
        else:
            print("Транзакцій на рахунку: {} не знайдено\n".format(account_number))
            return False

    def input_number(self):
        while True:
            num = input("Введіть номер рахунку:").strip()
            if num.isnumeric():
                if self.validate_account_num(num):
                    return num
            else:
                print("Введено некоректні дані, спробуйте ще раз.")

    def start(self):
        self.menu.main_menu()

    def return_to_menu(self):
        self.menu.main_menu()


class CategoryManager(BaseClass):

    @staticmethod
    def category_name_exists(name):
        return db_manager.verify(Category, "Name", name)

    # ввод от 3х символов
    def create_new_category(self):
        print("Існуючі категорії:")
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

    def category_manager_menu(self):
        list_of_methods = (self.create_new_category,
                           self.remove_category,
                           self.update_category,
                           self.show_list_categories,
                           self.menu.main_menu)

        self.menu.create_menu(list_of_methods, self.menu_categories, self.category_manager_menu)


class UserManager(BaseClass):

    @staticmethod
    def account_number_exists(account_num):
        return db_manager.verify(UserAccounts, "Number", account_num)

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

    def generate_account_number(self):
        digits = list(range(10))
        random.shuffle(digits)
        account_number = ''.join(map(str, digits[:8]))
        if len(account_number) == 8:
            if not self.account_number_exists(account_number):
                return account_number
        else:
            self.generate_account_number()

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
        self.menu.visual()

    @staticmethod
    def add_new_user_to_db(data):
        db_manager.create(UserAccounts, data)
        print('Рахунок створено\n')

    def remove_user_account(self):
        self.show_basic_user_info()
        number_for_delete = self.input_number()
        number_id = UserAccounts.get(Number=number_for_delete)
        if self.account_number_exists(number_for_delete):
            self.delete_user_account_from_db(number_for_delete, number_id)
            self.update_global_lists()
        else:
            self.remove_user_account()

    @staticmethod
    def delete_user_account_from_db(number, number_id):
        db_manager.delete(UserAccounts, "Number", number)
        db_manager.delete(TransactionAll, "Number", number_id)
        print(f"Рахунок {number} видалено \n")

    def update_user_name(self, account_number):
        while True:
            new_name = input("Введіть новий ПІБ: ")
            if self.validate_name(new_name):
                db_manager.update(UserAccounts, "Name", new_name, "Number", account_number)
                print("Інформацію оновлено")
                self.display_account_info(account_number)
                return

    def update_user_type_on_credit(self, account_number):
        db_manager.update(UserAccounts, "Type", "Кредитний", "Number", account_number)
        print("Тип рахунку змінено на Кредитний \n")
        self.display_account_info(account_number)

    def update_user_type_on_debit(self, account_number):
        db_manager.update(UserAccounts, "Type", "Дебетовий", "Number", account_number)
        print("Тип рахунку змінено на Дебетовий \n")
        self.display_account_info(account_number)

    def display_user_type_update_menu(self, account_number):
        update_menu_type_lst = ["Дебетовий", "Кредитний", "Назад"]
        # menu_dict = self.menu.generate_menu_dict(
        #     lambda: self.update_user_type_on_debit(account_number),
        #     lambda: self.update_user_type_on_credit(account_number),
        #     lambda: self.display_user_data_update_menu(account_number))
        #
        # while True:
        #     self.menu.print_subcategory_menu(update_menu_type_lst)
        #     choice = input("Оберіть потрібний пункт: ")
        #     if choice.isdigit() and int(choice) in menu_dict:
        #         menu_dict[int(choice)]()
        #         break
        #     else:
        #         print("Неправильний вибір, спробуйте ще раз.")

        list_of_methods = (lambda: self.update_user_type_on_debit(account_number),
                           lambda: self.update_user_type_on_credit(account_number),
                           lambda: self.display_user_data_update_menu(account_number))

        self.menu.create_menu(list_of_methods, update_menu_type_lst,
                              lambda: self.display_user_type_update_menu(account_number))

    def display_user_data_update_menu(self, account_number=None):
        update_menu_lst = ["Тип", "ПІБ", "Повернутись в меню"]

        list_of_methods = (lambda: self.display_user_type_update_menu(account_number),
                           lambda: self.update_user_name(account_number),
                           self.user_manager_menu)

        self.menu.create_menu(list_of_methods, update_menu_lst, self.display_user_data_update_menu)

    def update_user_data(self):
        self.show_detailed_user_info()
        account_number = self.input_number()
        print("Рахунок знайдено")
        print()
        self.display_account_info(account_number)
        self.display_user_data_update_menu(account_number)

    def show_detailed_user_info(self):
        if len(lst_accounts) == 0:
            print("Рахунків нема")
        for i in lst_accounts:
            self.display_account_info(i)

    def user_manager_menu(self):
        list_of_methods = (self.create_user_account,
                           self.remove_user_account,
                           self.update_user_data,
                           self.show_detailed_user_info,
                           self.return_to_menu)

        self.menu.create_menu(list_of_methods, self.bank_account, self.user_manager_menu)


class AccountManager(CategoryManager, UserManager, BaseClass):

    @staticmethod
    def generate_random_date():
        current_time = datetime.now()
        time_speed = random.uniform(0, 5)
        step = timedelta(days=1)
        current_time += step * time_speed
        formatted_datetime = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_datetime

    @staticmethod
    def generate_transaction_id():
        rand_num = random.randint(100000, 999999)
        new_transaction_id = f"TRX{rand_num}"
        return new_transaction_id

    def validate_money_input(self):
        date = self.generate_random_date()

        while True:
            self.show_list_categories()
            category_input = input("Введіть назву однієї з категорій: ")
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
        pattern = r"\d{4}-\d{2}-\d{2}"  # Format YYYY-MM-DD
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
                db_manager.update(UserAccounts, 'Balance', UserAccounts.Balance - amount, 'Number', account_number)
            else:
                db_manager.update(UserAccounts, 'Balance', UserAccounts.Balance + amount, 'Number', account_number)
        elif transaction_type == "Витрата":
            if is_transaction_cancelled:
                db_manager.update(UserAccounts, 'Balance', UserAccounts.Balance + amount, 'Number', account_number)
            else:
                db_manager.update(UserAccounts, 'Balance', UserAccounts.Balance - amount, 'Number', account_number)

    def add_transaction(self):
        self.show_detailed_user_info()
        trans_id = self.generate_transaction_id()
        account_num = self.input_number()
        self.display_balance(account_num)
        date, category, amount, transaction_type, transaction_str = self.validate_money_input()
        num_id, cat_id = UserAccounts.get(Number=account_num), Category.get(Name=category)
        db_manager.create(TransactionAll, {"Number": num_id,
                                           "Type": transaction_type,
                                           "Category": cat_id,
                                           "Date": date,
                                           "TransactionID": trans_id,
                                           "Amount": amount})

        self.update_balance(transaction_type, account_num, amount)
        print("Транзакція додана: {} | {} | {}\n".format(date, category, transaction_str))
        self.display_account_info(account_num)

    def delete_transaction(self):
        self.show_detailed_user_info()
        account_num = self.input_number()
        if self.display_user_transactions(account_num):
            transaction_id = self.input_transaction_id()
            list_transaction_for_del = TransactionAll.select().where(TransactionAll.TransactionID == transaction_id)
            for elem in list_transaction_for_del:
                self.update_balance(elem.Type, elem.Number.Number, elem.Amount, is_transaction_cancelled=True)
            db_manager.delete(TransactionAll, "TransactionID", transaction_id)

    def transaction_transfer(self):
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
            from_number_object = UserAccounts.get(Number=from_number)
            to_number_object = UserAccounts.get(Number=to_number)
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
        self.show_detailed_user_info()
        num = self.input_number()
        print("Для перевірки витрат і прибутків за певний період, будь ласка, введіть дату початку періоду та дату "
              "його завершення. Формат дати має бути наступним: рік-місяць-день (наприклад, 2023-05-16)")
        start_date, end_date = self.validate_date_input()
        income = 0
        expense = 0
        list_transaction = (TransactionAll.select().join(UserAccounts).where(
            (UserAccounts.Number == num) &
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
        self.show_detailed_user_info()
        num = self.input_number()
        self.display_user_transactions(num, True)
        print()

    def account_manager_menu(self):

        list_of_methods = (self.add_transaction,
                           self.delete_transaction,
                           self.transaction_transfer,
                           self.get_expenses_income_by_period,
                           self.get_statistics,
                           self.return_to_menu)

        self.menu.create_menu(list_of_methods, self.income_expense_management, self.account_manager_menu)


if __name__ == '__main__':
    test = BaseClass()
    test.start()

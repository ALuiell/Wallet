"""Тільки пусті функції для тестування"""
import re
import datetime
import random

menu_categories = ["Додати категорію", "Видалити категорію", "Змінити дані про категорію",
                   "Перегляд списку категорій", "Назад"]

bank_account = ["Створити новий рахунок", "Видалити рахунок", "Змінити дані рахунку",
                "Переглянути список рахунків", "Переглянути інформацію про рахунок", "Назад"]

income_expense_management = ["Додавання витрат та прибутків до певного рахунку",
                             "Видалення прибутків та витрат з певного рахунку",
                             "Переведення грошей з рахунку на рахунок",
                             "Перевірка витрат/прибутків за певний період",
                             "Отримання статистики прибутків/витрат за певний період по днях, по категоріях",
                             "Назад"]
search_transactions_op = ["Можливість пошуку категорій, витрат прибутків за категорією",
                          "Можливість пошуку прибутку витрати за сумою датою", "Назад"]
main_menu_options = ["Управління категоріями витрат та доходів", "Управління рахунками",
                     "Управління витратами та доходами", "Пошук", "Вихід"]

user_categories = ["Їжа", "Одяг і взуття", "Розваги", "Транспорт", "Комунальні послуги", "Оплата житла",
                   "Здоров'я та медицина", "Подарунки та благодійність", "Краса та гігієна",
                   "Офісні витрати", "Домашні тварини", "Подорожі", "Освіта та розвиток", "Інші витрати"]

user_categories1 = {}

user_accounts = {
    "12345678": {"type": "Дебетовий", "name": "John Smith", "transactions": [], "balance": 0.0},
    "87654321": {"type": "Кредитний", "name": "Jane Doe", "transactions": [], "balance": 0.0},
    "65432198": {"type": "Дебетовий", "name": "Michael Johnson", "transactions": [], "balance": 0.0}
}
lst_accounts = ["12345678", "87654321", "65432198"]

lst_transfer = {}


def rewrite_dict():
    for i in user_categories:
        user_categories1[i] = {}


class Menu:

    def __init__(self):
        self.main_menu_options = main_menu_options
        self.cat1 = CategoryOne
        self.cat2 = CategoryTwo
        self.cat3 = CategoryThree
        self.cat4 = CategoryFour

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
        quit()

    def main_menu(self):
        print("1.{} \n2.{} \n3.{} \n4.{} \n5.{} \nОберіть потрібну цифру: от 1 до 5: "
              .format(*self.main_menu_options))
        menu_dict = {
            1: self.cat1().menu_cat1,
            2: self.cat2().menu_cat2,
            3: self.cat3().menu_cat3,
            4: self.cat4().menu_cat4,
            5: self.the_end
        }
        try:
            choice = int(input("Введіть потрібний пункт: "))
            self.menu_loop(choice, 5, menu_dict, self.main_menu)
        except ValueError:
            print("\nВи ввели неправильне значення. Спробуйте ще раз.\n")
            self.main_menu()


class Categories:

    def __init__(self):
        # class Menu
        self.menu = Menu()

        # CategoryOne
        self.menu_categories = menu_categories
        self.user_categories = user_categories
        self.user_categories1 = user_categories1

        # CategoryTwo
        self.bank_account = bank_account
        self.user_accounts = user_accounts

        # CategoryThree
        self.income_expense_management = income_expense_management
        self.lst_transfer = lst_transfer

        # 4 CategoryFour
        self.search_transactions_op = search_transactions_op

        # 5 main_menu
        self.main_menu_options = main_menu_options

        # universal
        self.lst_accounts = lst_accounts

    @staticmethod
    def print_subcategory_menu(lst):
        for i, elem in enumerate(lst, start=1):
            print(f"{i}.{elem}")

    def return_to_menu(self):
        self.menu.main_menu()

    # перевіряє на тип даних та відправляє у виконання функції menu_loop
    def menu_universal(self, num, functional, menu_name):
        try:
            choice = int(input("Введіть потрібний пункт: "))
            self.menu.menu_loop(choice, num, functional, menu_name)
        except ValueError:
            print("\nВи ввели неправильне значення. Спробуйте ще раз.\n")

    def validate_account_num(self, num):
        if num in self.lst_accounts:
            return True
        else:
            print("Рахунок не знайдено")
            return False

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

    def display_balance(self, account_num):
        balance_info = self.user_accounts.get(account_num)
        print("Баланс: {:,.2f} грн".format(balance_info.get("balance")))

    def display_account_info(self, account_num):
        print("Номер Рахунку: {}".format(account_num))
        print(f"ПІБ: {self.user_accounts[account_num]['name']}")
        print(f"Тип: {self.user_accounts[account_num]['type']}")
        self.display_balance(account_num)
        print()

    def display_num_balance(self):
        for key, val in self.user_accounts.items():
            print("Номер рахунку: {}".format(key))
            self.display_balance(key)
            print()

    def display_all_num(self):
        for key, val in self.user_accounts.items():
            print("Номер рахунку: {}".format(key))

    def display_transactions(self, account_num):
        """Отображение транзакций"""
        transactions = self.user_accounts[account_num]["transactions"]
        if len(transactions) != 0:
            self.display_account_info(account_num)
            print("Транзакції: ")
            for i, transaction in enumerate(transactions):
                print(
                    f"{i + 1}. {transaction['date']} | {transaction['category']} | {transaction['transaction']}"
                    f" | id:{transaction['transaction_id']}")
            self.visual()
        else:
            print("Транзакцій на рахунку: {} не знайдено\n".format(account_num))

    def input_num(self):
        while True:
            num = input("Введіть номер рахунку:")
            if self.validate_account_num(num):
                return num

    @staticmethod
    def visual():
        print("-------------------------------------------------------------------------------------------------------")


class CategoryOne(Categories):

    def validate_name_categories(self, name):
        if name in self.user_categories:
            print("Категорія с такою назвою вже існує.")
            return False
        else:
            return True

    def add_category(self):
        print("\nІснуючі категорії:")
        name = input("Введіть назву нової категорії: ")
        if self.validate_name_categories(name):
            self.user_categories.append(name)
            self.user_categories1[name] = {}
            if name in self.user_categories:
                print("Категорія додана")

    def remove_category(self):
        print("remove_cat")

    def update_category(self):
        print("welcome to the update_category")

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

    def add_user_acc(self):
        print("welcome to the add_user_acc")

    def remove_user_acc(self):
        print('welcome to the remove_user_acc')

    def change_user_acc(self):
        print('welcome to the change_user_acc')

    def lst_user_acc(self):
        if len(self.user_accounts) == 0:
            print("Рахунків нема")
        else:
            print("Список рахунків:\n")
            for elem, info in self.user_accounts.items():
                self.display_account_info(elem)
        self.visual()

    def display_acc_info(self):
        self.display_all_num()
        num = self.input_num()
        self.display_account_info(num)
        self.display_transactions(num)

    def menu_cat2(self):
        functional = {
            1: self.add_user_acc,
            2: self.remove_user_acc,
            3: self.change_user_acc,
            4: self.lst_user_acc,
            5: self.display_acc_info,
            6: self.menu.main_menu
        }

        while True:
            self.print_subcategory_menu(self.bank_account)
            self.menu_universal(6, functional, self.menu_cat2)


class CategoryThree(CategoryOne, CategoryTwo, Categories):

    @staticmethod
    def generate_random_date():
        """Генерация даты"""
        current_time = datetime.datetime.now()
        time_speed = random.uniform(0, 400)  # случайное значение скорости времени
        step = datetime.timedelta(days=1)
        current_time += step * time_speed
        year = current_time.year
        month = current_time.month
        day = current_time.day
        return f"{day:02d}.{month:02d}.{year}"

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

        pattern = r"^[+-]\d+$"
        while True:
            trans = input("Введіть значення у форматі +/-сума, наприклад, "
                          "+100 для додавання 100 грн або -100 для віднімання 100 грн: ")
            if re.match(pattern, trans):
                break
            print("Введено неправильно. \nПриклад: +100, -100")

        return date, category_input, trans

    def add_transaction(self):
        # Show a list of user accounts for selection
        self.lst_user_acc()
        trans_id = self.generate_transaction_id()
        # Get the account number from the user input
        account_num = self.input_num()
        self.display_balance(account_num)
        # Get the date, category, and transaction details from the user input
        date, category, transaction = self.validate_money_input()
        # Get the list of transactions and current balance for the selected account
        transactions = self.user_accounts[account_num]["transactions"]
        balance = self.user_accounts[account_num]["balance"]
        # Add the new transaction to the list of transactions and update the balance
        transactions.append(
            {"transaction_id": trans_id, "date": date, "category": category, "transaction": transaction})
        balance += float(transaction)
        # Update the transactions list and balance for the selected account
        self.user_accounts[account_num]["transactions"] = transactions
        self.user_accounts[account_num]["balance"] = balance
        print("Транзакція додана: {} | {} | {}\n".format(date, category, transaction))
        self.display_account_info(account_num)
        # Add the new transaction to the user_categories1 dictionary
        if category not in self.user_categories1:
            self.user_categories1[category] = {}
        if account_num not in self.user_categories1[category]:
            self.user_categories1[category][account_num] = {}
        if date not in self.user_categories1[category][account_num]:
            self.user_categories1[category][account_num][date] = []
        new_transaction = {"transaction": transaction, "transaction_id": trans_id}
        self.user_categories1[category][account_num][date].append(new_transaction)
        print(user_categories1)

    def delete_transaction(self, account_num, transaction, transactions):
        """Удаление обычной транзакции"""
        """account_num: номер счета, transaction: словарь транзакции в списке,
        transactions: список транзакций указанного счета """

        transaction_amount = float(transaction["transaction"])
        if transaction_amount > 0:
            balance = self.user_accounts[account_num]["balance"] - transaction_amount
        else:
            balance = self.user_accounts[account_num]["balance"] + abs(transaction_amount)
        transactions.remove(transaction)
        self.user_accounts[account_num]["transactions"] = transactions
        self.user_accounts[account_num]["balance"] = balance

    def delete_transfer_transaction(self, account_num, transaction_id):
        """Удаление перевода со второго счета"""
        transaction_info = self.lst_transfer[transaction_id]
        account_num1 = transaction_info["to_account"]  # если удаляется транзакция со счета получателя True
        account_num2 = transaction_info["from_account"]  # если удаляется транзакция со счета отправителя False

        verify = "2"
        if account_num == account_num2:
            verify = "1"

        def delete(account_number):
            transactions = self.user_accounts[account_number]["transactions"]
            for elem in transactions:
                if transaction_id == elem["transaction_id"]:
                    print("id транзакции на втором счету найден")
                    transaction_amount = float(elem["transaction"])
                    if transaction_amount > 0:
                        balance = self.user_accounts[account_number]["balance"] - transaction_amount
                    else:
                        balance = self.user_accounts[account_number]["balance"] + abs(transaction_amount)
                    transactions.remove(elem)
                    self.user_accounts[account_number]["transactions"] = transactions
                    self.user_accounts[account_number]["balance"] = balance
                    break

        if verify == "1":
            delete(account_num1)
        elif verify == "2":
            delete(account_num2)

        del lst_transfer[transaction_id]

    def delete_transactions(self):
        account_num = self.input_num()
        transactions = user_accounts[account_num]["transactions"]
        self.display_transactions(account_num)
        transaction_id = input("Введіть id транзакції: ")
        for elem in transactions:
            if transaction_id == elem["transaction_id"]:
                if elem["category"] == "Перекази":
                    transfer_transaction = elem
                    self.delete_transaction(account_num, transfer_transaction, transactions)
                    self.delete_transfer_transaction(account_num, transaction_id)
                else:
                    transaction = elem
                    self.delete_transaction(account_num, transaction, transactions)
        print("Транзакція видалена")

    def transfer_money(self):
        """Перевод денег между счетами"""
        self.display_num_balance()
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
        if user_accounts[from_num1]["balance"] != 0.0:
            amount = float(input("Введіть суму для переводу: "))

            trans1 = "-{:.2f}".format(amount)
            trans2 = "+{:.2f}".format(amount)

            if user_accounts[from_num1]["balance"] >= amount:
                user_accounts[from_num1]["balance"] -= amount
                user_accounts[to_num2]["balance"] += amount
                user_accounts[from_num1]["transactions"].append(
                    {"transaction_id": transfer_id, "date": date1, "category": category, "transaction": trans1})

                user_accounts[to_num2]["transactions"].append(
                    {"transaction_id": transfer_id, "date": date1, "category": category, "transaction": trans2})
                print("\nПереказ виконано\n")

                lst_transfer[transfer_id] = {"date": date1, "from_account": from_num1, "to_account": to_num2,
                                             "amount": amount}
                self.visual()
                print(user_accounts)
            else:
                print("Недостатньо коштів на рахунку")
        else:
            print("Баланс рахунку: {} пустий".format(from_num1))

    @staticmethod
    def validate_date_input(date):
        pattern = r"\d{2}\.\d{2}\.\d{4}"
        if re.match(pattern, date):
            return True
        else:
            return False

    def get_expenses_income_by_period(self):
        self.display_all_num()
        num = self.input_num()
        print("Для перевірки витрат і прибутків за певний період, будь ласка, введіть дату початку періоду та дату "
              "його завершення. Формат дати має бути наступним: день.місяць.рік (наприклад, 01.05.2023)")

        while True:
            start_date_input = input("Введіть дату початку періоду: ")
            if self.validate_date_input(start_date_input):
                date_end_input = input("Введіть дату кінця періоду: ")
                if self.validate_date_input(date_end_input):

                    start_date = datetime.datetime.strptime(start_date_input, "%d.%m.%Y")
                    end_date = datetime.datetime.strptime(date_end_input, "%d.%m.%Y")
                    income = 0
                    expense = 0
                    transactions = self.user_accounts[num]["transactions"]
                    for transaction in transactions:
                        transaction_date = datetime.datetime.strptime(transaction['date'], "%d.%m.%Y")
                        transaction_amount = float(transaction['transaction'][1:])
                        transaction_type = transaction['transaction'][0]
                        if start_date <= transaction_date <= end_date:
                            if transaction_type == '+':
                                income += transaction_amount
                            elif transaction_type == '-':
                                expense += transaction_amount
                    print(f"Для введеного Вами періоду часу, загальна сума витрат становить {expense:,.2f} гривень.")
                    print(f"Також, загальний прибуток за цей період склав {income:,.2f} гривень. ")
                    print("Дякую, що користуєтесь нашим сервісом!")

    # 3.5. Можливість отримання статистики прибутків витрат за певний період по днях, по категоріях # вывести стату за нужный опльзователю день либо 3.4 + категории
    def get_statistics(self):
        num = self.input_num()
        self.display_lst_user_cat()
        while True:
            category = input("Введіть назву категорії: ")
            if self.validation_name_category(category):
                transaction = self.user_categories1[category][num]
                for elem in transaction:
                    print(elem)

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


class CategoryFour(Categories):

    def search_by_category(self):
        print("welcome to the search_by_category ")
        pass

    def search_by_amount_date(self):
        print("welcome to the search_by_amount_date ")
        pass

    def menu_cat4(self):
        functional = {
            1: self.search_by_category,
            2: self.search_by_amount_date,
            3: self.return_to_menu
        }
        while True:
            self.print_subcategory_menu(self.income_expense_management)
            self.menu_universal(3, functional, self.menu_cat4)


rewrite_dict()
test = Menu()
test.main_menu()

import re
import random
from db_config import db_manager
from models import UserAccounts, TransactionAll, Category
from datetime import datetime, timedelta
from general_utils import GeneralUtils, user_categories


class AccountDataStore:
    def __init__(self):
        self.income_expense_management = ["Додати транзакцію",
                                          "Видалити транзакцію",
                                          "Переведення грошей з рахунку на рахунок",
                                          "Перевірка витрат/прибутків за певний період",
                                          "Отримання статистики прибутків/витрат за певний період по категоріях",
                                          "Назад"]


class AccountDisplayManager:
    def __init__(self):
        self.general_utils = GeneralUtils()

    def display_user_transactions(self, account_number: str, show_for_user=False) -> bool:
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
                self.general_utils.display_account_info(account_number)
                print("Транзакції:")
                for count, transaction in enumerate(list_transactions, start=1):
                    print(
                        f"{count}. {transaction.Date} | {transaction.Category.Name} | {transaction.Type} "
                        f"| {transaction.Amount} "
                        f"| id:{transaction.TransactionID}")
                self.general_utils.visual()
                return True
        else:
            print("Транзакцій на рахунку: {} не знайдено\n".format(account_number))
            return False

    def display_number_and_balance(self):
        # Account Number, Name, Balance
        for elem in UserAccounts.select(UserAccounts.Number, UserAccounts.Name):
            print(f"Номер рахунку: {elem.Number}")
            print(f"ПІБ: {elem.Name}")
            self.general_utils.display_balance(elem.Number)
            print()


class AccountManagerUtils:

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

    @staticmethod
    def input_transaction_id():
        pattern = r"^TRX\d{6}$"
        while True:
            transaction_id = input("Введіть id транзакції: ")
            if re.match(pattern, transaction_id):
                return transaction_id
            else:
                print("Невірний формат id транзакції. Спробуйте ще раз.")


class AccountValidationManager:

    @staticmethod
    def validate_money_input():
        date = AccountManagerUtils.generate_random_date()

        while True:
            GeneralUtils().show_list_categories()
            category_input = input("Введіть назву однієї з категорій: ")
            if category_input in user_categories:
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


class AccountManager:
    def __init__(self):
        self.data_store = AccountDataStore()
        self.display_manager = AccountDisplayManager()
        self.validation_manager = AccountValidationManager()
        self.utils = AccountManagerUtils()
        self.general_utils = GeneralUtils()

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
        self.general_utils.show_info_about_all_users()
        trans_id = self.utils.generate_transaction_id()
        account_num = self.general_utils.input_number()
        self.general_utils.display_balance(account_num)
        date, category, amount, transaction_type, transaction_str = self.validation_manager.validate_money_input()
        num_id, cat_id = UserAccounts.get(Number=account_num), Category.get(Name=category)
        db_manager.create(TransactionAll, {"Number": num_id,
                                           "Type": transaction_type,
                                           "Category": cat_id,
                                           "Date": date,
                                           "TransactionID": trans_id,
                                           "Amount": amount})

        self.update_balance(transaction_type, account_num, amount)
        print("Транзакція додана: {} | {} | {}\n".format(date, category, transaction_str))
        self.general_utils.display_account_info(account_num)

    def delete_transaction(self):
        self.general_utils.show_info_about_all_users()
        account_num = self.general_utils.input_number()
        if self.display_manager.display_user_transactions(account_num):
            transaction_id = self.utils.input_transaction_id()
            list_transaction_for_del = TransactionAll.select().where(TransactionAll.TransactionID == transaction_id)
            for elem in list_transaction_for_del:
                self.update_balance(elem.Type, elem.Number.Number, elem.Amount, is_transaction_cancelled=True)
            db_manager.delete(TransactionAll, "TransactionID", transaction_id)
            print("Транзакція видалено успішно, баланс оновлено.")

    def transaction_transfer(self):
        def get_transfer_info():
            self.general_utils.display_number_and_balance()
            print("Номер відправника")
            from_num = self.general_utils.input_number()
            print(f"Номер рахунку: {from_num}")
            self.general_utils.display_balance(from_num)
            print()
            print("Номер одержувача")
            to_num = self.general_utils.input_number()
            transaction_transfer_id = self.utils.generate_transaction_id()
            date = self.utils.generate_random_date()
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
        self.general_utils.show_info_about_all_users()
        num = self.general_utils.input_number()
        print("Для перевірки витрат і прибутків за певний період, будь ласка, введіть дату початку періоду та дату "
              "його завершення. Формат дати має бути наступним: рік-місяць-день (наприклад, 2023-05-16)")
        start_date, end_date = self.validation_manager.validate_date_input()
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
        self.general_utils.show_info_about_all_users()
        num = self.general_utils.input_number()
        self.display_manager.display_user_transactions(num, True)
        print()

    def account_manager_menu(self, menu_manager):
        list_of_methods = (
            self.add_transaction,
            self.delete_transaction,
            self.transaction_transfer,
            self.get_expenses_income_by_period,
            self.get_statistics,
            menu_manager.main_menu
        )

        menu_manager.create_menu(list_of_methods, self.data_store.income_expense_management)

from models import *

# ----------------------------------------PATH DATABASE FILE----------------------------------------------------
db_path = "/db\\wallet_test.db"

# --------------------------------------------------------------------------------------------------------------
user_categories = [elem.Name for elem in Category]
lst_accounts = [elem.Number for elem in User_Accounts]


# ----------------------------------------------------------------------------------------------------------------

class GeneralUtils:
    @staticmethod
    def update_global_lists():
        global user_categories, lst_accounts

        new_categories = [elem.Name for elem in Category]
        new_accounts = [elem.Number for elem in User_Accounts]

        user_categories = new_categories
        lst_accounts = new_accounts

    def input_number(self):
        while True:
            num = input("Введіть номер рахунку:").strip()
            if num.isnumeric():
                if self.validate_account_num(num):
                    return num
            else:
                print("Введено некоректні дані, спробуйте ще раз.")

    @staticmethod
    def validate_account_num(number):
        if number in lst_accounts:
            return True
        else:
            print("Рахунок не знайдено")
            return False

    def show_list_categories(self, inline=False):
        if inline:
            print("Список категорій:")
            print(", ".join(user_categories))
        else:
            for elem in user_categories:
                print(elem)
        self.visual()

    def display_account_info(self, account_number):
        row = User_Accounts.get(Number=account_number)
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
    def display_balance(account_number):
        balance_info = User_Accounts.get(Number=account_number)
        print("Баланс: {:,.2f} грн".format(balance_info.Balance))

    @staticmethod
    def show_basic_users_info():
        # Account Number & Name
        for elem in User_Accounts.select(User_Accounts.Number, User_Accounts.Name):
            print(f"Номер рахунку: {elem.Number}")

    def show_info_about_all_users(self):
        # # Account Number, Account Type, Name, Balance
        if len(lst_accounts) == 0:
            print("Рахунків нема")
        for i in lst_accounts:
            self.display_account_info(i)

    @staticmethod
    def visual():
        print("-------------------------------------------------------------------------------------------------------")

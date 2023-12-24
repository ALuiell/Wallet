"""3 Категорія"""

menu_categories = ["Додати категорію", "Видалити категорію", "Змінити дані про категорію",
                   "Перегляд списку категорій", "Назад"]
user_categories = []
bank_account = ["Створити новий рахунок", "Видалити рахунок", "Змінити дані рахунку",
                "Переглянути список рахунків", "Переглянути кошти на рахунку", "Назад"]
user_accounts = {}
income_expense_management = ["Додавання/видалення витрат до певного рахунку",
                             "Додавання/видалення прибутків до певного рахунку",
                             "Переведення грошей з рахунку на рахунок",
                             "Перевірка витрат/прибутків за певний період",
                             "Отримання статистики прибутків/витрат за певний період по днях, по категоріях",
                             "Назад"]
search_transactions_op = ["Можливість пошуку категорій, витрат прибутків за категорією",
                          "Можливість пошуку прибутку витрати за сумою датою", "Назад"]
main_menu_options = ["Управління категоріями витрат та доходів", "Управління рахунками",
                     "Управління витратами та доходами", "Пошук", "Вихід"]


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
        self.user_categories = []

        # CategoryTwo
        self.bank_account = bank_account
        self.user_accounts = {
            "12345678": {"type": "Дебетовий", "name": "John Smith", "transactions": [], "balance": 0},
            "87654321": {"type": "Кредитний", "name": "Jane Doe", "transactions": [], "balance": 0},
            "65432198": {"type": "Дебетовий", "name": "Michael Johnson", "transactions": [], "balance": 0}
        }

        # CategoryThree
        self.income_expense_management = income_expense_management

        # 4 CategoryFour
        self.search_transactions_op = search_transactions_op

        # 5 main_menu
        self.main_menu_options = main_menu_options

        # universal
        self.lst_accounts = ["12345678", "87654321", "65432198"]

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
        print("Баланс: {}".format(balance_info.get("balance")))


class CategoryOne(Categories):

    def add_category(self):
        print("add_category")

    def remove_category(self):
        print("remove_cat")

    def update_category(self):
        print("welcome to the update_category")

    def list_category(self):
        print("welcome to the list_category")

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

    def display_account_info(self, account_num):
        account_info = self.user_accounts.get(account_num)
        print("Номер Рахунку: {}\nПІБ: {}\nТип: {} \nБаланс: {}".format(
            account_num,
            account_info.get('name'),
            account_info.get('type'),
            account_info.get("balance")
        ))

    def lst_user_acc(self):
        if len(self.user_accounts) == 0:
            print("Рахунків нема")
        for i in self.user_accounts:
            self.display_account_info(i)
            print()

    def balance_users_acc(self):
        print("welcome to the balance_users_acc")

    def menu_cat2(self):
        functional = {
            1: self.add_user_acc,
            2: self.remove_user_acc,
            3: self.change_user_acc,
            4: self.lst_user_acc,
            5: self.balance_users_acc,
            6: self.menu.main_menu
        }
        while True:
            self.print_subcategory_menu(self.bank_account)
            self.menu_universal(6, functional, self.menu_cat2)


class CategoryThree(Categories):

    def input_num(self):
        num = input("Введіть номер рахунку:")
        if validate_account_num(num):
            return num

    def add_expense(self):
        print("welcome to the add_expense ")
        pass

    def add_income(self):
        print("welcome to the add_income ")
        pass

    def transfer_money(self):
        print("welcome to the transfer_money ")
        pass

    def check_transactions(self):
        print("welcome to the check_transactions ")
        pass

    def get_statistics(self):
        print("welcome to the get_statistics ")
        pass

    def menu_cat3(self):
        functional = {
            1: self.add_expense,
            2: self.add_income,
            3: self.transfer_money,
            4: self.check_transactions,
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


test = Menu()
test.main_menu()


# методи перевірки та функціоналу -------------------------------------------------------------------------------------
def validate_account_num(account_num):
    if account_num in lst_accounts:
        return True
    else:
        print("Рахунок не знайдено")
        return False


# перевірка двох-трьох пунктного меню

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


def submenu_func_choice(name_func, name_func1, name_func2):
    functional = {
        1: name_func,
        2: name_func1,
        3: name_func2
    }


# методи відображення -------------------------------------------------------------------------------------------------
def display_account_info(account_num):
    account_info = user_accounts.get(account_num)
    print("Номер Рахунку: {}\nПІБ: {}\nТип: {} \nБаланс: {}".format(
        account_num,
        account_info.get('name'),
        account_info.get('type'),
        account_info.get("balance")
    ))


def lst_user_acc():
    if len(user_accounts) == 0:
        print("Рахунків нема")
    for i in user_accounts:
        display_account_info(i)
        print()


def display_balance(account_num):
    balance_info = user_accounts.get(account_num)
    print("Баланс: {}".format(balance_info.get("balance")))


# методи вводу від користувача ----------------------------------------------------------------------------------------
def input_num():
    num = input("Введіть номер рахунку:")
    if validate_account_num(num):
        return num


# 3.1. Можливість додавати/видаляти витрати до певного рахунку --------------------------------------------------------
def expense():
    lst_user_acc()
    num = input_num()

    def add_expense(num):
        print("welcome to the add_expense ")
        pass

    def remove_expense(num):
        print("welcome to the remove_expense")
        pass


# основний функціонал -------------------------------------------------------------------------------------------------
def income():
    def add_income():
        print("welcome to the add_income ")
        pass

    def remove_income():
        print("welcome to the remove_income")
        pass


# Можливість переведення грошей з рахунку на рахунок
def transfer_money():
    print("welcome to the transfer_money ")
    pass


# Можливість перевірки витрат прибутків за певний період
def check_transactions():
    print("welcome to the check_transactions ")
    pass


# Можливість отримання статистики прибутків витрат за певний період по днях, по категоріях
def get_statistics():
    print("welcome to the get_statistics ")
    pass
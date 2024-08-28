import re
import random
from db_config import db_manager
from models import User_Accounts, TransactionAll
from general_utils import GeneralUtils


class UserDataStore:
    def __init__(self):
        self.bank_account = ["Створити новий рахунок", "Видалити рахунок", "Змінити дані рахунку",
                             "Переглянути список рахунків", "Назад"]

        self.selected_account_number = None


class UserDisplayManager:
    def __init__(self):
        self.general_utils = GeneralUtils()

    @staticmethod
    def show_basic_user_info():
        # Account Number & Name
        for elem in User_Accounts.select(User_Accounts.Number, User_Accounts.Name):
            print(f"Номер рахунку: {elem.Number}")
            print(f"ПІБ: {elem.Name}\n")

    def show_detailed_user_info(self):
        self.general_utils.show_info_about_all_users()


class UserValidationManager:

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

    @staticmethod
    def validate_menu_choice(variable, include_three=True):
        choices = ["1", "2"]
        if include_three:
            choices.append("3")

        return variable in choices


class UserManagerUtils:
    def __init__(self):
        self.validation_manager = UserValidationManager()

    def generate_account_number(self):
        digits = list(range(10))
        random.shuffle(digits)
        account_number = ''.join(map(str, digits[:8]))
        if len(account_number) == 8:
            if not self.validation_manager.account_number_exists(account_number):
                return account_number
        else:
            self.generate_account_number()

    @staticmethod
    def validate_menu_choice(variable, include_three=True):
        choices = ["1", "2"]
        if include_three:
            choices.append("3")

        return variable in choices

    def input_name(self):
        while True:
            name = input("Введіть ПІБ: ")
            if self.validation_manager.validate_name(name):
                return name

    def input_type(self):
        while True:
            account_type = input("Оберіть тип: \n1.Дебетовий \n2.Кредитний \nВведіть цифру 1 або 2: ")
            if self.validate_menu_choice(account_type):
                if account_type == "1":
                    return "Дебетовий"
                elif account_type == "2":
                    return "Кредитний"


class UserManager:
    def __init__(self):
        self.data_store = UserDataStore()
        self.display_manager = UserDisplayManager()
        self.validation_manager = UserValidationManager()
        self.general_utils = GeneralUtils()
        self.utils = UserManagerUtils()

    def create_user_account(self):
        account_number = self.utils.generate_account_number()
        account_name = self.utils.input_name()
        account_type = self.utils.input_type()
        data = {"Number": account_number,
                "Type": account_type,
                "Name": account_name,
                "Balance": 0}
        self.add_new_user_to_db(data)
        self.general_utils.display_account_info(data["Number"])
        self.general_utils.update_global_lists()
        self.general_utils.visual()

    @staticmethod
    def add_new_user_to_db(data):
        db_manager.create(User_Accounts, data)
        print('Рахунок створено\n')

    def remove_user_account(self):
        self.general_utils.show_basic_users_info()
        number_for_delete = self.general_utils.input_number()
        number_id = User_Accounts.get(Number=number_for_delete)
        if self.validation_manager.account_number_exists(number_for_delete):
            self.delete_user_account_from_db(number_for_delete, number_id)
            self.general_utils.update_global_lists()
        else:
            self.remove_user_account()

    @staticmethod
    def delete_user_account_from_db(number, number_id):
        db_manager.delete(User_Accounts, "Number", number)
        db_manager.delete(TransactionAll, "Number", number_id)
        print(f"Рахунок {number} видалено \n")

    def update_user_data(self, menu_manager):
        self.display_manager.show_detailed_user_info()
        account_number = self.general_utils.input_number()
        self.data_store.selected_account_number = account_number
        print("Рахунок знайдено")
        print()
        self.general_utils.display_account_info(account_number)
        self.display_user_data_update_menu(menu_manager)

    def display_user_data_update_menu(self, menu_manager):
        update_menu_lst = ["Тип", "ПІБ", "Повернутись в меню"]

        list_of_methods = (self.display_user_type_update_menu,
                           self.update_user_name,
                           lambda: self.user_manager_menu(menu_manager))

        menu_manager.create_menu(list_of_methods, update_menu_lst)

    def display_user_type_update_menu(self, menu_manager):
        # remove the option to choose an account because there are only 2 options
        # account_types = ['Дебетовий', "Кредитний"]
        # account = User_Accounts.get_or_none(Number=self.data_store.selected_account_number)
        # if account.Type == account_types[0]:
        #     while True:
        #         user_confirmation = input(
        #             f"Ваши тип рахунку буде змінений з {account.Type} на {account_types[1]}. Ви Згодні? y/n")
        #         if user_confirmation.lower() == "y":
        #             self.update_user_type_on_credit()
        #         elif user_confirmation.lower() == "n":
        #             self.display_user_data_update_menu(menu_manager)

        update_menu_type_lst = ["Дебетовий", "Кредитний", "Назад"]

        list_of_methods = (self.update_user_type_on_debit,
                           self.update_user_type_on_credit,
                           lambda: self.display_user_data_update_menu(menu_manager))

        menu_manager.create_menu(list_of_methods, update_menu_type_lst)

    def update_user_name(self, test_account_number=None):
        while True:
            new_name = input("Введіть новий ПІБ: ")
            if self.validation_manager.validate_name(new_name):
                # for test
                if test_account_number is None:
                    db_manager.update(User_Accounts, "Name", new_name, "Number",
                                      self.data_store.selected_account_number)
                else:
                    db_manager.update(User_Accounts, "Name", new_name, "Number",
                                      test_account_number)
                print("Інформацію оновлено")
                self.general_utils.display_account_info(self.data_store.selected_account_number)
                return

    def update_user_type_on_credit(self):
        db_manager.update(User_Accounts, "Type", "Кредитний", "Number", self.data_store.selected_account_number)
        print("Тип рахунку змінено на Кредитний \n")
        self.general_utils.display_account_info(self.data_store.selected_account_number)

    def update_user_type_on_debit(self):
        db_manager.update(User_Accounts, "Type", "Дебетовий", "Number", self.data_store.selected_account_number)
        print("Тип рахунку змінено на Дебетовий \n")
        self.general_utils.display_account_info(self.data_store.selected_account_number)

    def user_manager_menu(self, menu_manager):
        list_of_methods = (
            self.create_user_account,
            self.remove_user_account,
            self.update_user_data,
            self.display_manager.show_detailed_user_info,
            menu_manager.main_menu
        )

        menu_manager.create_menu(list_of_methods, self.data_store.bank_account)

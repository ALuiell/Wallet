from general_utils import GeneralUtils
from user_manager import UserDisplayManager


class MenuManager:
    def __init__(self, cat_manager=None, u_manager=None, acc_manager=None):
        self.main_menu_options = ["Управління категоріями витрат та доходів", "Управління рахунками",
                                  "Управління витратами та доходами", "Вихід"]
        self.category_manager = cat_manager
        self.user_manager = u_manager
        self.account_manager = acc_manager
        self.general_utils = GeneralUtils()
        self.show_detailed_user_info = UserDisplayManager().show_detailed_user_info

    @staticmethod
    def visual():
        print("-------------------------------------------------------------------------------------------------------")

    @staticmethod
    def generate_menu_dict(*list_menu_options):
        menu_dict = {}
        for index, option in enumerate(list_menu_options, start=1):
            menu_dict[index] = option
        return menu_dict

    @staticmethod
    def print_subcategory_menu(lst):
        for i, elem in enumerate(lst, start=1):
            print(f"{i}.{elem}")

    # def menu_loop(self, input_var, end, dictionary, menu_name=None):
    #     if 0 == input_var or input_var > end:
    #         print("Ви ввели неправильне значення. Спробуйте ще раз")
    #         menu_name()
    #         self.visual()
    #     elif input_var <= end:
    #         func = dictionary.get(input_var)
    #         self.visual()
    #         if func.__name__ == 'main_menu':
    #             func(self.category_manager, self.user_manager, self.account_manager)
    #         else:
    #             func()
    #
    # # checks for a data type and sends to the menu_loop function
    # def menu_universal(self, menu_dict, menu_name):
    #     menu_item_count = len(menu_dict)
    #     try:
    #         choice = int(input("Оберіть потрібний пункт: "))
    #         self.menu_loop(choice, menu_item_count, menu_dict, menu_name)
    #     except ValueError:
    #         print("\nВи ввели неправильне значення. Спробуйте ще раз.\n")

    def create_menu(self, lst_of_functions, list_of_menu_options):
        menu_dict = self.generate_menu_dict(*lst_of_functions)
        user_update_menu = ['display_user_data_update_menu', 'update_user_data', 'display_user_type_update_menu']

        while True:
            self.print_subcategory_menu(list_of_menu_options)
            try:
                choice = int(input("Оберіть потрібний пункт: "))
                if 1 <= choice <= len(menu_dict):
                    self.visual()
                    func = menu_dict.get(choice)
                    if callable(func):
                        if func.__name__ == 'main_menu':
                            func(self.category_manager, self.user_manager,
                                 self.account_manager)
                        elif func.__name__ in user_update_menu:
                            func(self)

                        else:
                            func()

                    else:
                        self.create_menu(*func, self)
                else:
                    print("\nВи ввели неправильне значення. Спробуйте ще раз.\n")
            except ValueError:
                print("\nВи ввели неправильне значення. Спробуйте ще раз.\n")

    def var_updating(self, category_manager_menu_func, user_manager_menu_func, account_manager_menu_func):
        if self.category_manager is None:
            self.category_manager = category_manager_menu_func
            self.user_manager = user_manager_menu_func
            self.account_manager = account_manager_menu_func
        else:
            pass

    def main_menu(self, category_manager_menu_func, user_manager_menu_func, account_manager_menu_func):
        self.var_updating(category_manager_menu_func, user_manager_menu_func, account_manager_menu_func)
        list_of_methods = (
            lambda: category_manager_menu_func(self),
            lambda: user_manager_menu_func(self),
            lambda: account_manager_menu_func(self),
            self.the_end
        )

        self.create_menu(list_of_methods, self.main_menu_options)

    @staticmethod
    def the_end():
        quit()

    # def menu_loop(self, end, dictionary, menu_name=None):
    #     while True:
    #         try:
    #             choice = int(input("Оберіть потрібний пункт: "))
    #             if choice > end or choice < 1:
    #                 raise ValueError("Неправильне значення")
    #             func = dictionary.get(choice)
    #             self.visual()
    #             func()
    #         except ValueError:
    #             print("Ви ввели неправильне значення. Спробуйте ще раз.\n")
    #
    # # Обработка ввода пользователя и вызов соответствующей функции
    # def menu_universal(self, menu_dict, menu_name):
    #     menu_item_count = len(menu_dict)
    #     self.menu_loop(menu_item_count, menu_dict, menu_name)

class MenuManager:

    def __init__(self, cat_manager, u_manager, acc_manager):
        self.main_menu_options = ["Управління категоріями витрат та доходів", "Управління рахунками",
                                  "Управління витратами та доходами", "Вихід"]

        self.category_manager = cat_manager
        self.user_manager = u_manager
        self.account_manager = acc_manager

    # functional cycle of the menu, responsible for the operation and calling functions selected by the user
    def return_to_menu(self):
        self.main_menu()

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

    def menu_loop(self, input_var, end, dictionary, menu_name=None):
        if input_var > end:
            print("Ви ввели неправильне значення. Спробуйте ще раз")
            menu_name()
            self.visual()
        elif input_var <= end:
            func = dictionary.get(input_var)
            self.visual()
            func()

    # checks for a data type and sends to the menu_loop function
    def menu_universal(self, menu_dict, menu_name):
        menu_item_count = len(menu_dict)
        try:
            choice = int(input("Оберіть потрібний пункт: "))
            self.menu_loop(choice, menu_item_count, menu_dict, menu_name)
        except ValueError:
            print("\nВи ввели неправильне значення. Спробуйте ще раз.\n")

    def create_menu(self, lst_of_functions, list_of_menu_options, menu_name):
        menu_dict = self.generate_menu_dict(*lst_of_functions)

        while True:
            self.print_subcategory_menu(list_of_menu_options)
            self.menu_universal(menu_dict, menu_name)

    def main_menu(self):
        list_of_methods = (self.category_manager().category_manager_menu,
                           self.user_manager().user_manager_menu,
                           self.account_manager().account_manager_menu,
                           self.the_end)

        self.create_menu(list_of_methods, self.main_menu_options, self.main_menu)

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

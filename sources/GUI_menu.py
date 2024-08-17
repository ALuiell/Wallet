from tkinter import *
from tkinter import ttk


class MenuManager:

    def __init__(self, cat_manager, u_manager, acc_manager):
        self.main_menu_options_name = ["Управління категоріями витрат та доходів", "Управління рахунками",
                                       "Управління витратами та доходами", "Вихід"]

        self.category_manager = cat_manager
        self.user_manager = u_manager
        self.account_manager = acc_manager
        self.interface = Tk()
        self.interface.title("Wallet")

    def generate_menu_dict(self, methods_name, list_menu_options):
        my_dict_generator = ((name, option) for name, option in zip(methods_name, list_menu_options))
        return dict(my_dict_generator)

    def display_menu(self, dict_menu_options):
        for name, method in dict_menu_options.items():
            print(f"Створюємо кнопку: {name}")  # Додано для діагностики
            button = Button(self.interface, text=name, command=lambda m=method: m())
            button.pack()

    def create_menu(self, methods_name, list_menu_options):
        dict_menu_options = self.generate_menu_dict(methods_name, list_menu_options)
        self.display_menu(dict_menu_options)

    def main_menu(self):
        list_of_methods = (self.category_manager().category_manager_menu,
                           self.user_manager().user_manager_menu,
                           self.account_manager().account_manager_menu,
                           self.the_end)
        dict_menu_options = self.generate_menu_dict(self.main_menu_options_name, list_of_methods)
        self.display_menu(dict_menu_options)

    def start(self):
        self.interface.mainloop()

    def the_end(self):
        self.interface.quit()

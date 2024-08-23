from GUI_menu import MenuManager


class Jopa:
    def __init__(self, CategoryManager, UserManager, AccountManager):
        self.interface = MenuManager(CategoryManager, UserManager, AccountManager)
        self.interface.main_menu()  #
        self.interface.start()


class CategoryManager:
    def category_manager_menu(self):
        print("Категорії")


class UserManager:
    def user_manager_menu(self):
        print("Користувачі")


class AccountManager:
    def account_manager_menu(self):
        print("Рахунки")


a = Jopa(CategoryManager, UserManager, AccountManager)

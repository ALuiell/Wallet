from menu import MenuManager
from category_manager import CategoryManager
from core.account_manager import AccountManager
from core.user_manager import UserManager

if __name__ == '__main__':
    category_manager = CategoryManager()
    user_manager = UserManager()
    account_manager = AccountManager()
    menu_manager = MenuManager()
    menu_manager.main_menu(
        category_manager.category_manager_menu,
        user_manager.user_manager_menu,
        account_manager.account_manager_menu
    )

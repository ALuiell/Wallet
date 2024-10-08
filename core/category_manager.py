from core.db_config import db_manager
from core.models import Category
from core.general_utils import GeneralUtils
import re


class CategoryDataStore:
    def __init__(self):
        self.menu_categories = ["Додати категорію", "Видалити категорію", "Змінити дані про категорію",
                                "Перегляд списку категорій", "Назад"]


class CategoryDisplayManager:
    def __init__(self):
        self.general_utils = GeneralUtils()

    def show_categories_inline(self):
        self.general_utils.show_list_categories(inline=True)

    def show_categories_multiline(self):
        self.general_utils.show_list_categories()


class CategoryValidationManager:

    @staticmethod
    def validate_category_name(category_name):
        pattern = r'^[a-zA-Zа-яА-ЯєЄїЇіІґҐ\'\s]+$'
        return bool(re.match(pattern, category_name))

    @staticmethod
    def category_name_exists(name: str) -> bool:
        return db_manager.verify(Category, "Name", name)


class CategoryManagerUtils:
    def __init__(self):
        self.validator = CategoryValidationManager()

    def input_name(self) -> str:
        name = input("Введіть назву категорії: ").strip()
        if self.validator.category_name_exists(name):
            return name


class CategoryManager:
    def __init__(self):
        self.general_utils = GeneralUtils()
        self.data_store = CategoryDataStore()
        self.display_manager = CategoryDisplayManager()
        self.validation_manager = CategoryValidationManager()

    def create_new_category(self):
        print("Існуючі категорії:")
        self.display_manager.show_categories_multiline()
        while True:
            name = input("Введіть назву нової категорії: ").strip()
            if self.validation_manager.validate_category_name(name):
                if not self.validation_manager.category_name_exists(name):
                    self.add_category_to_db(name)
                    self.general_utils.update_global_lists()
                    return
                else:
                    print("Категорія з такою назвою вже існує")
            else:
                print("Неправильний формат назви категорії. Використовуйте лише букви.")

    @staticmethod
    def add_category_to_db(name: str):
        db_manager.create(Category, {"Name": name})
        print(f"Категорія {name} додана")

    def update_category(self):
        self.display_manager.show_categories_multiline()
        name = input("Введіть назву категорії, яку потрібно змінити: ").strip()
        if self.validation_manager.category_name_exists(name):
            print(f"Категорія з назвою {name} знайдена.")
            while True:
                new_name = input("Введіть нову назву: ")
                if not self.validation_manager.category_name_exists(new_name):
                    self.update_name_category_in_db(name, new_name)
                    self.general_utils.update_global_lists()
                    break
                else:
                    print(f"Категорія з назвою {new_name} вже існує. Будь ласка, введіть інше ім'я.")

        else:
            print(f"Категорія з назвою {name} не знайдена")

    @staticmethod
    def update_name_category_in_db(name: str, new_name: str):
        db_manager.update(Category, "Name", new_name, "Name", name)
        print(f"Назва категорії {name} змінена на {new_name}")

    def remove_category(self):
        self.display_manager.show_categories_multiline()
        while True:
            name = input("Введіть назву категорії: ").strip()
            if self.validation_manager.validate_category_name(name):
                if self.validation_manager.category_name_exists(name):
                    self.delete_category_from_db(name)
                    self.general_utils.update_global_lists()
                    return
                else:
                    print(f"Категорію з назвою {name} не знайдено")
            else:
                print("Неправильний формат назви категорії. Використовуйте лише букви.")

    @staticmethod
    def delete_category_from_db(name: str):
        db_manager.delete(Category, "Name", name)
        print(f"Категорія {name} видалена")

    def category_manager_menu(self, menu_manager):
        list_of_methods = (self.create_new_category,
                           self.remove_category,
                           self.update_category,
                           self.general_utils.show_list_categories,
                           menu_manager.main_menu)

        menu_manager.create_menu(list_of_methods, self.data_store.menu_categories)

import unittest
from unittest.mock import patch
from core.models import UserAccounts
from core import database_manager_ORM
from core.user_manager import UserManager
import peewee

db_path = "/db\\wallet_test.db"
db_manager = database_manager_ORM.DatabaseManager(db_path)

name_for_create = "Новий Тестовий Користувач"
name_for_update = "Змінений Тестовий Користувач"


class TestUserAccountMethods(unittest.TestCase):
    def setUp(self):
        self.user = UserManager()
        with patch('builtins.input', side_effect=[name_for_update, '1']):
            self.user.create_user_account()

    def test_create_user_account_correct_data(self):
        name = "Тестовий Новий Користувач"
        with patch('builtins.input', side_effect=[name, '1']):
            self.user.create_user_account()
        self.assertTrue(UserAccounts.select().where(UserAccounts.Name == name).exists())
        user_object = UserAccounts.get(Name=name)
        user_object.delete_instance()

    def test_change_user_account_name(self):
        user_object = UserAccounts.get(Name=name_for_update)
        with patch('builtins.input', side_effect=[name_for_update]):
            self.user.update_user_name(user_object.Number)
            self.assertTrue(UserAccounts.select().where(UserAccounts.Name == name_for_update).exists())

    def test_change_user_account_type(self):
        user_object = UserAccounts.get(Name=name_for_update)
        with patch('builtins.input', side_effect=["2", "1000"]):
            try:
                self.user.display_user_type_update_menu(user_object.Number)
            except StopIteration:
                pass  # Игнорируем исключение, так как оно указывает на успешный выход из цикла
        user_object = UserAccounts.get(Name=name_for_update)
        self.assertTrue(user_object.Type != "Дебетовий")

    def test_delete_user(self):
        user_object = UserAccounts.get(Name=name_for_update)
        with patch('builtins.input', side_effect=[user_object.Number]):
            self.user.remove_user_account()
            self.assertFalse(UserAccounts.select().where(UserAccounts.Name == name_for_update).exists())

    def tearDown(self):
        try:
            user_object = UserAccounts.get(Name=name_for_update)
            user_object.delete_instance()
        except peewee.DoesNotExist:
            pass


if __name__ == '__main__':
    unittest.main()

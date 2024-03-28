import unittest
from unittest.mock import patch
from sources.models import User_Accounts
from sources import database_manager_ORM
from sources.Wallet_DB import CategoryTwo
import peewee

db_path = "F:\\Python\\Wallet\\DB\\wallet_test.db"
db_manager = database_manager_ORM.DatabaseManager(db_path)

name_for_create = "Новий Тестовий Користувач"
name_for_update = "Змінений Тестовий Користувач"


class TestUserAccountMethods(unittest.TestCase):
    def setUp(self):
        self.category = CategoryTwo()
        with patch('builtins.input', side_effect=[name_for_update, '1']):
            self.category.create_user_account()

    def test_create_user_account_correct_data(self):
        name = "Тестовий Новий Користувач"
        with patch('builtins.input', side_effect=[name, '1']):
            self.category.create_user_account()
        self.assertTrue(User_Accounts.select().where(User_Accounts.Name == name).exists())
        user_object = User_Accounts.get(Name=name)
        user_object.delete_instance()

    def test_change_user_account_name(self):
        user_object = User_Accounts.get(Name=name_for_update)
        with patch('builtins.input', side_effect=[name_for_update]):
            self.category.update_user_name(user_object.Number)
            self.assertTrue(User_Accounts.select().where(User_Accounts.Name == name_for_update).exists())

    def test_change_user_account_type(self):
        user_object = User_Accounts.get(Name=name_for_update)
        with patch('builtins.input', side_effect=["2"]):
            self.category.display_user_type_update_menu(user_object.Number)
            user_object = User_Accounts.get(Name=name_for_update)
            self.assertTrue(user_object.Type != "Дебетовий")

    def test_delete_user(self):
        user_object = User_Accounts.get(Name=name_for_update)
        with patch('builtins.input', side_effect=[user_object.Number]):
            self.category.remove_user_account()
            self.assertFalse(User_Accounts.select().where(User_Accounts.Name == name_for_update).exists())

    def tearDown(self):
        try:
            user_object = User_Accounts.get(Name=name_for_update)
            user_object.delete_instance()
        except peewee.DoesNotExist:
            pass


if __name__ == '__main__':
    unittest.main()

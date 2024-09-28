import unittest
from unittest.mock import patch
from core.models import UserAccounts
from core.db_config import db_manager
from core.user_manager import UserManager


class TestUserManager(unittest.TestCase):
    test_account_number = None

    def setUp(self):
        self.user = UserManager()
        self.name_for_create = "Новий Тестовий Користувач"
        self.name_for_update = "Змінений Тестовий Користувач"

    def create_test_account(self, type_option='1'):
        # type_option='1' debit type, type_option='2' credit type,

        with patch('builtins.input', side_effect=[self.name_for_create, type_option]):
            self.user.create_user_account(test=True)
            TestUserManager.test_account_number = self.user.test_account_number

    def test_create_user_account(self):
        self.create_test_account()
        self.assertTrue(db_manager.verify(UserAccounts, 'Number', TestUserManager.test_account_number))
        db_manager.delete(UserAccounts, 'Number', TestUserManager.test_account_number)
        self.assertFalse(db_manager.verify(UserAccounts, 'Number', TestUserManager.test_account_number))

    def test_change_user_account_name(self):
        self.create_test_account()
        with patch('builtins.input', side_effect=[self.name_for_update]):
            self.user.update_user_name(test_account_number=TestUserManager.test_account_number)
            self.assertTrue(db_manager.verify2(UserAccounts,
                                               [('Number', TestUserManager.test_account_number),
                                                ('Name', self.name_for_update)]))
        db_manager.delete(UserAccounts, 'Number', TestUserManager.test_account_number)
        self.assertFalse(db_manager.verify(UserAccounts, 'Number', TestUserManager.test_account_number))

    def test_change_user_account_type_on_debit(self):
        self.create_test_account(type_option='2')
        self.user.update_user_type_on_debit(test_account_number=TestUserManager.test_account_number)
        self.assertTrue(db_manager.verify2(UserAccounts,
                                           [('Number', TestUserManager.test_account_number),
                                            ('Type', 'Дебетовий')]))
        db_manager.delete(UserAccounts, 'Number', TestUserManager.test_account_number)
        self.assertFalse(db_manager.verify(UserAccounts, 'Number', TestUserManager.test_account_number))

    def test_change_user_account_type_on_credit(self):
        self.create_test_account()
        self.user.update_user_type_on_credit(test_account_number=TestUserManager.test_account_number)
        self.assertTrue(db_manager.verify2(UserAccounts,
                                           [('Number', TestUserManager.test_account_number),
                                            ('Type', 'Кредитний')]))
        db_manager.delete(UserAccounts, 'Number', TestUserManager.test_account_number)
        self.assertFalse(db_manager.verify(UserAccounts, 'Number', TestUserManager.test_account_number))

    def test_delete_user(self):
        self.create_test_account()
        with patch('builtins.input', side_effect=[TestUserManager.test_account_number]):
            self.user.remove_user_account()
        self.assertFalse(db_manager.verify(UserAccounts, 'Number', TestUserManager.test_account_number))


if __name__ == '__main__':
    unittest.main()

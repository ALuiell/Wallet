import unittest
from unittest.mock import patch
from core.models import UserAccounts
from core.models import TransactionAll
from core.db_config import db_manager
from core.account_manager import AccountManager
from core.user_manager import UserManager


# @classmethod
# def create_test_accounts(cls):
#     data = {"Number": "12345678",
#             "Type": "Дебетовий",
#             "Name": "Тестовий Новий Користувач",
#             "Balance": 0}
#
#     data2 = {"Number": "23456789",
#              "Type": "Дебетовий",
#              "Name": "Тестовий Новий Користувач2",
#              "Balance": 0}
#     # create first test user
#     TestAccountManager.test_account_number = data['Number']
#     db_manager.create(UserAccounts, data)
#     # create second test user
#     TestAccountManager.test_account_number2 = data2['Number']
#     db_manager.create(UserAccounts, data2)

class TestAccountManager(unittest.TestCase):
    test_account_number = None
    test_account_number2 = None
    test_transaction_id = None
    test_transaction_id2 = None

    # def create_test_accounts(cls):
    #     data = {"Number": "12345678",
    #             "Type": "Дебетовий",
    #             "Name": "Тестовий Новий Користувач",
    #             "Balance": 0}
    #
    #     data2 = {"Number": "23456789",
    #              "Type": "Дебетовий",
    #              "Name": "Тестовий Новий Користувач2",
    #              "Balance": 0}
    #     # create first test user
    #     TestAccountManager.test_account_number = data['Number']
    #     db_manager.create(UserAccounts, data)
    #     # create second test user
    #     TestAccountManager.test_account_number2 = data2['Number']
    #     db_manager.create(UserAccounts, data2)

    @classmethod
    def create_test_accounts(cls):
        with patch('builtins.input', side_effect=['Перший Тестовий Користувач', '1']):
            cls.user_manager.create_user_account(test=True)
            cls.test_account_number = cls.user_manager.test_account_number  # сохраняем номер счета

        with patch('builtins.input', side_effect=['Другий Тестовий Користувач', '1']):
            cls.user_manager.create_user_account(test=True)
            cls.test_account_number2 = cls.user_manager.test_account_number  # сохраняем номер счета

    @classmethod
    def setUpClass(cls):
        cls.user_manager = UserManager()
        cls.create_test_accounts()

    def setUp(self):
        self.account_manager = AccountManager()

    def test_create_transaction_on_account(self):
        # number, category_name, +-amount
        with patch('builtins.input', side_effect=[TestAccountManager.test_account_number, "Тест", "+100"]):
            self.account_manager.add_transaction(test=True)
            TestAccountManager.test_transaction_id = self.account_manager.test_transaction_id
            self.assertTrue(db_manager.verify(TransactionAll, "TransactionID", TestAccountManager.test_transaction_id))
            self.assertTrue(db_manager.verify2(UserAccounts, [('Number', TestAccountManager.test_account_number),
                                                              ("Balance", '100')]))
            db_manager.update(UserAccounts, 'Balance', 0, 'Number', TestAccountManager.test_account_number)
            db_manager.delete(TransactionAll, 'TransactionID', TestAccountManager.test_transaction_id)
            self.assertFalse(db_manager.verify(TransactionAll, "TransactionID", TestAccountManager.test_transaction_id))
            self.assertTrue(db_manager.verify2(UserAccounts, [('Number', TestAccountManager.test_account_number),
                                                              ("Balance", '0')]))

    def test_remove_transaction_on_account(self):
        with patch('builtins.input', side_effect=[TestAccountManager.test_account_number, "Тест", "+100"]):
            self.account_manager.add_transaction(test=True)
            TestAccountManager.test_transaction_id = self.account_manager.test_transaction_id
            self.assertTrue(db_manager.verify(TransactionAll, "TransactionID", TestAccountManager.test_transaction_id))
        with patch('builtins.input', side_effect=[TestAccountManager.test_account_number,
                                                  TestAccountManager.test_transaction_id]):
            self.account_manager.delete_transaction()
            self.assertFalse(db_manager.verify(TransactionAll, "TransactionID", TestAccountManager.test_transaction_id))

    def test_create_transfer_transaction_on_account(self):
        # create transaction for update money amount on balance
        with patch('builtins.input', side_effect=[TestAccountManager.test_account_number, "Тест", "+100"]):
            self.account_manager.add_transaction(test=True)
            TestAccountManager.test_transaction_id = self.account_manager.test_transaction_id
            self.assertTrue(db_manager.verify(TransactionAll, "TransactionID", TestAccountManager.test_transaction_id))
            self.assertTrue(db_manager.verify2(UserAccounts, [('Number', TestAccountManager.test_account_number),
                                                              ("Balance", '100')]))

        # make transfer
        with patch('builtins.input', side_effect=[TestAccountManager.test_account_number,
                                                  TestAccountManager.test_account_number2, '20']):
            self.account_manager.transaction_transfer()
            TestAccountManager.test_transaction_id2 = self.account_manager.test_transaction_id
            self.assertTrue(db_manager.verify(TransactionAll, "TransactionID", TestAccountManager.test_transaction_id))
            self.assertTrue(db_manager.verify2(UserAccounts, [('Number', TestAccountManager.test_account_number),
                                                              ("Balance", '80')]))

            self.assertTrue(db_manager.verify2(UserAccounts, [('Number', TestAccountManager.test_account_number2),
                                                              ("Balance", '20')]))

        # delete transfer transaction
        with patch('builtins.input', side_effect=[TestAccountManager.test_account_number,
                                                  TestAccountManager.test_transaction_id]):
            self.account_manager.delete_transaction()
            self.assertFalse(db_manager.verify(TransactionAll,
                                               "TransactionID",
                                               TestAccountManager.test_transaction_id))
        # delete transaction
        with patch('builtins.input', side_effect=[TestAccountManager.test_account_number,
                                                  TestAccountManager.test_transaction_id2]):
            self.account_manager.delete_transaction()
            self.assertFalse(db_manager.verify(TransactionAll,
                                               "TransactionID",
                                               TestAccountManager.test_transaction_id2))

    @classmethod
    def tearDownClass(cls):
        with patch('builtins.input', side_effect=[TestAccountManager.test_account_number]):
            UserManager().remove_user_account()
        with patch('builtins.input', side_effect=[TestAccountManager.test_account_number2]):
            UserManager().remove_user_account()


if __name__ == '__main__':
    unittest.main()

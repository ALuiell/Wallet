import unittest
from unittest.mock import patch
from core.models import UserAccounts
from core.models import TransactionAll
from core.db_config import db_manager
from core.account_manager import AccountManager
from core.user_manager import UserManager


class TestAccountManager(unittest.TestCase):
    test_account_number = '12345678'
    test_account_number2 = '23456789'
    test_transaction_id = 'TRX123456'
    test_transaction_id2 = 'TRX234567'

    @classmethod
    def create_test_accounts(cls):
        with patch('builtins.input', side_effect=['Перший Тестовий Користувач', '1']):
            cls.user_manager.create_user_account(cls.test_account_number)

        with patch('builtins.input', side_effect=['Другий Тестовий Користувач', '1']):
            cls.user_manager.create_user_account(cls.test_account_number2)

    @classmethod
    def setUpClass(cls):
        cls.user_manager = UserManager()
        cls.create_test_accounts()

    def setUp(self):
        self.account_manager = AccountManager()

    def test_create_transaction_on_account(self):
        # number, category_name, +-amount
        with patch('builtins.input', side_effect=[self.test_account_number, "Тест", "+100"]):
            self.account_manager.add_transaction(account_number=self.test_account_number,
                                                 transaction_id=self.test_transaction_id)

            self.assertTrue(db_manager.verify(TransactionAll, "TransactionID", self.test_transaction_id))
            self.assertTrue(db_manager.verify2(UserAccounts, [('Number', self.test_account_number),
                                                              ("Balance", '100')]))
            db_manager.update(UserAccounts, 'Balance', 0, 'Number', self.test_account_number)
            db_manager.delete(TransactionAll, 'TransactionID', self.test_transaction_id)
            self.assertFalse(db_manager.verify(TransactionAll, "TransactionID", self.test_transaction_id))
            self.assertTrue(db_manager.verify2(UserAccounts, [('Number', self.test_account_number),
                                                              ("Balance", '0')]))

    def test_remove_transaction_on_account(self):
        with patch('builtins.input', side_effect=[self.test_account_number, "Тест", "+100"]):
            self.account_manager.add_transaction(account_number=self.test_account_number,
                                                 transaction_id=self.test_transaction_id)
            self.assertTrue(db_manager.verify(TransactionAll, "TransactionID", self.test_transaction_id))
        with patch('builtins.input', side_effect=[self.test_account_number,
                                                  self.test_transaction_id]):
            self.account_manager.delete_transaction()
            self.assertFalse(db_manager.verify(TransactionAll, "TransactionID", self.test_transaction_id))

    def test_create_transfer_transaction_on_account(self):
        # create transaction for update money amount on balance
        with patch('builtins.input', side_effect=[self.test_account_number, "Тест", "+100"]):
            self.account_manager.add_transaction(account_number=self.test_account_number,
                                                 transaction_id=self.test_transaction_id)

            self.assertTrue(db_manager.verify(TransactionAll, "TransactionID", self.test_transaction_id))
            self.assertTrue(db_manager.verify2(UserAccounts, [('Number', self.test_account_number),
                                                              ("Balance", '100')]))

        # make transfer
        with patch('builtins.input', side_effect=[self.test_account_number,
                                                  self.test_account_number2, '20']):
            self.account_manager.transaction_transfer(transaction_id=self.test_transaction_id2)
            self.assertTrue(db_manager.verify(TransactionAll, "TransactionID", self.test_transaction_id2))
            self.assertTrue(db_manager.verify2(UserAccounts, [('Number', self.test_account_number),
                                                              ("Balance", '80')]))

            self.assertTrue(db_manager.verify2(UserAccounts, [('Number', self.test_account_number2),
                                                              ("Balance", '20')]))

        # delete transfer transaction
        with patch('builtins.input', side_effect=[self.test_account_number,
                                                  self.test_transaction_id]):
            self.account_manager.delete_transaction()
            self.assertFalse(db_manager.verify(TransactionAll,
                                               "TransactionID",
                                               self.test_transaction_id))
        # delete transaction
        with patch('builtins.input', side_effect=[self.test_account_number,
                                                  self.test_transaction_id2]):
            self.account_manager.delete_transaction()
            self.assertFalse(db_manager.verify(TransactionAll,
                                               "TransactionID",
                                               self.test_transaction_id2))

    @classmethod
    def tearDownClass(cls):
        with patch('builtins.input', side_effect=[cls.test_account_number]):
            UserManager().remove_user_account()
        with patch('builtins.input', side_effect=[cls.test_account_number2]):
            UserManager().remove_user_account()


if __name__ == '__main__':
    unittest.main()

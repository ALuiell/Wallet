import unittest
import category_manager_test
import user_manager_test
import account_manager_test


class Test(unittest.TestCase):
    def test_all(self):
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        suite.addTest(loader.loadTestsFromTestCase(category_manager_test.TestCategoryManager))
        suite.addTest(loader.loadTestsFromTestCase(user_manager_test.TestUserManager))
        suite.addTest(loader.loadTestsFromTestCase(account_manager_test.TestAccountManager))
        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == '__main__':
    unittest.main()

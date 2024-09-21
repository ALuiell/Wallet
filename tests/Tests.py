import unittest
import category_manager
import user_manager


class Test(unittest.TestCase):
    def test_all(self):
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        suite.addTest(loader.loadTestsFromTestCase(category_manager.TestCategoryMethods))
        suite.addTest(loader.loadTestsFromTestCase(user_manager.TestUserAccountMethods))
        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == '__main__':
    unittest.main()

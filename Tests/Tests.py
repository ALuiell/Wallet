import unittest
import test_cat1
import test_cat2


class Test(unittest.TestCase):
    def test_all(self):
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        suite.addTest(loader.loadTestsFromTestCase(test_cat1.TestCategoryMethods))
        suite.addTest(loader.loadTestsFromTestCase(test_cat2.TestUserAccountMethods))
        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == '__main__':
    unittest.main()

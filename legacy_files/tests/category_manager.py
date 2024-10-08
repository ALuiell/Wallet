import unittest
from unittest.mock import patch

from core.models import Category
from core import database_manager_ORM
from legacy_files.wallet_ver3 import CategoryManager

db_path = "/db\\wallet_test.db"
db_manager = database_manager_ORM.DatabaseManager(db_path)


class TestCategoryMethods(unittest.TestCase):

    def setUp(self):
        self.category_name = "TestCategory"
        self.new_category_name = "UPCategory"
        self.category = CategoryManager()

    @patch('builtins.input', side_effect=["TestCategory"])
    def test_create_new_category(self, mock_input):
        self.category.create_new_category()
        self.assertTrue(Category.select().where(Category.Name == self.category_name).exists())

        # create existing category
        self.category.create_new_category()
        self.assertTrue(Category.select().where(Category.Name == self.category_name).exists())

    def test_remove_category(self):
        db_manager.create(Category, {"Name": self.category_name})
        self.assertTrue(Category.select().where(Category.Name == self.category_name).exists())
        with patch('builtins.input', return_value=self.category_name):
            self.category.remove_category()
        self.assertFalse(Category.select().where(Category.Name == self.category_name).exists())

    def test_update_category(self):
        db_manager.create(Category, {"Name": self.category_name})
        self.assertTrue(Category.select().where(Category.Name == self.category_name).exists())

        with patch('builtins.input', side_effect=[self.category_name, self.new_category_name]):
            self.category.update_category()

        self.assertTrue(Category.select().where(Category.Name == self.new_category_name).exists())

    def tearDown(self):
        db_manager.delete(Category, "Name", self.category_name)
        db_manager.delete(Category, "Name", self.new_category_name)


if __name__ == '__main__':
    unittest.main()

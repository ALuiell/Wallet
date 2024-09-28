import unittest
from unittest.mock import patch
from core.models import Category
from core.category_manager import CategoryManager
from core.db_config import db_manager


class TestCategoryManager(unittest.TestCase):

    def setUp(self):
        self.category_name = "TestCategory"
        self.new_category_name = "UPCategory"
        self.category = CategoryManager()

    @patch('builtins.input', side_effect=["TestCategory"])
    def test_create_new_category(self, mock_input):
        self.category.create_new_category()
        self.assertTrue(Category.select().where(Category.Name == self.category_name).exists())

    def test_update_category(self):
        db_manager.create(Category, {"Name": self.category_name})
        self.assertTrue(Category.select().where(Category.Name == self.category_name).exists())

        with patch('builtins.input', side_effect=[self.category_name, self.new_category_name]):
            self.category.update_category()

        self.assertTrue(Category.select().where(Category.Name == self.new_category_name).exists())

    def test_remove_category(self):
        db_manager.create(Category, {"Name": self.category_name})
        self.assertTrue(Category.select().where(Category.Name == self.category_name).exists())

        # Используем side_effect, чтобы input возвращал правильное имя категории с первого раза
        with patch('builtins.input', return_value=self.category_name):
            self.category.remove_category()

        self.assertFalse(Category.select().where(Category.Name == self.category_name).exists())

    def tearDown(self):
        db_manager.delete(Category, "Name", self.category_name)
        db_manager.delete(Category, "Name", self.new_category_name)


if __name__ == '__main__':
    unittest.main()

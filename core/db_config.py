import os
from core.database_manager_ORM import DatabaseManager


db_path = os.path.join("db", "wallet_test.db")
db_manager = DatabaseManager(db_path)

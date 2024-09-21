import os
from models import *
from core import database_manager_ORM

db_path = os.path.join("db", "wallet_test.db")
db_manager = database_manager_ORM.DatabaseManager(db_path)

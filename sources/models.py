from peewee import Model, SqliteDatabase, CharField, FloatField, TextField, ForeignKeyField, DateTimeField

db = SqliteDatabase("F:\\Python\\Wallet\\DB\\wallet_test.db")


class BaseModel(Model):
    class Meta:
        database = db


class Category(BaseModel):
    Name = TextField(unique=True)

    class Meta:
        table_name = "Category"


class User_Accounts(BaseModel):
    Number = CharField(unique=True, max_length=8)
    Type = TextField()
    Name = TextField()
    Balance = FloatField()

    class Meta:
        table_name = "User_Accounts"


class TransactionAll(BaseModel):
    Number = ForeignKeyField(User_Accounts, backref='transactions')
    Type = TextField()
    Category = ForeignKeyField(Category, backref='transactions')
    Date = DateTimeField()
    TransactionID = CharField(max_length=10)
    Amount = FloatField()

    class Meta:
        table_name = "TransactionAll"

# list of info about accounts | DB+
# полностью перенести в db и выпилить
user_accounts = {
    "12345678": {"type": "Дебетовий", "name": "John Smith", "transactions": [], "balance": 0.0},
    "87654321": {"type": "Кредитний", "name": "Jane Doe", "transactions": [], "balance": 0.0},
    "65432198": {"type": "Дебетовий", "name": "Michael Johnson", "transactions": [], "balance": 0.0}}

# EXAMPLE "12345678": {"type": "Дебетовий", "name": "John Smith", "transactions": [], "balance": 0.0}
#                                       Structure of transactions
# "transactions": [{"transaction_id": trans_id, "date": date, "category": category, "transaction": transaction}]
#                    transaction_id : TRX237516 | date: 01.10.2023 | category: "Одяг" | transaction: +100\-100

# --------------------------------------------------------------------------------------------------------------------

# наполнять из базы данных
# lst number accounts for verification, ONLY numbers
lst_accounts = ["12345678", "87654321", "65432198"]
# --------------------------------------------------------------------------------------------------------------------

# lst name categories for verification, ONLY THE NAMES IS ADDED
# оставить список и потом из базы данных наполнять список недостающими
user_categories = ["Їжа", "Одяг і взуття", "Розваги", "Транспорт", "Комунальні послуги", "Оплата житла",
                   "Здоров'я та медицина", "Подарунки та благодійність", "Краса та гігієна",
                   "Офісні витрати", "Домашні тварини", "Подорожі", "Освіта та розвиток", "Перекази"]
# -------------------------------------------------------------------------------------------------------------------
# полностью перенести в db и выпилить
# list of information about user_categories and transactions by these categories, ADDED NAMES WITH DICTIONARIES   |  DB+
user_categories1 = {}
#                                           STRUCTURE
# user_categories1  = {
# {'Їжа': {'65432198': {'05.10.2023': [{'transaction': '+100', 'transaction_id': 'TRX605817'}]}},
# 'Одяг і взуття': {},
# 'Розваги': {},
# 'Перекази': {}
# }

# --------------------------------------------------------------------------------------------------------------------
# в дб и выпилить
# list for the transfer transaction     |  DB+
lst_transfer = {}

#                                           STRUCTURE
# transfer_id = {"date": date1, "from_account": from_num1, "to_account": to_num2, "amount": amount}
# EXAMPLE
# {'TRX286495': {'date': '10.10.2023', 'from_account': '65432198', 'to_account': '12345678', 'amount': 50.0}}
"""
1. добавить невозможность вывода дебетового счета в минус
2. везде добавить обратно в меню
3. поставить более понятные проверки на ввод пользователя
4. 

"""

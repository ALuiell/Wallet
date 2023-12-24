import random
import re

'''testing categoryTwo'''
"""
                                                Database TABLE
User_accounts Table
Number: Unique account number (integer).
Type: Account type (text).
Name: Account holder's name (text).
Balance: Account balance (float).

TransactionAll Table
Number: Account number to which the transaction is associated (integer).
Type: Type of transaction (text).
Category: Transaction category (text).
TransactionDate: Transaction date (in the format "yyyy.mm.dd").
TransactionID: Unique transaction identifier (text).
Amount: Transaction amount (float).

Transaction_Transfer Table
From_number: Sender's account number (integer).
To_number: Receiver's account number (integer).
TransactionDate: Transaction date (in the format "yyyy.mm.dd").
TransactionID: Unique transaction identifier (text).
Amount: Transaction amount (float)."""

user_accounts = {
    "12345678": {"type": "debit", "name": "John Smith", "transactions": [], "balance": 0},
    "87654321": {"type": "credit", "name": "Jane Doe", "transactions": [], "balance": 0},
    "65432198": {"type": "debit", "name": "Michael Johnson", "transactions": [], "balance": 0}
}


def generate_account_number():
    digits = list(range(10))
    random.shuffle(digits)
    account_number = ''.join(map(str, digits[:8]))
    return account_number


def validate_account_num(account_num, lst_accounts):
    if account_num not in lst_accounts:
        lst_accounts.append(account_num)
    else:
        account_num = generate_account_number()
        lst_accounts.append(account_num)
    return account_num


def display_account_info(account_num):
    account_info = user_accounts.get(account_num)
    print("Номер Рахунку: {}\nПІБ: {}\nТип: {} \nБаланс: {}".format(
        account_num,
        account_info.get('name'),
        account_info.get('type'),
        account_info.get("balance")
    ))


def validate_name(name):
    pattern = r'^[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+\s+([-\']?[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+\s+)?[А-ЩЬЮЯЇІЄҐ][а-щьюяїієґ]+$'
    match = re.match(pattern, name)
    if match:
        return True
    else:
        print("ПІБ введено неправильно")
        return False


def input_name():
    while True:
        name = input("Введіть ПІБ: ")
        if validate_name(name):
            return name


def validate_type(acc_type):
    if acc_type == "1" or acc_type == "2":
        return True
    else:
        return False


def input_type():
    while True:
        account_type = input("Оберіть тип: \n1.Дебетовий \n2.Кредитний \nВведіть цифру 1 або 2: ")
        if validate_type(account_type):
            return account_type


def add_user_acc():
    lst_accounts = []
    account_num = generate_account_number()
    account_num = validate_account_num(account_num, lst_accounts)
    account_name = input_name()
    account_type = input_type()

    if account_type == "1":
        user_accounts[account_num] = {"type": "Дебетовий", "name": account_name, "transactions": [], "balance": 0}
        print('Рахунок створено')
        display_account_info(account_num)

    elif account_type == "2":
        user_accounts[account_num] = {"type": "Кредитний", "name": account_name, "transactions": [], "balance": 0}
        print('Рахунок створено')
        display_account_info(account_num)


def lst_user_acc():
    for i in user_accounts:
        display_account_info(i)
        print()


def update_menu(input_acc):
    def update_account_type():
        update_acc_type = ["1.Дебетовий", "2.Кредитний", "3.Назад"]
        print("{} \n{} \n{}".format(*update_acc_type))
        while True:
            what_type = input("Оберіть пункт: ")
            if what_type == "1":
                user_accounts[input_acc]["type"] = "Дебетовий"
                print("Тип рахунку змінено на Дебетовий \n")
                return

            elif what_type == "2":
                user_accounts[input_acc]["type"] = "Кредитний"
                print("Тип рахунку змінено на Кредитний \n")
                return

            elif what_type == "3":
                return

            else:
                print("Неправильний вибір, спробуйте ще раз.")
                update_account_type()

    def update_account_name():
        while True:
            new_name = input("Введіть новий ПІБ: ")
            if validate_name(new_name):
                user_accounts[input_acc]["name"] = new_name
                print("Інформацію оновлено")
                display_account_info(input_acc)
                update_menu(input_acc)
                return "back"

            else:
                print("Неправильне ім'я, спробуйте ще раз.")
                continue

    while True:
        update_menu_lst = ["Що бажаєте змінити?", "1.Тип", "2.ПІБ", "3.Повернутись в меню"]
        print("{} \n{} \n{} \n{}".format(*update_menu_lst))
        what_change = input("Введіть номер опції: ")
        if what_change == "1":
            update_account_type()

        elif what_change == "2":
            result1 = update_account_name()
            if result1 == "back":
                break

        elif what_change == "3":
            break

        else:
            print("Неправильний вибір, спробуйте ще раз.")
            update_menu(input_acc)


def update_user_acc():
    lst_user_acc()
    input_acc = input("Введіть номер рахунку: ")
    if input_acc in user_accounts:
        print("Рахунок знайдено\n")
        display_account_info(input_acc)
        print()
        update_menu(input_acc)
    else:
        print("Рахунок не знайдено, спробуйте ще раз")
        update_user_acc()


def remove_user_acc():
    lst_user_acc()
    num_acc = input("Введіть номер рахунку для видалення: ")
    if num_acc in user_accounts:
        print("Рахунок видалено \n")
        del user_accounts[num_acc]
    else:
        print("Рахунок не знайдено \n")
        remove_user_acc()


lst_user_acc()
remove_user_acc()
lst_user_acc()

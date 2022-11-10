"""Банкомат 3.0
- реалізуйте видачу купюр за логікою видавання найменшої кількості купюр, але в межах наявних в банкоматі.
Наприклад: 2560 --> 2х1000, 1х500, 3х20. Будьте обережні з "жадібним алгоритмом"! Видані купюри також мають бути
“вилучені” з банкомату. Тобто якщо до операції в банкоматі було 5х1000, 5х500, 5х20 - має стати 3х1000, 4х500, 2х20.
- як і раніше, поповнення балансу користувача не впливає на кількість купюр. Їх кількість може змінювати лише інкасатор.
- обов’язкова реалізація таких дій (назви можете використовувати свої):
При запускі
- Вхід
- Реєстрація (з перевіркою валідності/складності введених даних)
- Вихід
Для користувача
- Баланс
- Поповнення
- Зняття
- Історія транзакцій
- Вихід на стартове меню
Для інкасатора
- Наявні купюри/баланс тощо
- Зміна кількості купюр
- Повна історія операцій по банкомату (дії всіх користувачів та інкасаторів)
- Вихід на стартове меню
- обов’язкове дотримання РЕР8 (якщо самостійно ніяк, то https://flake8.pycqa.org/en/latest/ вам в допомогу)
- (опціонально) не лініться і придумайте якусь свою особливу фішку/додатковий функціонал, але за умови що основне
завдання виконане"""


import sqlite3
import tabulate
import datetime
from prettytable import PrettyTable
import pygame
import sys
import time


conn = sqlite3.connect('atm.db')
cursor = conn.cursor()
conn.execute('''CREATE TABLE IF NOT EXISTS ACCOUNTS
                (USERNAME TEXT PRIMARY KEY NOT NULL,
                PASSWORD TEXT NOT NULL,
                BALANCE FLOAT NOT NULL
                )''')
conn.commit()
conn.execute("INSERT OR IGNORE INTO ACCOUNTS VALUES ('admin', 'admin', 70000.00)")
conn.commit()
cur_lst = [1000, 500, 200, 100, 50, 20, 10]


def users():
    users_passwords_balance_list = []
    cursor = conn.execute("SELECT * FROM ACCOUNTS")
    conn.commit()
    for row in cursor:
        users_passwords_balance_list.append(row)
    return users_passwords_balance_list


def valid_username_check(username):
    """Usernames can contain letters (a-z), numbers (0-9), and periods (.). Usernames cannot contain
    an ampersand (&), equals sign (=), underscore (_), dash (-), plus sign (+), comma (,), brackets (<,>),
    or more than one period (.) in a row. Maximum length - 256 characters."""
    forbidden_symbols = '&=_-+,<>'
    for i in username:
        full_stops = []
        if (len(i) > 256) or (i in forbidden_symbols):
            print('Usernames can`t contain: &, =, _, -, +, comma (,), <, > or include more than 256 characters.')
            return False
        if i == '.':
            full_stops.append('.')
        if len(full_stops) >= 2:
            print('Usernames cannot contain more than one period (.) in a row.')
            return False
        else:
            return True


def valid_password_check(password):
    """
    1) At least 12 characters.
    2) A mixture of both uppercase and lowercase letters.
    3) A mixture of letters and numbers.
    4) Inclusion of at least one special character, e.g., ! @ # ? ]"""
    password_check_list = [len(password) >= 12]
    password_check_list.append((password.upper() != password) & (password.lower() != password))
    password_check_list.append(all([[i for i in password if i.isalpha()], [j for j in password if j.isdigit()]]))
    password_check_list.append(bool([n for n in password if n in '@#$%^&*()_+{}:"<>?']))
    if all(password_check_list):
        return True
    else:
        print('Password must include 12 or more characters; numbers; uppercase and lowercase letters')
        print('and minimum 1 special character such as ! @ # or ?')
        return False


def log_in(username):
    for i in range(3):
        password = input('Please enter your password: ')
        if bool([row for row in users() if (row[0] == username) & (row[1] == password)]):
            return username
        else:
            print(f'Incorrect username or password. {2 - i} attempts left.')
        if i == 2:
            return False


def sign_up(username):
    while True:
        if not valid_username_check(username):
            username = input('Please enter a valid username: ')
        else:
            break
    usernames_list = []
    for row in users():
        usernames_list.append(row[0])
    if username in usernames_list:
        print('You already have an account.')
        return log_in(username)
    else:
        password = input('Please come up with a password: ')
        while True:
            if not valid_password_check(password):
                password = input('Please come up with a valid password: ')
            else:
                cursor = conn.cursor()
                conn.execute("INSERT INTO ACCOUNTS VALUES (?,?,?)", (username, password, 0.00))
                conn.commit()
                return username


def admin_menu(username):
    if username != 'admin':
        print('ACCESS DENIED | ADMINS ONLY\nP.S. if you are admin - enter 3 and log in as admin)')
        return False
    else:
        conn.execute('''CREATE TABLE IF NOT EXISTS BANKNOTES
                        (CURRENCY INT PRIMARY KEY NOT NULL,
                        NUMBER INT,
                        SUM INT
                        )''')
        conn.commit()
        currency_dict = {1000: 10, 500: 20, 200: 50, 100: 100, 50: 200, 20: 500, 10: 1000}
        for key in currency_dict:
            suma = key * currency_dict[key]
            conn.execute("INSERT OR IGNORE INTO BANKNOTES VALUES (?, ?, ?)", (key, currency_dict[key], suma))
            conn.commit()

        def view_ATM_balance():
            ATM_currency_list = []
            sum_up = 0
            cursor = conn.execute("SELECT * FROM BANKNOTES")
            conn.commit()
            for row in cursor:
                ATM_currency_list.append(row)
                sum_up += row[2]
            conn.execute("UPDATE ACCOUNTS set BALANCE = ? where USERNAME = ?", (sum_up, 'admin'))
            conn.commit()
            return ATM_currency_list

        def change_ATM_balance():
            cur_bal = ()
            in_or_de = input('Enter `+` if you want to increase the ATM balance or `-` if you want to decrease it: ')
            perms_char = '+-'
            for ch in in_or_de:
                if ch not in perms_char:
                    return print('You can enter only + or -')
            if ('+' in in_or_de) & ('-' in in_or_de):
                return print('You have to choose only 1 operation: + or -')
            if not in_or_de:
                return print('You didn`t choose the operation. Try again :(')
            try:
                currency = int(input(f'Balance of which currency from these {cur_lst} would u like to be changed? '))
                print(currency)
                if currency not in cur_lst:
                    print(f'Only these {cur_lst} currency exist and could be changed')
                    return False
                else:
                    for row in view_ATM_balance():
                        if row[0] == currency:
                            cur_bal = row
                    amount = input('How many banknotes? ')
                    if amount:
                        if '-' in amount:
                            amount = amount.replace('-', '')
                            if '-' not in in_or_de:
                                in_or_de += '-'
                        if '.' in amount:
                            print('I can change only integer number of banknotes.')
                            return False
                        else:
                            amount = int(amount)
                    else:
                        amount = 0
                    if '-' in in_or_de:
                        if int(cur_bal[1]) < amount:
                            print('The operation is not possible - there are not enough funds on the balance :(')
                            print(f'Number of {cur_bal[0]} banknotes - {cur_bal[1]}, their sum - {cur_bal[2]}')
                            amount = 0
                        else:
                            amount *= -1
            except ValueError:
                print(f'Only these {cur_lst} currency exist and could be changed')
                return False
            new_bal = (currency, cur_bal[1] + amount, currency * (cur_bal[1] + amount))
            conn.execute("UPDATE BANKNOTES set NUMBER = ?, SUM = ? where CURRENCY = ?",
                         (new_bal[1], new_bal[2], new_bal[0]))
            conn.commit()
            if amount != 0:
                print('Operation successful!\nNew ATM balance:')
                print(tabulate.tabulate(
                    [('CURRENCY', 'NUMBER OF THIS CURRENCY', 'SUM OF THIS CURRENCY')] + view_ATM_balance()))

        while True:
            print('Choose an option:')
            first = '(1) Check the ATM balance - enter 1,'
            second = '\n(2) Check the balance of banknotes - enter 2,'
            third = '\n(3) Change the balance of banknotes - enter 3,'
            fourth = '\n(4) Check all the transactions - enter 4,'
            fifth = '\n(5) Exit - enter 5\n'
            action = input(first + second + third + fourth + fifth)
            if '1' in action:
                print('The ATM balance: ', balance(username))
            if '2' in action:
                print(tabulate.tabulate(
                    [('CURRENCY', 'NUMBER OF THIS CURRENCY', 'SUM OF THIS CURRENCY')] + view_ATM_balance()))
            if '3' in action:
                change_ATM_balance()
            if '4' in action:
                transactions_history('admin', 0, True)
            if not [i for i in range(1, 6) if str(i) in action]:
                print('Incorrect input. Please choose option 1, 2, 3, 4 or 5.')
            if '5' in action:
                break


def balance(username, changes=0):
    result = 0
    for i in users():
        if i[0] == username:
            b = str(i[2])
            if b:
                result = float(b.split('.')[0])
                if len(b.split('.')) == 2:
                    result += round(float(b.split('.')[1]) / (10 ** len(b.split('.')[1])), 2)
    result += changes
    conn.execute("UPDATE ACCOUNTS set BALANCE = ? where USERNAME = ?", (result, username))
    conn.commit()
    return result


def transactions_history(username, changes=0, show=False):
    cursor = conn.cursor()
    conn.execute('''CREATE TABLE IF NOT EXISTS ALL_TRANSACTIONS
                    (USERNAME TEXT NOT NULL,
                    OPERATION TEXT,
                    DATETIME TEXT
                    )''')
    conn.commit()
    if changes:
        if changes > 0:
            changes = '+' + str(changes)
        changes = str(changes)
        when = str(datetime.datetime.now())
        conn.execute("INSERT INTO ALL_TRANSACTIONS VALUES (?, ?, ?)", (username, changes, when))
        conn.commit()
    if show:
        transactions_list = []
        cursor = conn.execute("SELECT * FROM ALL_TRANSACTIONS")
        conn.commit()
        if username != 'admin':
            for row in cursor:
                if row[0] == username:
                    transactions_list.append(row)
        else:
            for row in cursor:
                transactions_list.append(row)
        print(tabulate.tabulate([('USERNAME', 'OPERATION', 'DATE/TIME')] + transactions_list))


def operation(username):
    earn_or_spend = input('Enter `+` if you want to deposit money on the card or `-` if you want to withdraw money: ')
    perms_char = '+-'
    for ch in earn_or_spend:
        if ch not in perms_char:
            return print('You can enter only + or -')
    if ('+' in earn_or_spend) & ('-' in earn_or_spend):
        return print('You have to choose only 1 operation: + or -')
    if not earn_or_spend:
        return print('You didn`t choose the operation. Try again :(')
    oper = input('How many? ')
    try:
        if oper:
            if '-' in oper:
                oper = oper.replace('-', '')
                if '-' not in earn_or_spend:
                    earn_or_spend += '-'
            if '.' in oper:
                oper = float(oper.split('.')[0]) + round(float(oper.split('.')[1]) / (10 ** len(oper.split('.')[1])), 2)
            else:
                oper = int(oper)
        else:
            oper = 0
        if '-' in earn_or_spend:
            if oper > balance(username):
                print('The operation is not possible - there are not enough funds on the balance :(')
                print('BALANCE: ', balance(username))
                oper = 0
            else:
                oper *= -1
    except ValueError:
        print('Sorry, I don`t know how to count with letters')
        oper = 0
    if balance('admin') + oper - oper % 10 >= 0:
        oper_ten = oper % 10
        if oper_ten:
            oper -= oper_ten
            print(f'Currency must be multiples of 10. So your change is: {oper_ten}, and operation sum is: {oper}')
        if oper < 0:
            rest = abs(oper)
            get_currency = {}
            for i in cur_lst:
                if rest >= i:
                    get_currency[i] = rest // i
                    rest = rest % i
            in_ATM_now = []
            cursor = conn.execute("SELECT * FROM BANKNOTES")
            conn.commit()
            for row in cursor:
                if row[0] in list(get_currency):
                    in_ATM_now.append(row)
            for i in in_ATM_now:
                new_number = i[1] - get_currency[i[0]]
                conn.execute("UPDATE BANKNOTES set NUMBER = ?, SUM = ? where CURRENCY = ?",
                             (new_number, new_number * i[0], i[0]))
            conn.commit()
            print('Get your money:')
            p_tables = PrettyTable()
            p_tables.field_names = ['CURRENCY', 'HOW MANY']
            for i in get_currency.items():
                p_tables.add_row(i)
            print(p_tables)
        balance(username, oper)
        transactions_history(username, oper)
        if oper != 0:
            print('Operation successful!')
    else:
        print('Sorry, not enough money in the ATM :(')


def start():
    lang = input('Please choose the language. Type ENG or RUS: ')
    if lang.upper() == 'RUS':
        print('Щелепи банкомата не налаштовані на російську')
        pygame.init()
        song = pygame.mixer.Sound('file.mp3')
        clock = pygame.time.Clock()
        song.play()
        while True:
            clock.tick(11)
        pygame.quit()
        return None
    if lang.upper() == 'ENG':
        account_exists = input('Do you have an account? If yes - type smth, if no - leave this field empty: ')
        your_name = input('Please enter the username: ')
        if account_exists:
            username = log_in(your_name)
        else:
            username = sign_up(your_name)

        if not username:
            return f'Login failed'
        else:
            if username == 'admin':
                admin_menu(username)
            else:
                while True:
                    print('\nChoose an action:\nIf you want to')
                    first = '(1) Check the balance - enter 1,'
                    second = '\n(2) Deposit or withdraw the money - enter 2,'
                    third = '\n(3) Log in to another account - enter 3,'
                    fourth = '\n(4) Watch the transactions - enter 4,'
                    fifth = '\n(5) Control panel - enter 5,'
                    sixth = '\n(6) Exit - enter 6\n'
                    action = input(first + second + third + fourth + fifth + sixth)
                    if '1' in action:
                        print('Your balance: ', balance(username))
                    if '2' in action:
                        operation(username)
                    if '3' in action:
                        username = input('Please enter the username: ')
                        if log_in(username) == 'admin':
                            admin_menu('admin')
                            break
                    if '4' in action:
                        transactions_history(username, 0, True)
                    if '5' in action:
                        admin_menu(username)
                    if not [i for i in range(1, 7) if str(i) in action]:
                        print('Incorrect input. Please choose option 1, 2, 3, 4, 5 or 6')
                    if '6' in action:
                        break
            conn.close()
            return f'Thank you for using my ATM! Have a nice day! :)'
    else:
        print('You can only choose ENG or RUS :( ')
        start()


print('WELCOME TO THE ATM!')
print(start())

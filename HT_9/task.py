"""Банкомат 2.0

    - усі дані зберігаються тільки в sqlite3 базі даних у відповідних таблицях.
    Більше ніяких файлів. Якщо в попередньому завданні ви добре продумали структуру програми,
    то у вас не виникне проблем швидко адаптувати її до нових вимог.

    - на старті додати можливість залогінитися або створити нового користувача (при створенні нового користувача,
    перевіряється відповідність логіну і паролю мінімальним вимогам. Для перевірки створіть окремі функції)

    - в таблиці з користувачами також має бути створений унікальний користувач-інкасатор, який матиме розширені
    можливості (домовимось, що логін/пароль будуть admin/admin щоб нам було простіше перевіряти)

    - банкомат має власний баланс

    - кількість купюр в банкоматі обмежена (тобто має зберігатися номінал та кількість).
    Номінали купюр - 10, 20, 50, 100, 200, 500, 1000

    - змінювати вручну кількість купюр або подивитися їх залишок в банкоматі може лише інкасатор

    - користувач через банкомат може покласти на рахунок лише суму кратну мінімальному номіналу що підтримує
    банкомат. В іншому випадку - повернути "здачу" (наприклад при поклажі 1005 --> повернути 5). Але це не має
    впливати на баланс/кількість купюр банкомату, лише збільшується баланс користувача (моделюємо наявність двох
    незалежних касет в банкоматі - одна на прийом, інша на видачу)

    - зняти можна лише в межах власного балансу, але не більше ніж є всього в банкоматі.

    - при неможливості виконання якоїсь операції - вивести повідомлення з причиною (невірний логін/пароль,
    недостатньо коштів на рахунку, неможливо видати суму наявними купюрами тощо.)

    - файл бази даних з усіма створеними таблицями і даними додайте в репозиторій, щоб ми могли його використати"""

import sqlite3
from tabulate import tabulate

conn = sqlite3.connect('atm.db')
cursor = conn.cursor()
conn.execute('''CREATE TABLE IF NOT EXISTS ACCOUNTS
                (USERNAME TEXT PRIMARY KEY NOT NULL,
                PASSWORD TEXT NOT NULL,
                BALANCE FLOAT NOT NULL
                )''')
conn.execute("INSERT OR IGNORE INTO ACCOUNTS VALUES ('admin', 'admin', 0.00)")


def users():
    users_passwords_balance_list = []
    cursor = conn.execute("SELECT * FROM ACCOUNTS")
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
                return username


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
    return result


def transactions_history(username, changes=0):
    conn.execute('''CREATE TABLE IF NOT EXISTS ALL_TRANSACTIONS
                    (USERNAME TEXT NOT NULL,
                    OPERATION TEXT NOT NULL
                    )''')
    if changes != 0:
        if changes >= 0:
            changes = '+' + str(changes)
        conn.execute("INSERT INTO ALL_TRANSACTIONS VALUES (?,?)", (username, str(changes)))


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
    print('Your operation: ', oper)
    print(balance(username, oper))
    transactions_history(username, oper)
    if oper != 0:
        print('Operation successful!')


def banknotes(username):
    if username != 'admin':
        print('ACCESS DENIED | ONLY ADMINS')
        return False
    else:
        conn.execute('''CREATE TABLE IF NOT EXISTS BANKNOTES
                        (CURRENCY INT PRIMARY KEY NOT NULL,
                        NUMBER INT,
                        SUM INT
                        )''')
        currency_dict = {10: 1000, 20: 500, 50: 200, 100: 100, 200: 50, 500: 20, 1000: 10}
        for key in currency_dict:
            suma = key * currency_dict[key]
            conn.execute("INSERT OR IGNORE INTO BANKNOTES VALUES (?, ?, ?)", (key, currency_dict[key], suma))


        def view_ATM_balance():
            ATM_currency_list = []
            sum_up = 0
            cursor = conn.execute("SELECT * FROM BANKNOTES")
            for row in cursor:
                ATM_currency_list.append(row)
                sum_up += row[2]
            conn.execute("UPDATE ACCOUNTS set BALANCE = ? where USERNAME = ?", (sum_up, 'admin'))
            return ATM_currency_list


        def change_ATM_balance():
            global cur_bal
            in_or_de = input('Enter `+` if you want to increase the ATM balance or `-` if you want to decrease it: ')
            perms_char = '+-'
            for ch in in_or_de:
                if ch not in perms_char:
                    return print('You can enter only + or -')
            if ('+' in in_or_de) & ('-' in in_or_de):
                return print('You have to choose only 1 operation: + or -')
            if not in_or_de:
                return print('You didn`t choose the operation. Try again :(')
            cur_lst = [10, 20, 50, 100, 200, 500, 1000]
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
            conn.execute("UPDATE BANKNOTES set NUMBER = ?, SUM = ? where CURRENCY = ?", (new_bal[1], new_bal[2], new_bal[0]))
            if amount != 0:
                print('Operation successful!')
                print('New ATM balance: ', view_ATM_balance())


        if input('If u`d like too change the ATM balance - type smth, if just watch - leave this field empty: '):
            change_ATM_balance()
        else:
            print(tabulate([('CURRENCY', 'NUMBER OF THIS CURRENCY', 'SUM OF THIS CURRENCY')] + view_ATM_balance()))




def start():
    print('WELCOME TO THE ATM!')

    account_exists = input('Do you have an account? If yes - type smth, if no - leave this field empty: ')
    your_name = input('Please enter the username: ')
    if account_exists:
        username = log_in(your_name)
    else:
        username = sign_up(your_name)

    if not username:
        return f'Login failed'
    else:
        print('\nChoose an action:\nIf you want to')
        while True:
            first = '(1) Check the balance - enter 1,'
            second = '\n(2) Deposit or withdraw the money - enter 2,'
            third = '\n(3) Log in to another account - enter 3,'
            fourth = '\n(4) Control panel - enter 4,'
            fifth = '\n(5) Exit - enter 5\n'
            action = input(first + second + third + fourth + fifth)
            if '1' in action:
                print('Your balance: ', balance(username))
            if '2' in action:
                operation(username)
            if '3' in action:
                username = input('Please enter the username: ')
                log_in(username)
            if '4' in action:
                banknotes(username)
            if ('1' not in action) & ('2' not in action) & ('3' not in action) & ('4' not in action) & ('5' not in action):
                print('Incorrect input. Please choose option 1, 2, 3, 4 or 5.')
            if '5' in action:
                break
        return f'Thank you for using my ATM! Have a nice day! :)'


print(start())

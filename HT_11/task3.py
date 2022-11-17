# Банкомат 4.0
# Переробіть программу з функціонального підходу програмування на використання класів.
# Додайте шанс 10% отримати бонус на баланс при створенні нового користувача.

import sqlite3
import tabulate
import datetime
from prettytable import PrettyTable
import random

conn = sqlite3.connect('atm.db')
cursor = conn.cursor()
conn.execute('''CREATE TABLE IF NOT EXISTS ACCOUNTS
                (USERNAME TEXT PRIMARY KEY NOT NULL,
                PASSWORD TEXT NOT NULL,
                BALANCE FLOAT
                )''')
conn.commit()
conn.execute("INSERT OR IGNORE INTO ACCOUNTS VALUES ('admin', 'admin', 70000.00)")
conn.commit()
cur_lst = [1000, 500, 200, 100, 50, 20, 10]
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
conn.execute('''CREATE TABLE IF NOT EXISTS ALL_TRANSACTIONS
                (USERNAME TEXT NOT NULL,
                OPERATION TEXT,
                DATETIME TEXT
                )''')
conn.commit()


class Users:

    def users_balance_passwords(self):
        users_passwords_balance_list = []
        cursor = conn.execute("SELECT * FROM ACCOUNTS")
        conn.commit()
        for row in cursor:
            users_passwords_balance_list.append(row)
        return users_passwords_balance_list


users = Users()


class Authorization:

    def __init__(self, username):
        self.username = username

    def valid_username_check(self):
        """Usernames can contain letters (a-z), numbers (0-9), and periods (.). Usernames cannot contain
        an ampersand (&), equals sign (=), underscore (_), dash (-), plus sign (+), comma (,), brackets (<,>),
        or more than one period (.) in a row. Maximum length - 256 characters."""

        for i in self.username:
            full_stops = []
            if (len(i) > 256) or (i in '&=_-+,<>'):
                print('Usernames can`t contain: &, =, _, -, +, comma (,), <, > or include more than 256 characters.')
                return False
            if i == '.':
                full_stops.append('.')
            if len(full_stops) >= 2:
                print('Usernames cannot contain more than one period (.) in a row.')
                return False
            else:
                return True

    def valid_password_check(self, password):
        """
        1) At least 12 characters.
        2) A mixture of both uppercase and lowercase letters.
        3) A mixture of letters and numbers.
        4) Inclusion of at least one special character, e.g., ! @ # ? ]"""
        password_check_list = [len(password) >= 12, (password.upper() != password) & (password.lower() != password),
                               all([[i for i in password if i.isalpha()], [j for j in password if j.isdigit()]]),
                               bool([n for n in password if n in '!@#$%^&*()_+{}:"<>?'])]
        if all(password_check_list):
            return True
        else:
            print('Password must include 12 or more characters; numbers; uppercase and lowercase letters')
            print('and minimum 1 special character such as ! @ # ? or others')
            return False

    def log_in(self):
        for i in range(3):
            password = input('Please enter your password: ')
            if bool([row for row in users.users_balance_passwords() if
                     (row[0] == self.username) & (row[1] == password)]):
                return self.username
            else:
                print(f'Incorrect username or password. {2 - i} attempts left.')
            if i == 2:
                return False

    def sign_up(self):
        while True:
            if not self.valid_username_check():
                self.username = input('Please enter a valid username: ')
            else:
                break
        usernames_list = []
        for row in users.users_balance_passwords():
            usernames_list.append(row[0])
        if self.username in usernames_list:
            print('You already have an account.')
            return self.log_in()
        else:
            password = input('Please come up with a password: ')
            while True:
                if not self.valid_password_check(password):
                    password = input('Please come up with a valid password: ')
                else:
                    cursor = conn.cursor()
                    if random.choices([True, False, False, False, False, False, False, False, False, False]):
                        print('Congratulation! You get bonus! Check your balance ;)')
                        conn.execute("INSERT INTO ACCOUNTS VALUES (?,?,?)", (self.username, password, 50.00))
                    else:
                        conn.execute("INSERT INTO ACCOUNTS VALUES (?,?,?)", (self.username, password, 0.00))
                    conn.commit()
                    return self.username


class AdminMenu:
    username = 'admin'
    first = '(1) Check the ATM balance - enter 1,'
    second = '\n(2) Check the balance of banknotes - enter 2,'
    third = '\n(3) Change the balance of banknotes - enter 3,'
    fourth = '\n(4) Check all the transactions - enter 4,'
    fifth = '\n(5) Exit - enter 5\n'

    def view_atm_balance(self):
        atm_currency_list = []
        sum_up = 0
        cursor = conn.execute("SELECT * FROM BANKNOTES")
        for row in cursor:
            atm_currency_list.append(list(row))
            sum_up += row[2]
        conn.execute("UPDATE ACCOUNTS set BALANCE = ? where USERNAME = ?", (sum_up, self.username))
        conn.commit()
        return atm_currency_list

    def change_atm_balance(self):
        in_or_de = input('Enter `+` if you want to increase the ATM balance or `-` if you want to decrease it: ')
        for ch in in_or_de:
            if ch not in '+-':
                return print('You can enter only + or -')
        if ('+' in in_or_de) & ('-' in in_or_de):
            return print('You have to choose only 1 operation: + or -')
        if not in_or_de:
            return print('You didn`t choose the operation. Try again :(')
        try:
            currency = int(input(f'Balance of which currency from these {cur_lst} would u like to be changed? '))
            if currency not in cur_lst:
                print(f'Only these {cur_lst} currency exist and could be changed')
                return False
            else:
                cur_bal = ()
                for row in self.view_atm_balance():
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
                        print(
                            f'Number of {cur_bal[0]} banknotes - {cur_bal[1]}, their sum - {cur_bal[2]}')
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
                [['CURRENCY', 'NUMBER OF THIS CURRENCY', 'SUM OF THIS CURRENCY']] + self.view_atm_balance()))

    def control_panel(self, username):
        if username != self.username:
            print('ACCESS DENIED | ADMINS ONLY\nP.S. if you are admin - enter 3 and log in as admin)')
            return False
        else:
            while True:
                print('Choose an option:')
                action = input(self.first + self.second + self.third + self.fourth + self.fifth)
                if '1' in action:
                    self.view_atm_balance()
                    money = Money(username)
                    print('The ATM balance: ', money.balance(username))
                if '2' in action:
                    print(tabulate.tabulate(
                        [['CURRENCY', 'NUMBER OF THIS CURRENCY', 'SUM OF THIS CURRENCY']] + self.view_atm_balance()))
                if '3' in action:
                    self.change_atm_balance()
                if '4' in action:
                    money = Money(username)
                    money.transactions_history(0, True)
                if not [i for i in range(1, 6) if str(i) in action]:
                    print('Incorrect input. Please choose option 1, 2, 3, 4 or 5.')
                if '5' in action:
                    break


class Money:
    perms_char = '+-'

    def __init__(self, username):
        self.username = username

    def balance(self, username, changes=0):
        result = 0
        for i in users.users_balance_passwords():
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

    def transactions_history(self, changes=0, show=False):
        if changes:
            if changes > 0:
                changes = '+' + str(changes)
            changes = str(changes)
            when = str(datetime.datetime.now())
            conn.execute("INSERT INTO ALL_TRANSACTIONS VALUES (?, ?, ?)", (self.username, changes, when))
            conn.commit()
        if show:
            cursor = conn.execute("SELECT * FROM ALL_TRANSACTIONS")
            conn.commit()
            transactions_list = []
            if self.username != 'admin':
                for row in cursor:
                    if row[0] == self.username:
                        transactions_list.append(row)
            else:
                for row in cursor:
                    transactions_list.append(row)
            print(tabulate.tabulate([('USERNAME', 'OPERATION', 'DATE/TIME')] + transactions_list))

    def operation(self):
        combinations, available_currency, unique_combinations = [], [], []
        get_currency = {}
        earn_or_spend = input('Enter `+` if you want to deposit money on the card or `-` if you want'
                              'to withdraw money: ')
        for ch in earn_or_spend:
            if ch not in self.perms_char:
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
                    oper = float(oper.split('.')[0]) + round(
                        float(oper.split('.')[1]) / (10 ** len(oper.split('.')[1])), 2)
                else:
                    oper = int(oper)
            else:
                oper = 0
            if '-' in earn_or_spend:
                if oper > self.balance(self.username):
                    print('The operation is not possible - there are not enough funds on the balance :(')
                    print('BALANCE: ', self.balance(self.username))
                    oper = 0
                else:
                    oper *= -1
        except ValueError:
            print('Sorry, I don`t know how to count with letters')
            oper = 0
        if self.balance('admin') + oper - oper % 10 >= 0:
            oper_ten = oper % 10
            if oper_ten:
                oper -= oper_ten
                print(f'Currency must be multiples of 10. So your change is: {oper_ten}, and operation sum is: {oper}')
            if oper < 0:
                old_name = self.username
                admin_menu = AdminMenu()
                for k in [i for i in admin_menu.view_atm_balance() if i[1]]:
                    for j in range(k[1]):
                        available_currency.append(k[0])
                for i in range(10000):
                    new_row = []
                    available_currency_for_new_row = list(available_currency)
                    while sum(new_row) < abs(oper):
                        val = random.choices(available_currency_for_new_row)[0]
                        new_row.append(val)
                        available_currency_for_new_row.remove(val)
                    combinations.append(new_row)
                sum_list = [sum(i) for i in combinations]
                best_match_combinations = [i for i in combinations if sum(i) == min(sum_list)]
                len_list = [len(i) for i in best_match_combinations]
                shortest_combinations = [i for i in best_match_combinations if len(i) == min(len_list)]
                sorted_combinations = [sorted(i, reverse=True) for i in shortest_combinations]
                for i in sorted_combinations:
                    if i not in unique_combinations:
                        unique_combinations.append(i)
                if len(unique_combinations) != 1:
                    first_elements = [k[0] for k in unique_combinations]
                    unique_combination = [row for row in unique_combinations if row[0] == max(first_elements)][0]
                else:
                    unique_combination = unique_combinations[0]
                for i in cur_lst:
                    if i in unique_combination:
                        get_currency[i] = unique_combination.count(i)
                admin_menu = AdminMenu()
                for l in [s for s in admin_menu.view_atm_balance() if s[0] in list(get_currency)]:
                    new_number = l[1] - get_currency[l[0]]
                    conn.execute("UPDATE BANKNOTES set NUMBER = ?, SUM = ? where CURRENCY = ?",
                                 (new_number, new_number * l[0], l[0]))
                conn.commit()

                self.username = old_name
                if sum(unique_combinations[0]) != abs(oper):
                    oper = sum(unique_combination)
                    print('Due to the lack of the necessary bills in the ATM, the withdrawal amount: ', oper)

                print('Get your money:')
                p_tables = PrettyTable()
                p_tables.field_names = ['CURRENCY', 'HOW MANY']
                for i in get_currency.items():
                    p_tables.add_row(i)
                print(p_tables)
            self.balance(self.username, oper)
            self.transactions_history(oper)
            if oper != 0:
                print('Operation successful!')
        else:
            print('Sorry, not enough money in the ATM :(')


class MainClass:
    first = '(1) Check the balance - enter 1,'
    second = '\n(2) Deposit or withdraw the money - enter 2,'
    third = '\n(3) Log in to another account - enter 3,'
    fourth = '\n(4) Watch the transactions - enter 4,'
    fifth = '\n(5) Control panel - enter 5,'
    sixth = '\n(6) Exit - enter 6\n'

    def start(self):
        lang = input('Please choose the language. Type ENG or RUS: ')
        if lang.upper() == 'RUS':
            import pygame
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
                username_actions = Authorization(your_name)
                username = username_actions.log_in()
            else:
                username_actions = Authorization(your_name)
                username = username_actions.sign_up()

            if not username:
                return f'Login failed'
            else:
                if username == 'admin':
                    admin_menu = AdminMenu()
                    admin_menu.control_panel(username)
                else:
                    while True:
                        print('\nChoose an action:\nIf you want to')
                        action = input(self.first + self.second + self.third + self.fourth + self.fifth + self.sixth)
                        if '1' in action:
                            money = Money(username)
                            print('Your balance: ', money.balance(username))
                        if '2' in action:
                            money = Money(username)
                            money.operation()
                        if '3' in action:
                            username = input('Please enter the username: ')
                            username_actions = Authorization(username)
                            if username_actions.log_in() == 'admin':
                                admin_menu = AdminMenu()
                                admin_menu.control_panel(username)
                                break
                        if '4' in action:
                            money = Money(username)
                            money.transactions_history(0, True)
                        if '5' in action:
                            admin_menu = AdminMenu()
                            admin_menu.control_panel(username)
                        if not [i for i in range(1, 7) if str(i) in action]:
                            print('Incorrect input. Please choose option 1, 2, 3, 4, 5 or 6')
                        if '6' in action:
                            break
                conn.close()
                return f'Thank you for using my ATM! Have a nice day! :)'
        else:
            print('You can only choose ENG or RUS :( ')
            self.start()


if __name__ == '__main__':
    print('WELCOME TO THE ATM!')
    main_class = MainClass()
    main_class.start()

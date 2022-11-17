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

    def accounts_and_balance(self):
        cursor = conn.execute("SELECT * FROM ACCOUNTS")
        users_passwords_balance_list = [i for i in cursor]
        conn.commit()
        return users_passwords_balance_list

    def set_and_get_user_balance(self, username, changes=0):
        result = 0
        for i in self.accounts_and_balance():
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

    def add_transactions(self, username, changes):
        if changes > 0:
            changes = '+' + str(changes)
        changes = str(changes)
        conn.execute("INSERT INTO ALL_TRANSACTIONS VALUES (?, ?, ?)", (username, changes, str(datetime.datetime.now())))
        conn.commit()

    def show_transactions(self, username=''):
        cursor = conn.execute("SELECT * FROM ALL_TRANSACTIONS")
        conn.commit()
        if username:
            transactions_list = [row for row in cursor if row[0] == username]
        else:
            transactions_list = [row for row in cursor]
        return print(tabulate.tabulate([('USERNAME', 'OPERATION', 'DATE/TIME')] + transactions_list))

    def oper_sum_to_number(self, oper):
        if '.' in oper:
            oper = float(oper.split('.')[0]) + round(float(oper.split('.')[1]) / (10 ** len(oper.split('.')[1])), 2)
        else:
            oper = int(oper)
        return oper

    def operation_sum(self, oper, earn_or_spend):
        after_minus_check = banknotes_operations.negative_amount(oper, earn_or_spend)
        oper = after_minus_check[0]
        earn_or_spend = after_minus_check[1]
        oper = self.oper_sum_to_number(oper)
        return oper, earn_or_spend

    def enough_user_balance(self, username, oper, earn_or_spend):
        if '-' in earn_or_spend:
            if oper > self.set_and_get_user_balance(username):
                print('The operation is not possible - there are not enough funds on the balance :(')
                print('BALANCE: ', self.set_and_get_user_balance(username))
                oper = 0
            else:
                oper *= -1
        return oper

    def multiples_of_10(self, oper):
        if banknotes_operations.atm_balance() + oper - oper % 10 >= 0:
            oper_ten = oper % 10
            if oper_ten:
                oper -= oper_ten
                print(f'Currency must be multiples of 10. So your change is: {oper_ten}, and operation sum is: {oper}')
        else:
            print('Sorry, not enough money in the ATM :(')
            oper = 0
        return oper

    def available_currency(self):
        available_currency = []
        for k in [i for i in banknotes_operations.atm_contents() if i[1]]:
            for j in range(k[1]):
                available_currency.append(k[0])
        return available_currency

    def combinations(self, oper):
        combinations = []
        for i in range(10000):
            new_row = []
            available_currency_for_new_row = list(self.available_currency())
            while sum(new_row) < abs(oper):
                val = random.choices(available_currency_for_new_row)[0]
                new_row.append(val)
                available_currency_for_new_row.remove(val)
            combinations.append(new_row)
        return combinations

    def unique_combination(self, combinations):
        unique_combinations = []
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
        return unique_combination

    def get_currency(self, unique_combination):
        get_currency = {}
        for i in cur_lst:
            if i in unique_combination:
                get_currency[i] = unique_combination.count(i)
        return get_currency

    def update_banknotes(self, get_currency):
        for l in [s for s in banknotes_operations.atm_contents() if s[0] in list(get_currency)]:
            new_number = l[1] - get_currency[l[0]]
            conn.execute("UPDATE BANKNOTES set NUMBER = ?, SUM = ? where CURRENCY = ?",
                         (new_number, new_number * l[0], l[0]))
        conn.commit()

    def withdrow_money(self, oper):
        combinations = self.combinations(oper)
        unique_combination = self.unique_combination(combinations)
        get_currency = self.get_currency(unique_combination)
        self.update_banknotes(get_currency)
        if sum(unique_combination) != abs(oper):
            oper = sum(unique_combination)
            print('Due to the lack of the necessary bills in the ATM, the withdrawal amount: ', oper)
        print('Get your money:')
        p_tables = PrettyTable()
        p_tables.field_names = ['CURRENCY', 'HOW MANY']
        for i in get_currency.items():
            p_tables.add_row(i)
        print(p_tables)

    def operation(self, username):
        earn_or_spend = banknotes_operations.put_or_get('user')
        if not earn_or_spend:
            print('You didn`t choose the operation. Try again :(')
            return False
        oper = input('How many? ')
        try:
            if oper:
                prepared_data = self.operation_sum(oper, earn_or_spend)
                oper = prepared_data[0]
                earn_or_spend = prepared_data[1]
                oper = self.enough_user_balance(username, oper, earn_or_spend)
                oper = self.multiples_of_10(oper)
                if oper < 0:
                    self.withdrow_money(oper)
                self.set_and_get_user_balance(username, oper)
                self.add_transactions(username, oper)
                if oper != 0:
                    print('Operation successful!')
            else:
                return False
        except ValueError:
            print('Sorry, I don`t know how to count with letters')
            return False


users = Users()


class Authorization:

    def __init__(self, username):
        self.username = username

    def log_in(self):
        for i in range(3):
            password = input('Please enter your password: ')
            if bool([row for row in users.accounts_and_balance() if
                     (row[0] == self.username) & (row[1] == password)]):
                return self.username
            else:
                print(f'Incorrect username or password. {2 - i} attempts left.')
            if i == 2:
                return False

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

    def valid_username_input(self):
        while True:
            if not self.valid_username_check():
                self.username = input('Please enter a valid username: ')
            else:
                break

    def account_exists_check(self):
        usernames_list = [i[0] for i in users.accounts_and_balance()]
        if self.username in usernames_list:
            print('You already have an account.')
            return True
        else:
            return False

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

    def lottery(self, password):
        cursor = conn.cursor()
        if random.choices([True, False, False, False, False, False, False, False, False, False]):
            print('Congratulation! You get bonus! Check your balance ;)')
            conn.execute("INSERT INTO ACCOUNTS VALUES (?,?,?)", (self.username, password, 50.00))
        else:
            conn.execute("INSERT INTO ACCOUNTS VALUES (?,?,?)", (self.username, password, 0.00))
        conn.commit()

    def sign_up(self):
        self.valid_username_input()
        if self.account_exists_check():
            print('You already have an account.')
            return self.log_in()
        else:
            password = input('Please come up with a password: ')
            while True:
                if not self.valid_password_check(password):
                    password = input('Please come up with a valid password: ')
                else:
                    break
            self.lottery(password)
            return self.username


class BanknotesOperations:
    admin_in_or_de_text = 'Enter `+` if you want to increase the ATM balance or `-` if you want to decrease it: '
    user_in_or_de_text = 'Enter `+` if you want to deposit money on the card or `-` if you want to withdraw money: '

    def atm_contents(self):
        cursor = conn.execute("SELECT * FROM BANKNOTES")
        atm_currency_list = [list(row) for row in cursor]
        conn.commit()
        return atm_currency_list

    def atm_balance(self, username = 'admin'):
        balance = sum([i[2] for i in self.atm_contents()])
        conn.execute("UPDATE ACCOUNTS set BALANCE = ? where USERNAME = ?", (balance, username))
        conn.commit()
        return balance

    def put_or_get(self, who):
        if who == 'admin':
            in_or_de = input(self.admin_in_or_de_text)
        else:
            in_or_de = input(self.user_in_or_de_text)
        if (len(in_or_de) != 1) or (in_or_de not in '+-'):
            print('You have to choose only 1 operation: + or -')
            return False
        else:
            return in_or_de

    def choose_currency(self):
        try:
            currency = int(input(f'Balance of which currency from these {cur_lst} would u like to be changed? '))
            if currency not in cur_lst:
                return False
            else:
                return currency
        except ValueError:
            return False

    def negative_amount(self, amount, in_or_de):
        if '-' in amount:
            amount = amount.replace('-', '')
            if '-' not in in_or_de:
                in_or_de += '-'
        return amount, in_or_de

    def amount_to_int(self, amount):
        if '.' in amount:
            print('I can change only integer number of banknotes.')
            amount = 0
        else:
            try:
                amount = int(amount)
            except ValueError:
                print('I can`t count with letters')
                amount = 0
        return amount

    def choose_amount(self, in_or_de):
        amount = input('How many banknotes? ')
        if amount:
            after_minus_check = self.negative_amount(amount, in_or_de)
            amount = after_minus_check[0]
            in_or_de = after_minus_check[1]
            amount = self.amount_to_int(amount)
        else:
            amount = 0
        return amount, in_or_de

    def prepare_data_to_insert(self, in_or_de, cur_bal, currency, amount):
        if '-' in in_or_de:
            if int(cur_bal[1]) < amount:
                print('The operation is not possible - there are not enough funds on the balance :(')
                print(
                    f'Number of {cur_bal[0]} banknotes - {cur_bal[1]}, their sum - {cur_bal[2]}')
                amount = 0
            else:
                amount *= -1
        new_bal = (currency, cur_bal[1] + amount, currency * (cur_bal[1] + amount))
        return new_bal, amount

    def insert_data_to_atm(self, new_bal):
        conn.execute("UPDATE BANKNOTES set NUMBER = ?, SUM = ? where CURRENCY = ?",
                     (new_bal[1], new_bal[2], new_bal[0]))
        conn.commit()

    def new_atm_contents_show(self, amount):
        if amount:
            print('Operation successful!\nNew ATM balance:')
            print(tabulate.tabulate(
                [['CURRENCY', 'NUMBER OF THIS CURRENCY', 'SUM OF THIS CURRENCY']] + self.atm_contents()))

    def change_atm_balance(self):
        in_or_de = self.put_or_get('admin')
        if not in_or_de:
            print('You didn`t choose the operation. Try again :(')
            return False
        currency = self.choose_currency()
        if not currency:
            print(f'Only these {cur_lst} currency exist and could be changed')
            return False
        cur_bal = [row for row in self.atm_contents() if row[0] == currency][0]
        choose_amount_result = self.choose_amount(in_or_de)
        amount = choose_amount_result[0]
        in_or_de = choose_amount_result[1]
        ready_to_insert = self.prepare_data_to_insert(in_or_de, cur_bal, currency, amount)
        new_bal = ready_to_insert[0]
        amount = ready_to_insert[1]
        self.insert_data_to_atm(new_bal)
        self.new_atm_contents_show(amount)


banknotes_operations = BanknotesOperations()


class AdminMenu:
    username = 'admin'
    first = '(1) Check the ATM balance - enter 1,'
    second = '\n(2) Check the balance of banknotes - enter 2,'
    third = '\n(3) Change the balance of banknotes - enter 3,'
    fourth = '\n(4) Check all the transactions - enter 4,'
    fifth = '\n(5) Exit - enter 5\n'
    banknotes_header = ['CURRENCY', 'NUMBER OF THIS CURRENCY', 'SUM OF THIS CURRENCY']

    def rights_check(self, username):
        if username != self.username:
            print('ACCESS DENIED | ADMINS ONLY\nP.S. if you are admin - enter 3 and log in as admin)')
            return False
        else:
            return True

    def control_panel(self, username):
        if self.rights_check(username):
            while True:
                print('Choose an option:')
                action = input(self.first + self.second + self.third + self.fourth + self.fifth)
                if '1' in action:
                    print('The ATM balance: ', banknotes_operations.atm_balance())
                if '2' in action:
                    print(tabulate.tabulate([self.banknotes_header] + banknotes_operations.atm_contents()))
                if '3' in action:
                    banknotes_operations.change_atm_balance()
                if '4' in action:
                    users.show_transactions()
                if not [i for i in range(1, 6) if str(i) in action]:
                    print('Incorrect input. Please choose option 1, 2, 3, 4 or 5.')
                if '5' in action:
                    break
        else:
            return False


class MainClass:
    first = '(1) Check the balance - enter 1,'
    second = '\n(2) Deposit or withdraw the money - enter 2,'
    third = '\n(3) Log in to another account - enter 3,'
    fourth = '\n(4) Watch the transactions - enter 4,'
    fifth = '\n(5) Control panel - enter 5,'
    sixth = '\n(6) Exit - enter 6\n'

    def rus_lang(self):
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

    def eng_lang(self):
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
                        print('Your balance: ', users.set_and_get_user_balance(username))
                    if '2' in action:
                        users.operation(username)
                    if '3' in action:
                        username = input('Please enter the username: ')
                        username_actions = Authorization(username)
                        if username_actions.log_in() == 'admin':
                            admin_menu = AdminMenu()
                            admin_menu.control_panel(username)
                            break
                    if '4' in action:
                        users.show_transactions(username)
                    if '5' in action:
                        admin_menu = AdminMenu()
                        admin_menu.control_panel(username)
                    if not [i for i in range(1, 7) if str(i) in action]:
                        print('Incorrect input. Please choose option 1, 2, 3, 4, 5 or 6')
                    if '6' in action:
                        break
            conn.close()
            return f'Thank you for using my ATM! Have a nice day! :)'

    def start(self):
        lang = input('Please choose the language. Type ENG or RUS: ').upper()
        if lang == 'RUS':
            self.rus_lang()
        if lang == 'ENG':
            self.eng_lang()
        else:
            print('You can only choose ENG or RUS :( ')
            self.start()


if __name__ == '__main__':
    print('WELCOME TO THE ATM!')
    main_class = MainClass()
    main_class.start()
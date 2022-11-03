#TASK 3
"""Програма-банкомат.
   Використовуючи функції створити програму з наступним функціоналом:
      - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.CSV>);
      - кожен з користувачів має свій поточний баланс (файл <{username}_balance.TXT>) та історію транзакцій (файл <{username_transactions.JSON>);
      - є можливість як вносити гроші, так і знімати їх. Обов'язкова перевірка введених даних (введено цифри; знімається не більше, ніж є на рахунку і т.д.).
   Особливості реалізації:
      - файл з балансом - оновлюється кожен раз при зміні балансу (містить просто цифру з балансом);
      - файл - транзакціями - кожна транзакція у вигляді JSON рядка додається в кінець файла;
      - файл з користувачами: тільки читається. Але якщо захочете реалізувати функціонал додавання нового користувача - не стримуйте себе :)
   Особливості функціонала:
      - за кожен функціонал відповідає окрема функція;
      - основна функція - <start()> - буде в собі містити весь workflow банкомата:
      - на початку роботи - логін користувача (програма запитує ім'я/пароль). Якщо вони неправильні - вивести повідомлення про це і закінчити роботу (хочете - зробіть 3 спроби, а потім вже закінчити роботу - все на ентузіазмі :))
      - потім - елементарне меню типн:
        Введіть дію:
           1. Подивитись баланс
           2. Поповнити баланс
           3. Вихід
      - далі - фантазія і креатив, можете розширювати функціонал, але основне завдання має бути повністю реалізоване :)
    P.S. Увага! Файли мають бути саме вказаних форматів (csv, txt, json відповідно)
    P.S.S. Добре продумайте структуру програми та функцій"""


import csv
import json
import datetime


def users_passwords(file_name = 'users.csv'):
    with open(file_name, 'r', newline = '') as file:
        reader = csv.DictReader(file)
        users_passwords_list = []
        for record in reader:
            users_passwords_list.append(record)
        return users_passwords_list
    

def balance(username, changes = 0):
    file_name = str(username) + '_balance.TXT'
    with open(file_name, 'r+') as file:
        file.seek(0)
        b = file.read()
        if '\x00' in b:
            b = b.replace('\x00', '')
        if b:
            result = float(b.split('.')[0]) 
            if len(b.split('.')) == 2:
                result += round(float(b.split('.')[1]) / (10 ** len(b.split('.')[1])), 2)
        else:
            result = 0
        result += changes
        file.truncate(0)
        file.write(str(result))
    return result


def transactions_history(username, changes = 0):
    if changes != 0:
        file_name = str(username) + '_transactions.JSON'
        try:
            with open(file_name) as file:
                transactions_dict = json.load(file)
        except:
            transactions_dict = {}
        when = str(datetime.datetime.now())
        if changes >= 0:
            changes = '+' + str(changes)
        transactions_dict.update({when: str(changes)})
        json_object = json.dumps(transactions_dict)
        with open(file_name, "w") as outfile:
            outfile.write(json_object)
    
    
def operation(username):
    earn_or_spend = input('Enter `+` if you want to deposit money on the card or `-` if you want to withdraw money: ')
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
    balance(username, oper)
    transactions_history(username, oper)
    if oper != 0:
        print('Operation successful!')

    
def log_in():
    for i in range(3):
        username = input('Please enter your username: ')
        password = input('Please enter your password: ')
        if bool([i for i in users_passwords() if (i['username'] == username) & (i['password'] == password)]):
            return username
            break
        else:
            print(f'Incorrect username or password. {2 - i} attempts left.')
        if i == 2:
            return False
    
    
def start():
    print('WELCOME TO THE ATM!')
    username = log_in()
    if not username:
        return f'Login failed'
    else:
        print('\nChoose an action:\nIf you want to')
        while True:
            action = input('>Check the balance - enter 1,\n>Deposit or withdraw the money - enter 2,\n>Exit - enter 3\n')
            if '1' in action:
                print('Your balance: ', balance(username))
            if '2' in action:
                operation(username)
            if ('1' not in action) & ('2' not in action) & ('3' not in action):
                print('Incorrect input. Please choose option 1, 2 or 3.')
            if '3' in action:
                break
        return f'Thank you for using my ATM! Have a nice day! :)'
        
        
print(start())
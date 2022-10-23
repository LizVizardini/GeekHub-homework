#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 3
"""На основі попередньої функції (скопіюйте кусок коду) створити наступний скрипт:
   а) створити список із парами ім'я/пароль різноманітних видів (орієнтуйтесь по правилам своєї функції) - як валідні, так і ні;
   б) створити цикл, який пройдеться по цьому циклу і, користуючись валідатором, перевірить ці дані і надрукує для кожної пари значень
   відповідне повідомлення, наприклад:
      Name: vasya
      Password: wasd
      Status: password must have at least one digit
      -----
      Name: vasya
      Password: vasyapupkin2000
      Status: OK
   P.S. Не забудьте використати блок try/except ;)
"""


class LoginException(Exception):
    ...


def list_validation():
    # a)
    lst = [['Quincy100'], ['Wi'], ['Ellalalalalalalalalalalalalalalalalalallalalalala^_^'], ['Ro55'], ['Tilni#1']]
    for i in range (len(lst)):
        lst[i].append(''.join((random.choice(string.ascii_letters + string.digits) for i in range(random.randint(5, 15)))))
    # б)
    for i in range (len(lst)):
        print(f'Name: {lst[i][0]}\nPassword: {lst[i][1]}\n\nStatus:')
        try:
            if len(lst[i][0]) < 3 or len(lst[i][0]) > 50:
                raise LoginException('The username must include from 3 to 50 symbols')
            if len(lst[i][1]) < 8 or all(not char.isdigit() for char in lst[i][1]):
                raise LoginException('The password must include 8 symbols or more and at least 1 of them must be a number')
            if lst[i][0] == lst[i][1]:
                raise LoginException('The password and the username could not be equal')
            if ' ' in lst[i][1]:
                raise LoginException('The password could not includ space')
            else:
                print('OK')
        except LoginException as le:
            print(le)
        print('------------------------------------------------------------------------------------')
        if i == len(lst) - 1:
            print('THAT`S ALL USERS')
        

list_validation()
#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 1
"""Створіть функцію, всередині якої будуть записано СПИСОК із п'яти користувачів (ім'я та пароль).
Функція повинна приймати три аргументи: два - обов'язкових (<username> та <password>) і третій -
необов'язковий параметр <silent> (значення за замовчуванням - <False>).
Логіка наступна:
    якщо введено правильну пару ім'я/пароль - вертається True;
    якщо введено неправильну пару ім'я/пароль:
        якщо silent == True - функція повертає False
        якщо silent == False - породжується виключення LoginException (його також треба створити =))"""

class LoginException(Exception):
    ...


def passwords_base(username, password, silent = False):
    lst = [['Quincy100', '86ktzQGnlj'], ['Wi77', 'rrt9GUbp'], ['Ellala^_^', '7kKOnW12nI'],
           ['Ro55', 'XW1gXXyj9I5o'], ['Tilni#1', 'iSKYn8UnfBXnj']]
    for i in lst:
        if [username, password] in lst:
            return True
        elif silent == True:
            return False
        else:
            raise LoginException('Incorrect username or password')


try:
    print(passwords_base('Quincy100', 'b bbjjb'))
except LoginException as le:
    print(f'Try again. {[le]}')
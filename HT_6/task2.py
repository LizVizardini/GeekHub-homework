#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 2
#Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
#   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
#   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну цифру;
#   - якесь власне додаткове правило :)
#   Якщо якийсь із параметрів не відповідає вимогам - породити виключення із відповідним текстом.

class LoginException(Exception):
    ...


def validation(username, password):
    lst = [['Quincy100', '86ktzQGnlj'], ['Wi77', 'rrt9GUbp'], ['Ellala^_^', '7kKOnW12nI'],
           ['Ro55', 'XW1gXXyj9I5o'], ['Tilni#1', 'iSKYn8UnfBXnj']]
    if len(username) < 3 or len(username) > 50:
        raise LoginException('The username must include from 3 to 50 symbols')
    if len(password) < 8 or all(not char.isdigit() for char in password):
        raise LoginException('The password must include 8 symbols or more and at least 1 of them must be a number')
    if username == password:
        raise LoginException('The password and the username could not be equal')
    if ' ' in password:
        raise LoginException('The password could not includ space')
    if [username, password] in lst:
        return f'Login complete succesfully!'
    else:
        lst.append([username, password])
        return lst
    
        
        
try:
    print(validation('Quincy100', '86 ktzQGnlj'))
except LoginException as le:
    print(f'Try again. {[le]}')
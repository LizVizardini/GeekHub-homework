#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 4
"""Наприклад маємо рядок -->
"f98neroi4nr0c3n30irn03ien3c0rfe kdno400we(nw,kowe%00koi!jn35pijnp4 6ij7k5j78p3kj546p4 65jnpoj35po6j345"
-> просто потицяв по клавi =)
   Створіть ф-цiю, яка буде отримувати довільні рядки на зразок цього та яка обробляє наступні випадки:
-  якщо довжина рядка в діапазоні 30-50 (включно) -> прiнтує довжину рядка, кiлькiсть букв та цифр
-  якщо довжина менше 30 -> прiнтує суму всіх цифр та окремо рядок без цифр та знаків лише з буквами (без пробілів)
-  якщо довжина більше 50 -> щось вигадайте самі, проявіть фантазію =)"""


import re


def stringmeter():
    my_string = input('Please enter smth. Yes, u can just haphazardly poke around the keyboard =)\n')
    no_digits = ''.join([i for i in my_string if not i.isdigit()])
    letters = re.sub(r'[^\w]', '', no_digits)
    digits = ''.join([i for i in my_string if i.isdigit()])
    if (len(my_string) >= 30) & (len(my_string) <= 50):
        print('\nString length: ', len(my_string))
        print(f'It includes {len(letters)} letters.')
        print(f'Also it includes {len(digits)} digits.')
    elif len(my_string) < 30:
        digits_sum = 0
        for i in digits:
            digits_sum += int(i)
        print('\nSum of the digits is: ', digits_sum)
        print('Your string without numbers and symbols: ', letters)
    else:
        for i in my_string:
            if i.isdigit():
                if int(i) % 2 == 0:
                    my_string = my_string.replace(i, '0')
                else:
                    my_string = my_string.replace(i, '1')
        print(my_string.upper())


stringmeter()
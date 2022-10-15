#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 3
"""Користувач вводить змінні "x" та "y" з довільними цифровими значеннями. Створіть просту умовну конструкцію (звiсно вона повинна бути
в тiлi ф-цiї), під час виконання якої буде перевірятися рівність змінних "x" та "y" та у випадку нерівності - виводити ще і різницю.
    Повинні працювати такі умови (x, y, z заміність на відповідні числа):
    x > y;       вiдповiдь - "х бiльше нiж у на z"
    x < y;       вiдповiдь - "у бiльше нiж х на z"
    x == y.      відповідь - "х дорівнює y" """


def compare():
    while True:
        try:
            x = float(input('Please enter the 1st number: '))
            y = float(input('Please enter the 2nd number: '))
            if x > y:
                return print(f'\n{x} is larger than {y} on {x - y}')
                break
            if y > x:
                return print(f'\n{y} is larger than {x} on {y - x}')
                break
            else:
                return print(f'\n{x} and {y} are equal')
                break
        except ValueError:
            print('Entered values must be NUMBERS. Try again :)\n')

            
compare()
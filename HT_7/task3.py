#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 3
"""Напишіть свою реалізацію функції <range>. Тобто щоб її можна було використати у вигляді:
    for i in my_range(1, 10, 2):
        print(i)
    1
    3
    5
    7
    9
   P.S. Повинен вертатись генератор.
   P.P.S. Для повного розуміння цієї функції - можна почитати документацію по ній:
   https://docs.python.org/3/library/stdtypes.html#range
   P.P.P.S Не забудьте обробляти невалідні ситуації (типу range(1, -10, 5) тощо).
   Подивіться як веде себе стандартний range в таких випадках."""


def my_range(start, end = False, step = False):
    if start:
        args = [start]
    else:
        args = [0]
    if end:
        args.append(end)
    if step:
        args.append(step)
    if len(args) < 3:
        step = 1
        if len(args) == 2:
            start = args[0]
            end = args[1]
        else:
            start = 0
            end = args[0]
    start = int(start)
    end = int(end)
    step = int(step)
    while start != end:
            yield start
            start += step
        

print('One argument given:')
lst = []
for i in my_range(16):
    lst.append(i)
print(lst)

print('\nTwo arguments given:')
lst = []
for i in my_range(0, 16):
    lst.append(i)
print(lst)

print('\nThree argument given:')
lst = []
for i in my_range(0, 16, 1):
    lst.append(i)
print(lst)

print('\nInvalid situations:')
lst = []
for i in my_range(1, -10, 5):
    lst.append(i)
print(lst)
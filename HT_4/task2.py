#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 2
"""Створіть 3 рiзних функцiї (на ваш вибiр). Кожна з цих функцiй повинна повертати якийсь результат (напр. інпут від юзера, результат
математичної операції тощо). Також створiть четверту ф-цiю, яка всередині викликає 3 попередні, обробляє їх результат та також повертає
результат своєї роботи. Таким чином ми будемо викликати одну (четверту) функцiю, а вона в своєму тiлi - ще 3."""


def sum_of_two():
    a = float(input('The first adding number (a): '))
    b = float(input('The second adding number (b): '))
    return a + b


def subtraction_of_two():
    a = float(input('Minuend (c): '))
    b = float(input('Subtrahend (d): '))
    return a - b


def multiplication(a, b):
    return a * b


def full_expression():
    return multiplication(sum_of_two(), subtraction_of_two()) ** 2


print('\n((a + b) * (c - d))^2 = ', full_expression())
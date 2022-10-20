#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 2
"""Написати функцію <bank> , яка працює за наступною логікою: користувач робить вклад у розмірі <a> одиниць строком на <years>
років під <percent> відсотків (кожен рік сума вкладу збільшується на цей відсоток, ці гроші додаються до суми вкладу і в наступному
році на них також нараховуються відсотки). Параметр <percents> є необов'язковим і має значення по замовчуванню <10> (10%).
Функція повинна принтануть суму, яка буде на рахунку, а також її повернути (але округлену до копійок)."""


def bank(a, years, percent = 10):
    for i in range (years):
        a += a * percent / 100
        print(f'After {i + 1} year(s), the amount is {a} currency units')
    rounded_sum = round(a, 2)
    return rounded_sum


a = float(input('Amount of deposit: '))
years = int(input('After how many years do you plan to get the money back? '))
try:
    percent = int(input('At what percentage is the money invested? \n'))
    print('\nThe amount you will receive as a result: ', bank(a, years, percent))
except ValueError:
    print('\nThe amount you will receive as a result: ', bank(a, years))
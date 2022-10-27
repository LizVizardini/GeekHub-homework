#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 4
"""Реалізуйте генератор, який приймає на вхід будь-яку ітерабельну послідовність (рядок, список, кортеж) і повертає генератор,
який буде повертати значення з цієї послідовності, при цьому, якщо було повернено останній елемент із послідовності - ітерація починається знову.
   Приклад (якщо запустили його у себе - натисніть Ctrl+C ;) ):
   for elem in my_generator([1, 2, 3]):
       print(elem)
   1
   2
   3
   1
   2
   3
   1
   ......."""


def my_generator(sequence):
    while True:
        for i in sequence:
            yield i
        sequence += sequence

        
for elem in my_generator([1, 2, 3]):
       print(elem)
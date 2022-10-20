#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 1
#Написати функцію <square>, яка прийматиме один аргумент - сторону квадрата,
#і вертатиме 3 значення у вигляді кортежа: периметр квадрата, площа квадрата та його діагональ.


import math


def square(side):
    P = 4 * side
    S = side ** 2
    d = side * math.sqrt(2)
    return (P, S, d)


square(float(input('Please enter the length of the side of the square: ')))
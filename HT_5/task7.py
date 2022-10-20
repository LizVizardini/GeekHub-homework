#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 7
#Написати функцію, яка приймає на вхід список (через кому), підраховує кількість однакових елементів у ньому і виводить результат.
#Елементами списку можуть бути дані будь-яких типів.
#    Наприклад:
#    1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2] ----> "1 -> 3, foo -> 2, [1, 2] -> 2, True -> 1

lst = [1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2]]


def count_list_elements(lst):
    unique_elements, bools = [], []
    for i in lst:
        if (i not in unique_elements) & (type(i) != bool):
            unique_elements.append(i)
        if type(i) == bool:
            bools.append(i)
    i = 0
    while i < len(lst):
        if type(lst[i]) == bool:
            del lst[i]
        else:
            i += 1
    for i in unique_elements:
        print(i, '->', lst.count(i))
    if True in bools:
        print(True, '->', bools.count(True))
    if False in bools:
        print(False, '->', bools.count(False))
        
        
count_list_elements(lst)
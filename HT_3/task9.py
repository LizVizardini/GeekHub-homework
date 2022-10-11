#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 9
#Користувачем вводиться початковий і кінцевий рік. Створити цикл, який виведе всі високосні роки в цьому проміжку (границі включно).
#P.S. Рік є високосним, якщо він кратний 4, але не кратний 100, а також якщо він кратний 400.

term = input('Please write year of beginning and end separated by "-": ').split('-')
for i in range (int(term[0]), int(term[1]) + 1):
    if ((i % 4 == 0) and (i % 100 != 0)) or (i % 400 == 0):
        print(i)
exit()

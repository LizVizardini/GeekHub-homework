#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 8
#Створити цикл від 0 до ... (вводиться користувачем).
#В циклі створити умову, яка буде виводити поточне значення, якщо остача від ділення на 17 дорівнює 0.

n = int(input('Please enter any integer: '))
for i in range (n):
    if i % 17 == 0:
        print(i)
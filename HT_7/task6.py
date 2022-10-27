#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 6
#Напишіть функцію,яка приймає рядок з декількох слів і повертає довжину найкоротшого слова.
#Реалізуйте обчислення за допомогою генератора в один рядок.


def shorter_word_lenght(my_str):
    return min([len(i) for i in my_str.split()])


shorter_word_lenght(input('Please enter a string that consists of a few words without symbols:\n'))
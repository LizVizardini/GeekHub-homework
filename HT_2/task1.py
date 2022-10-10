#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 1
#Write a script that accepts a sequence of comma-separated numbers from the user
#and generates a list and a tuple with those numbers.

#CREATING THE LIST
numbers = input('Please write some comma-separated numbers: ')
lst = list(map(float, numbers.split(',')))
print('Here is a list of them:', lst)

#CREATING THE TUPLE
numbers = input('\nPlease write some other comma-separated numbers: ')
tpl = tuple(map(float, numbers.split(',')))
print('Here is a tuple of them:', tpl)
exit()

#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 4
#Write a script that accepts a <number> from the user and then <number> times asks the user for string input.
#In the end, the script must print out the result of concatenating all <number> strings.

n = int(input('Please input a number: '))
s = ''
for i in range (n):
    s += input('Please enter smth: ')
print(s)
exit()

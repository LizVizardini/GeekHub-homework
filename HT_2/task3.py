#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 3
#Write a script that accepts a <number> from the user
#and prints out a sum of the first <number> positive integers.

n = int(input('Please input a number: '))
sum = 0
for i in range (1, n+1):
    sum += i
print(f'A sum of the first {n} positive integers: {sum}')
exit()

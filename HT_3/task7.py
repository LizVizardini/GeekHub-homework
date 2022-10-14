#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 7
#Write a script which accepts a <number>(int) from user and generates dictionary
#in range <number> where key is <number> and value is <number>*<number>
#    e.g. 3 --> {0: 0, 1: 1, 2: 4, 3: 9}

n = int(input('Please enter any integer: '))
mydict = {}
for i in range(n+1):
    mydict[i] = i*i
print(mydict)
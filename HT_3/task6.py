#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 6
#Write a script to get the maximum and minimum VALUE in a dictionary.


from random import randrange


def random_dict():
    mydict = {}
    n = randrange(10)
    for i in range(n):
        mydict['key' + str(i)] = randrange(100)
    return mydict


r_dict = random_dict()
print(f'Here is the dictionary:\n{r_dict}\n')
print(f'The maximum value is: {r_dict[max(r_dict, key = r_dict.get)]}')
print(f'The minimum value is: {r_dict[min(r_dict, key = r_dict.get)]}')
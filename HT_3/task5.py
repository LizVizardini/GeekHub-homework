#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 5
#Write a script to remove values duplicates from dictionary. Feel free to hardcode your dictionary.

dct = {'foo': 'bar', 'bar': 'buz', 'dou': 'jones', 'USD': 36, 'AUD': 19.2, 'name': 'Tom', 'oof': 'bar', 'oud': 'buz'}
dct2 = {}
print('The old dictionary:\n', dct)
for i, j in dct.items():
    if j not in dct2.values():
        dct2[i] = dct[i]
print('\nThe new dictionary:\n', dct2)
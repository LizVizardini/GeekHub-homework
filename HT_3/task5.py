#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 5
#Write a script to remove values duplicates from dictionary. Feel free to hardcode your dictionary.


from iteration_utilities import duplicates


dct = {'foo': 'bar', 'bar': 'buz', 'dou': 'jones', 'USD': 36, 'AUD': 19.2, 'name': 'Tom', 'oof': 'bar', 'oud': 'buz'}
dct2 = dct.copy()
print('The old dictionary:\n', dct)
for i, j in dct.items():
    if (len(list(dct2.values())) > len(set(list(dct.values())))) & (j in list(duplicates(list(dct.values())))):
        del dct2[i]
print('\nThe new dictionary:\n', dct2)
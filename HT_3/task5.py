#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 5
#Write a script to remove values duplicates from dictionary. Feel free to hardcode your dictionary.

dct = {'foo': 'bar', 'bar': 'buz', 'dou': 'jones', 'USD': 36, 'AUD': 19.2, 'name': 'Tom', 'oof': 'bar', 'oud': 'buz'}
lst = []
new_dict = {}
for i, j in dct.items():
    if j not in lst:
        new_dict[i] = j
        lst.append(j)
print(f'The old dictionary:\n{dct},\n\nThe new one:\n{new_dict}')
exit()

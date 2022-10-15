#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 1
#Write a script that will run through a list of tuples and replace the last value for each tuple.
#The list of tuples can be hard coded. The "replacement" value is entered by the user.
#The number of elements in the tuples must be different.

lst = [(1, 2, 3), (4, 5, 6, 7, 8, 9, 0), (4, 2, 3, 1), (6, 7), ()]
new_lst = []
repl_value = input('Please enter any value: ')
for i in lst:
    if i:
        new_lst.append(i[:-1] + (repl_value,))
    else:
        new_lst.append(i)
print(new_lst)
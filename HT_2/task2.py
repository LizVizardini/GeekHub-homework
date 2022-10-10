#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 2
#Write a script which accepts two sequences of comma-separated colors from user.
#Then print out a set containing all the colors from color_list_1 which are not present in color_list_2.

color_list_1 = set(input('Please write the 1st group of comma-separated colors: ').split(','))
color_list_2 = set(input('Please write the 2nd group of comma-separated colors: ').split(','))
print('\nAll the colors from color_list_1 which are not present in color_list_2: ', color_list_1 - color_list_2)
exit()

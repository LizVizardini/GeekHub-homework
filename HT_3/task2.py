#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 2
#Write a script to remove empty elements from a list.
#    Test list: [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]

lst = [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]
print(list(filter(bool, lst)))

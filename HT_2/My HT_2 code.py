#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 1
#Write a script that accepts a sequence of comma-separated numbers from the user
#and generates a list and a tuple with those numbers.

#CREATING THE LIST
numbers = input('Please write some comma-separated numbers: ')
lst = list(map(float, numbers.split(',')))
print('Here is a list of them:', lst)

#CREATING THE TUPLE
numbers = input('\nPlease write some other comma-separated numbers: ')
tpl = tuple(map(float, numbers.split(',')))
print('Here is a tuple of them:', tpl)


# In[3]:


#TASK 2
#Write a script which accepts two sequences of comma-separated colors from user.
#Then print out a set containing all the colors from color_list_1 which are not present in color_list_2.

color_list_1 = set(input('Please write the 1st group of comma-separated colors: ').split(','))
color_list_2 = set(input('Please write the 2nd group of comma-separated colors: ').split(','))
print('\nAll the colors from color_list_1 which are not present in color_list_2: ', color_list_1 - color_list_2)


# In[4]:


#TASK 3
#Write a script that accepts a <number> from the user
#and prints out a sum of the first <number> positive integers.

n = int(input('Please input a number: '))
sum = 0
for i in range (1, n+1):
    sum += i
print(f'A sum of the first {n} positive integers: {sum}')


# In[5]:


#TASK 4
#Write a script that accepts a <number> from the user and then <number> times asks the user for string input.
#In the end, the script must print out the result of concatenating all <number> strings.

n = int(input('Please input a number: '))
s = ''
for i in range (n):
    s += input('Please enter smth: ')
print(s)


# In[6]:


#TASK 5
#Write a script that accepts a decimal number from the user and converts it to hexadecimal.

print('Hexadecimal: ', format(int(input('Please enter a decimal number: ')), '02x'))


# In[7]:


#TASK 6
#Write a script to check whether a value from user input is contained in a group of values.

lst = input('Please write some of comma-separated values: ').split(',')
input('Enter an element u wanna check: ') in lst


# In[9]:


#TASK 7
#Write a script to concatenate all elements in a list into a string and print it.
#The list must include both strings and integers and must be hard coded.

''.join(str(e) for e in [6, 'cgjj', '0, 9, 8', 7.654])


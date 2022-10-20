#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 3
#Написати функцию <is_prime>, яка прийматиме 1 аргумент - число від 0 до 1000,
#і яка вертатиме True, якщо це число просте і False - якщо ні.


def is_prime(number):
    try:
        if (number == 0) or (number == 1):
            return False
        elif number == 2:
            return True
        else:
            counter = 0
            for i in range (2, number):
                if number % i == 0:
                    counter += 1
            if counter:
                return False
            else:
                return True
    except ValueError:
        print('Try again')
        
        
def human_lang_output():
    if is_prime(int(input('Please enter an integer from 0 to 1000: '))):
        yes_no = ''
    else:
        yes_no = 'not'
    return f'This number is {yes_no} prime!'


#human_lang_output()
#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 5
#Написати функцію <fibonacci>, яка приймає один аргумент і виводить всі числа Фібоначчі, що не перевищують його.


def fibonacci(stop):
    fibonacci_list = [0, 1]
    i = 0
    if stop < 0:
        return []
    elif stop == 0:
        return [0]
    else:
        while True:
            next_element = fibonacci_list[-1] + fibonacci_list[-2]
            if next_element > stop:
                break
            else:
                fibonacci_list.append(next_element)
        return fibonacci_list
            

while True:
    try:            
        print(fibonacci(int(input('Enter an integer number and I`ll return all Fibonacci numbers not exceeding it: '))))
        break
    except ValueError:
        print('The numbers are above the letters on the keyboard. Feel free to use them ;)\n')
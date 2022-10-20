#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 4
#Написати функцію <prime_list>, яка прийматиме 2 аргументи - початок і кінець діапазона, і вертатиме список простих чисел
#всередині цього діапазона. Не забудьте про перевірку на валідність введених даних та у випадку невідповідності - виведіть повідомлення.


from task3 import is_prime


def prime_list(start, end):
    prime_numbers_list = []
    for i in range (start, end + 1):
        if is_prime(i):
            prime_numbers_list.append(i)
    print('\nPrime numbers inside the interval: ', prime_numbers_list)

    
while True:
    try:
        ab = sorted([int(input('Pls enter the 1st number of the interval u wanna check: ')), int(input('And the last: '))])
        prime_list(ab[0], ab[1])
        break
    except ValueError:
        print('\nU have to enter 2 INTEGER NUMBERS that mark the limits of the interval in 2 different inputs')
        print('Try again')
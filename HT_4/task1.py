#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 1
"""Написати функцiю season, яка приймає один аргумент (номер мiсяця вiд 1 до 12)
та яка буде повертати пору року, до якої цей мiсяць належить (зима, весна, лiто або осiнь).
У випадку некоректного введеного значення - виводити відповідне повідомлення."""


def season():
    while True:
        try:
            month = int(input('Please enter an integer number of the month from 1 to 12: '))
            if (month == 1) or (month == 2) or (month == 12):
                res = 'It is a winter month'
                break
            elif (month >= 3) & (month <= 5):
                res = 'It is a spring month'
                break
            elif (month >= 6) & (month <= 8):
                res = 'It is a summer month'
                break
            elif (month >= 9) & (month <= 12):
                res = 'It is an autumn month'
                break
            else:
                print('\nIncorrect number. It must be an integer from 1 to 12. Try again.')
        except ValueError:
            print('\nI SAID INTEGER NUMBER')
    print('\n', res)

    
season()
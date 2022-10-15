#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 5
"""Ну і традиційно - калькулятор. Повинна бути 1 функцiя, яка приймає 3 аргументи - один з яких операцiя, яку зробити!
Аргументи брати від юзера (можна по одному - окремо 2, окремо +, окремо 2; можна всі разом - типу 2 + 2).
Операції що мають бути присутні: +, -, *, /, %, //, **. Не забудьте протестувати з різними значеннями на предмет помилок!"""


def calculator(a, b, operation):
    try:
        a = float(a)
        b = float(b)
        if ('+' in operation) or ('plus' in operation):
            return a + b
        elif ('-' in operation) or ('minus' in operation):
            return a - b
        elif ('*' in operation) or ('x' in operation) or ('multiply' in operation):
            return a * b
        elif (('/' in operation) or (':' in operation) or ('divide' in operation)) & ('remainder' not in operation):
            return a / b
        elif ('%' in operation) or (('remainder' in operation) & ('without' not in operation) & ('no' not in operation)):
            return a % b
        elif ('//' in operation) or (('remainder' in operation) & (('without' in operation) or ('no' in operation))):
            return a // b
        elif ('**' in operation) or ('pow' in operation) or ('power' in operation):
            return a ** b
        else:
            return print('nothing. Are u sure this operation exists?')
    except ValueError:
        print('\n! Do not forget about spases between the numbers and the operation !\n')
    except ZeroDivisionError:
        print('\n! Trying to divide by 0? Want to talk about linear analysis? !\n')


probl = input('Please enter 1-operation problem, make sure to put spaces between the numbers and the operation.\n')
problem = probl.split()
print(probl + ' = ' + str(calculator(problem[0], problem[-1], problem[1:-1])))
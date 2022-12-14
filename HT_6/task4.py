#!/usr/bin/env python
# coding: utf-8

# In[2]:


#TASK 4
"""Створіть функцію <morse_code>, яка приймає на вхід рядок у вигляді коду Морзе та виводить декодоване значення (латинськими літерами).
   Особливості:
    - використовуються лише крапки, тире і пробіли (.- )
    - один пробіл означає нову літеру
    - три пробіли означають нове слово
    - результат може бути case-insensitive (на ваш розсуд - великими чи маленькими літерами).
    - для простоти реалізації - цифри, знаки пунктуацїї, дужки, лапки тощо використовуватися не будуть. Лише латинські літери.
    - додайте можливість декодування сервісного сигналу SOS (...---...)
    Приклад:
    --. . . -.- .... ..- -...   .. ...   .... . .-. .
    результат: GEEKHUB IS HERE"""


def morse_code(your_string):
    morse_dict = { 'SOS' : '...---...', 'A' : '.-', 'B' : '-...', 'C' : '-.-.', 'D' : '-..', 'E' : '.',
                    'F' : '..-.', 'G' : '--.', 'H' : '....', 'I' : '..', 'J' : '.---', 'K' : '-.-',
                    'L' : '.-..', 'M' : '--', 'N' : '-.', 'O' : '---', 'P' : '.--.', 'Q' : '--.-',
                    'R' : '.-.', 'S' : '...', 'T' : '-', 'U' : '..-', 'V' : '...-', 'W' : '.--', 'X' : '-..-',
                    'Y' : '-.--', 'Z' : '--..'}
    lst = your_string.split('   ')
    lst = [item.split() for item in lst]
    result = ''
    for i in lst:
        for j in i:
            result += list(morse_dict.keys())[list(morse_dict.values()).index(j)]
        if i != lst[-1]:
            result += ' '
    return result


try:
    print(morse_code(input('Pls enter smth coded in Morse using ".", "-" (" " between letters and "   " between words)')))
except ValueError:
    print('Incorrect input. Try again :)')
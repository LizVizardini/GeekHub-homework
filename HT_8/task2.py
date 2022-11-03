# TASK 2
"""Написати функцію, яка приймає два параметри: ім'я (шлях) файлу та кількість символів. Файл також додайте в репозиторій.
На екран має бути виведений список із трьома блоками - символи з початку, із середини та з кінця файлу. Кількість символів в блоках - та,
яка введена в другому параметрі. Придумайте самі, як обробляти помилку, наприклад, коли кількість символів більша, ніж є в файлі або,
наприклад, файл із двох символів і треба вивести по одному символу, то що виводити на місці середнього блоку символів?).
Не забудьте додати перевірку чи файл існує."""


def func(n, name = 'text.txt'):
    while True:
        try:
            n = abs(int(n))
            break
        except ValueError:
            n = input('Are you sure that you have entered an integer number? Try again: ')
    try:
        file = open(str(name), "r+")
        file.seek(0)
        data = file.read()
        print(len(data))
        if '\ufeff' in data:
            data = data.replace('\ufeff', '')
        if (len(data) < 3) & (n != 0):
            answer = input('Not enough symbols in the file. If u want to add smth to file, type it here, if not - leave this field empty.')
            if answer:
                data += answer
                file.truncate(0)
                file.write(data)
            else:
                lst = []
                return lst
        if n > len(data):
            print('Error. Maximum number of symbols -', len(data))
            lst = []
        if n == 0:
            lst = []
        if n == len(data):
            lst = [data, data, data]
        if n < len(data):
            lst = [data[:n], data[(len(data) - n) // 2 : (len(data) + n) // 2], data[-n:]]    
        return lst
    except FileNotFoundError:
        if '.' not in name:
            return 'You`ve fogot to write the file extension. Write the file name again without forgetting `.extension`'
        else:
            return 'The file name is incorrect. Please check it and try again.'


name = input('Please enter the file name including the extension: ')
n = input('Please enter the number of the symbols: ')
if name:
    result = func(n, name)
else:
    result = func(n)
if type(result) == list:
    for i in result:
        print('\n\n', i)
else:
    print(result)
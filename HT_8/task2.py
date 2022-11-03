# TASK 2
"""Написати функцію, яка приймає два параметри: ім'я (шлях) файлу та кількість символів. Файл також додайте в репозиторій.
На екран має бути виведений список із трьома блоками - символи з початку, із середини та з кінця файлу. Кількість символів в блоках - та,
яка введена в другому параметрі. Придумайте самі, як обробляти помилку, наприклад, коли кількість символів більша, ніж є в файлі або,
наприклад, файл із двох символів і треба вивести по одному символу, то що виводити на місці середнього блоку символів?).
Не забудьте додати перевірку чи файл існує."""


def func(name, n):
    n = int(n)
    try:
        file = open(str(name), "r")
        data = file.read()
        if len(data) < n:
            n = len(data) // 3
            if n == 0:
                n = 1
        file.seek(0)
        lst = [file.read(n)]
        if '\ufeff' in lst[0]:
            lst[0] = lst[0].replace('\ufeff', '')
        if len(data) == 2:
            if n >= 2:
                file.seek(0)
                lst.append(file.read())
            else:
                lst.append('')
        elif len(data) > 2:
            file.seek((len(data) - n) // 2 + 1)
            lst.append(file.read(n))
        file.seek(len(data) - n)
        lst.append(file.read(n))
        return lst
    except FileNotFoundError:
        if '.' not in name:
            return 'You`ve fogot to write the file extension. Write my name again without forgetting `.extension`'
        else:
            return 'The file name is incorrect. Please check it and try again.'


name = input('Please enter the file name including the extension: ')
n = input('Please enter the number of the symbols: ')

if type(func(name, n)) == list:
    for i in func(name, n):
        print('\n', i)
else:
    print(func(name, n))
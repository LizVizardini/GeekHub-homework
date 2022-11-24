"""
Створити клас Matrix, який буде мати наступний функціонал:
1. __init__ - вводиться кількість стовпців і кількість рядків
2. fill() - заповнить створений масив числами - по порядку. Наприклад:
+────+────+
| 1  | 2  |
+────+────+
| 3  | 4  |
+────+────+
| 5  | 6  |
+────+────+
3. print_out() - виведе створений масив (якщо він ще не заповнений даними - вивести нулі
4. transpose() - перевертає створений масив. Тобто, якщо взяти попередню таблицю, результат буде
+────+────+────+
| 1  | 3  | 5  |
+────+────+────+
| 2  | 4  | 6  |
+────+────+────+
P.S. Всякі там Пандас/Нампай не використовувати - тільки хардкор ;)
P.P.S. Вивід не обов’язково оформлювати у вигляді таблиці - головне, щоб було видно, що це окремі стовпці / рядки
"""


import tabulate


class Matrix:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.matrix = [0] * rows * columns

    def fill(self):
        while True:
            matrix_elements = input('Please input space-separated matrix elements by order: ').split()
            if len(matrix_elements) != len(self.matrix):
                print(f'{len(self.matrix)} elements must be entered. You`ve entered {len(matrix_elements)}. Try again.')
            else:
                break
        matrix_elements = [float(i) for i in matrix_elements]
        matrix_rows = []
        lst = []
        for i in matrix_elements:
            lst.append(i)
            if len(lst) == self.columns:
                matrix_rows.append(lst)
                lst = []
        self.matrix = matrix_rows

    def print_out(self):
        return print(tabulate.tabulate(self.matrix))

    def transpose(self):
        matrix_columns = list(map(list, zip(*self.matrix)))
        self.matrix = matrix_columns
        self.rows = len(matrix_columns)
        self.columns = len(matrix_columns[0])


matrix = Matrix(3, 2)
matrix.fill()
matrix.print_out()
matrix.transpose()
matrix.print_out()
matrix.transpose()
matrix.print_out()
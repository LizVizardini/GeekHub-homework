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


class Matrix:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.matrix = []
        for i in range(rows):
            self.matrix.append([0] * columns)

    def fill(self, *numbers):
        if len(numbers) != self.rows * self.columns:
            raise TypeError(f'fill() takes {self.rows * self.columns} positional arguments but {len(numbers)} were '
                            f'given.')
        matrix_elements = [float(i) for i in numbers]
        matrix_rows = []
        lst = []
        for i in matrix_elements:
            lst.append(i)
            if len(lst) == self.columns:
                matrix_rows.append(lst)
                lst = []
        self.matrix = matrix_rows

    def print_out(self):
        result = ''
        for i in self.matrix:
            result += str(i) + '\n'
        return print(result)

    def transpose(self):
        matrix_columns = list(map(list, zip(*self.matrix)))
        self.matrix = matrix_columns
        self.rows = len(matrix_columns)
        self.columns = len(matrix_columns[0])


matrix = Matrix(3, 2)
matrix.print_out()
matrix.fill(1, 2, 3, 4, 5, 6)
matrix.print_out()
matrix.transpose()
matrix.print_out()
matrix.transpose()
matrix.print_out()
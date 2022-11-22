# Напишіть програму, де клас «геометричні фігури» (Figure) містить властивість color з початковим значенням white і
# метод для зміни кольору фігури, а його підкласи «овал» (Oval) і «квадрат» (Square) містять методи _init_ для завдання
# початкових розмірів об'єктів при їх створенні.


import math


class Figure:
    color = 'white'

    def change_color(self):
        self.color = input('Please enter new color of the figure: ')


class Oval(Figure):

    def __init__(self, R, r):
        self.R = float(R)
        self.r = float(r)

    def perimeter(self):
        P = 4 * (math.pi * self.R * self.r + self.R - self.r) / (self.R + self.r)
        return round(P, 3)

    def area(self):
        S = self.R * self.r * math.pi
        return round(S, 3)

    def figure_description(self):
        return f'It`s a(n) {self.color} oval with a perimeter of {self.perimeter()} and an area of {self.area()}.'


class Square(Figure):

    def __init__(self, a):
        self.a = float(a)

    def perimeter(self):
        P = 4 * self.a
        return round(P, 3)

    def area(self):
        S = self.a ** 2
        return round(S, 3)

    def figure_description(self):
        return f'It`s a(n) {self.color} square with a perimeter of {self.perimeter()} and an area of {self.area()}.'


figure = Figure()
print(figure.color)
figure.color = 'red'
print(figure.color)
print('----------------------------------------------------------------------')

oval = Oval(10, 5)
print(oval.figure_description())
oval.color = 'black'
oval.r = 1 / math.pi
print(oval.figure_description())
print('----------------------------------------------------------------------')

square = Square(5)
print(square.figure_description())
square.color = str(figure.color)
square.a = 10
print(square.figure_description())
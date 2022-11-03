#TASK 1
"""Програма-світлофор.
   Створити програму-емулятор світлофора для авто і пішоходів. Після запуска програми на екран виводиться в лівій половині -
   колір автомобільного, а в правій - пішохідного світлофора. Кожну 1 секунду виводиться поточні кольори. Через декілька ітерацій -
   відбувається зміна кольорів - логіка така сама як і в звичайних світлофорах (пішоходам зелений тільки коли автомобілям червоний).
   Приблизний результат роботи наступний:
      Red        Green
      Red        Green
      Red        Green
      Red        Green
      Yellow     Red
      Yellow     Red
      Green      Red
      Green      Red
      Green      Red
      Green      Red
      Yellow     Red
      Yellow     Red
      Red        Green"""


import time
from time import monotonic as timer


car = ['Red', 'Red', 'Red', 'Red', 'Yellow', 'Yellow', 'Green', 'Green', 'Green', 'Green', 'Yellow', 'Yellow']
human = ['Green', 'Green', 'Green', 'Green', 'Red', 'Red', 'Red', 'Red', 'Red', 'Red', 'Red', 'Red']
while True:
    for i in range(12):
        print('{0:10}  {1}'.format(car[i], human[i]))
        time.sleep(1 - timer() % 1)
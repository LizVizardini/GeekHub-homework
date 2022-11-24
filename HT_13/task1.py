# Створіть клас Car, який буде мати властивість year (рік випуску). Додайте всі необхідні методи до класу,
# щоб можна було виконувати порівняння car1 > car2 , яке буде показувати, що car1 старша за car2.
# Також, операція car1 - car2 повинна повернути різницю між роками випуску.


class Car:
    def __init__(self, year: int = 2022):
        self._year = year
        self._age = 2022 - self._year

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, year):
        self._year = year
        self._age = 2022 - self._year


car1 = Car(2012)
car1 = car1.age
car2 = Car(2017)
car2 = car2.age
print(car1 > car2)
print(car1 - car2)

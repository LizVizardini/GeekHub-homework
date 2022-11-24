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

    def __gt__(self, other):
        return self.age > other.age

    def __lt__(self, other):
        return self.age < other.age

    def __ge__(self, other):
        return self.age >= other.age

    def __le__(self, other):
        return self.age <= other.age

    def __sub__(self, other):
        return self.age - other.age


car1 = Car(2012)
car2 = Car(2017)
print(car1 > car2)
print(car1 < car2)
print(car1 >= car2)
print(car1 <= car2)
print(car1 - car2)

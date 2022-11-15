"""Створити клас Person, в якому буде присутнім метод __init__ який буде приймати якісь аргументи,
які зберігатиме у відповідні змінні.
- Методи, які повинні бути в класі Person - show_age, print_name, show_all_information.
- Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть атрибут profession
(його не має інсувати під час ініціалізації в самому класі) та виведіть його на екран (прінтоніть)"""


class Person:
    def __init__(self, name, age, specialty):
        self.name = name
        self.age = age
        self.specialty = specialty

    def show_age(self):
        return print(f'He/she is {self.age} years old.')

    def print_name(self):
        return print(f'His/her name is {self.name}.')

    def show_all_information(self):
        return print(f'{self.age} years old {self.name} has a diploma by a specialty {self.specialty}.')


person_1 = Person('Zina', 21, 'statistics')
person_2 = Person('Lev', 37, 'web design')
person_1.profession = 'Data Scientist in a big IT company'
person_2.profession = 'SMM-manager in a popular dry cleaners chain'

person_1.print_name()
person_1.show_age()
person_1.show_all_information()
print(f'He/she works as a {person_1.profession}.\n')

person_2.print_name()
person_2.show_age()
person_2.show_all_information()
print(f'He/she works as a {person_2.profession}.')

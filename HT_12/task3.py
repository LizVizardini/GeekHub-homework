class Person:
    i = 0

    def __init__(self):
        Person.i += 1


person_1 = Person()
print(person_1.i)

person_2 = Person()
print(person_2.i)

person_3 = Person()
print(person_3.i)

print(person_2.i)

print(person_1.i)
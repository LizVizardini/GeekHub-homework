# Створіть за допомогою класів та продемонструйте свою реалізацію шкільної бібліотеки (включіть фантазію).
# Наприклад вона може містити класи Person, Teacher, Student, Book, Shelf, Author, Category і.т.д.
# Можна робити по прикладу банкомату з меню, базою даних і т.д.

import datetime
from abc import ABC, abstractmethod
import sqlite3
import tabulate


conn = sqlite3.connect('library.db')
cursor = conn.cursor()
conn.execute('''CREATE TABLE IF NOT EXISTS STUDENT_BOOKS
                (SUBJECT TEXT NOT NULL,
                GRADE INT NOT NULL,
                AMOUNT INT
                )''')
#conn.execute("CREATE UNIQUE INDEX IF NOT EXIST IX_STUDENT_BOOKS ON STUDENT_BOOKS (SUBJECT, GRADE)")
conn.commit()

cursor = conn.cursor()
conn.execute('''CREATE TABLE IF NOT EXISTS TEACHER_BOOKS
                (SUBJECT TEXT NOT NULL,
                GRADE INT NOT NULL,
                AMOUNT INT
                )''')
#conn.execute("CREATE UNIQUE INDEX IF NOT EXIST IX_TEACHER_BOOKS ON TEACHER_BOOKS (SUBJECT, GRADE)")
conn.commit()

student_books = []
for i in range(1, 11):
    ukr = ('Ukrainian language', i, 120)
    eng = ('English', i, 120)
    tech = ('Technologies', i, 120)
    pe = ('Physical education', i, 120)
    ua_liter = ('Ukrainian literature', i, 120)
    if 7 <= i <= 9:
        alg = ('Algebra', i, 120)
        geom = ('Geometry', i, 120)
        student_books.append(alg)
        student_books.append(geom)
    else:
        math = ('Math', i, 120)
        student_books.append(math)
    if i < 8:
        draw = ('Visual art', i, 120)
        music = ('Musical art', i, 120)
        student_books.append(draw)
        student_books.append(music)
    else:
        art = ('Art', i, 120)
        student_books.append(art)
    if i <= 4:
        world = ('I explore the world', i, 120)
    else:
        if i == 5:
            nature = ('Natural science', i, 120)
            student_books.append(nature)
        else:
            if i <= 9:
                health = ('Health basics', i, 120)
                student_books.append(health)
            if i > 6:
                phis = ('Physics', i, 120)
                chem = ('Chemistry', i, 120)
                student_books.append(phis)
                student_books.append(chem)
            bio = ('Biology', i, 120)
            geo = ('Geography', i, 120)
            student_books.append(bio)
            student_books.append(geo)
        for_liter = ('Foreign literature', i, 120)
        hist = ('History', i, 120)
        student_books.append(for_liter)
        student_books.append(hist)
    if i >= 10:
        defense = ('Defense of Ukraine', i, 120)
    student_books.append(ukr)
    student_books.append(eng)
    student_books.append(tech)
    student_books.append(pe)
    student_books.append(ua_liter)

cursor = conn.execute("SELECT * FROM STUDENT_BOOKS")
for i in student_books:
    conn.execute("INSERT OR IGNORE INTO STUDENT_BOOKS VALUES (?, ?, ?)", (i[0], i[1], i[2]))
conn.commit()

teacher_books = [tuple([i[0], i[1], 3]) for i in student_books]

cursor = conn.execute("SELECT * FROM TEACHER_BOOKS")
for i in student_books:
    conn.execute("INSERT OR IGNORE INTO TEACHER_BOOKS VALUES (?, ?, ?)", (i[0], i[1], i[2]))
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS FICTION_BOOKS
                (NAME TEXT NOT NULL,
                AUTHOR TEXT NOT NULL,
                AMOUNT INT
                )''')
conn.commit()
fiction_books = {'Іван Котляревський': ['ЕНЕЇДА', 'НАТАЛКА-ПОЛТАВКА'], 'Тарас Шевченко': ['КОБЗАР'],
                 'Пантелеймон Куліш': ['ЧОРНА РАДА']}
cursor = conn.execute("SELECT * FROM FICTION_BOOKS")
for key in fiction_books:
    for i in fiction_books[key]:
        conn.execute("INSERT OR IGNORE INTO FICTION_BOOKS VALUES (?, ?, ?)", (i, key, 5))
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS ACTIONS
                (FULL_NAME TEXT NOT NULL,
                POSITION TEXT NOT NULL,
                ACTION TEXT,
                DATE TEXT
                )''')
conn.commit()


class Books(ABC):
    subjects = list(set([row[0] for row in student_books]))

    def get_subject_name(self):
        print('Please choose a subject: ')
        for subject_number in range(len(self.subjects)):
            print(f'({subject_number + 1}) To choose the {self.subjects[subject_number]} book - enter '
                  f'{subject_number + 1}')
        entered_number = int(input()) - 1
        subject_name = self.subjects[entered_number]
        return subject_name

    def is_sb_accessible(self, grade, subject_name):
        subject_books = [i for i in student_books if i[0] == subject_name]
        grade_number = int(''.join(filter(str.isdigit, grade)))
        if grade_number in [i[1] for i in subject_books]:
            return grade_number
        else:
            return False

    def is_sb_available(self, subject, grade):
        available_now = 0
        cursor = conn.execute("SELECT * FROM STUDENT_BOOKS")
        for row in cursor:
            if (row[0] == subject) & (row[1] == grade):
                available_now = int(row[2])
        conn.commit()
        return available_now

    def remove_sb_from_library(self, subject, grade, available):
        if not available:
            print('Sorry, these books are currently out of stock(')
            return False
        else:
            conn.execute("UPDATE STUDENT_BOOKS set AMOUNT = ? where SUBJECT = ? and GRADE = ?",
                         (available - 1, subject, grade))
            conn.commit()
            return True

    def add_to_action(self, name, position, subject, put_or_get):
        conn.execute("INSERT INTO ACTIONS VALUES (?, ?, ?, ?)",
                     (name, position, put_or_get + subject, datetime.datetime.now().strftime("%d/%m/%Y")))
        conn.commit()

    def get_student_book(self, name, position):
        result = False
        subject_name = self.get_subject_name()
        grade_number = self.is_sb_accessible(position, subject_name)
        if grade_number:
            available_now = self.is_sb_available(subject_name, grade_number)
            result = self.remove_sb_from_library(subject_name, grade_number, available_now)
            if result:
                self.add_to_action(name, position, subject_name, '-')
            else:
                print('Unfortunately, these student`s books are currently unavailable.')
        else:
            print('You can get student`s books only for the subjects you are studying this year.')
        return result

    def is_tb_accessible(self, subject_name, grade):
        subject_books = [i for i in teacher_books if i[0] == subject_name]
        grade_number = int(''.join(filter(str.isdigit, grade)))
        if grade_number in [i[1] for i in subject_books]:
            return grade_number
        else:
            return False

    def is_tb_available(self, subject, grade):
        available_now = 0
        cursor = conn.execute("SELECT * FROM TEACHER_BOOKS")
        for row in cursor:
            if (row[0] == subject) & (row[1] == grade):
                available_now = int(row[2])
        conn.commit()
        return available_now

    def remove_tb_from_library(self, subject, grade, available):
        if not available:
            print('Sorry, these books are currently out of stock(')
            return False
        else:
            conn.execute("UPDATE TEACHER_BOOKS set AMOUNT = ? where SUBJECT = ? and GRADE = ?",
                         (available - 1, subject, grade))
            conn.commit()
            return True

    def get_teacher_book(self, name, position):
        result = False
        grade = input('Which grade do you need a study guide for? ')
        subject_name = self.get_subject_name()
        grade_number = self.is_tb_accessible(grade, subject_name)
        if grade_number:
            available_now = self.is_tb_available(subject_name, grade_number)
            result = self.remove_tb_from_library(subject_name, grade_number, available_now)
            if result:
                subject_name = subject_name + ', ' + str(grade_number)
                self.add_to_action(name, position, subject_name, '-')
            else:
                print('Unfortunately, these teacher`s books are currently unavailable.')
        else:
            print('Such a subject is not studied in this grade. Are you sure you are a teacher?')
        return result

    def fiction_book_check(self):
        now_available, counter = 0, 0
        author = input('Please enter the author of the book: ').title()
        book_name = input('Please enter the name of the book: ').upper()
        cursor = conn.execute("SELECT * FROM FICTION_BOOKS")
        for row in cursor:
            if (row[0] == book_name) & (row[1] == author):
                counter += 1
                now_available = row[2]
                if now_available:
                    now_available -= 1
                else:
                    print('Sorry, this book is currently unavailable.')
        conn.commit()
        if not counter:
            print('The library does not have this book')
        new_values = tuple([book_name, author, now_available])
        return new_values

    def get_fiction_book(self, name, position):
        new_values = self.fiction_book_check()
        if new_values[2]:
            conn.execute("UPDATE FICTION_BOOKS set AMOUNT = ? where NAME = ? and AUTHOR = ?",
                         (new_values[2], new_values[0], new_values[1]))
            conn.commit()
            self.add_to_action(name, position, new_values[0], '-')
            return True
        else:
            return False

    @abstractmethod
    def book_picture(self):
        print('████████████████████████████████████████')
        print('████████████░▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄░░░░████████')
        print('███████████░▄████████████████▄▄░▀███████')
        print('██████████░▄████████████████████░▀██████')
        print('█████████░▄█████████████████████▄░██████')
        print('████████░▄███████████████████████▄░█████')
        print('███████░░█████████████████████████░░████')
        print('██████▀░█████████████████████████▀░░▀███')
        print('█████▀░████████████████████████▀░░░░░▀██')
        print('████▀░▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀░░░░░░░░▀█')
        print('███░▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄░█')
        print('██░▄█▀░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░███')
        print('█▀░█▀░░░░░▄▄▄▄▄▄▄▄▄▄▄░░░░░░░░░░░░░░░████')
        print('█▄░█░░░░░░▀█▀▀▀▀▀▀██▀░░░░░░░░░░░░░░░████')
        print('██░▀█░░░░░░█░░░░░░██░░░░░░░░░░░░░░░░░███')
        print('██▄░▀█▄▄▄▄██░░░░░░██▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄███')
        print('████░░░░▄██░░░░░░▄█░░░░░░░░░░░░░░░░░░░░█')
        print('████████▀▀░░░░░░▄███████████████████████')
        print('██████▄▄░░░░░░▄█████████████████████████')
        print('████████████████████████████████████████')

    def return_student_book(self, name, position):
        amount, counter = 0, 0
        subject_name = self.get_subject_name()
        grade_number = int(''.join(filter(str.isdigit, position)))
        cursor = conn.execute("SELECT * FROM STUDENT_BOOKS")
        for row in cursor:
            if (row[0] == subject_name) & (row[1] == grade_number):
                counter += 1
                conn.execute("UPDATE STUDENT_BOOKS set AMOUNT = ? where SUBJECT = ? and GRADE = ?",
                             (row[2] + 1, subject_name, grade_number))
        if not counter:
            conn.execute("INSERT INTO STUDENT_BOOKS VALUES (?, ?, ?)", (subject_name, grade_number, 1))
        self.add_to_action(name, position, subject_name, '+')

    def return_teacher_book(self, name, position, grade):
        amount, counter = 0, 0
        subject_name = self.get_subject_name()
        grade_number = int(''.join(filter(str.isdigit, grade)))
        cursor = conn.execute("SELECT * FROM TEACHER_BOOKS")
        for row in cursor:
            if (row[0] == subject_name) & (row[1] == grade_number):
                counter += 1
                conn.execute("UPDATE TEACHER_BOOKS set AMOUNT = ? where SUBJECT = ? and GRADE = ?",
                             (row[2] + 1, subject_name, grade_number))
        if not counter:
            conn.execute("INSERT INTO TEACHER_BOOKS VALUES (?, ?, ?)", (subject_name, grade_number, 1))
        self.add_to_action(name, position, subject_name, '+')

    def fiction_book_return_check(self):
        now_available, counter = 0, 0
        author = input('Please enter the author of the book: ').title()
        book_name = input('Please enter the name of the book: ').upper()
        cursor = conn.execute("SELECT * FROM FICTION_BOOKS")
        for row in cursor:
            if (row[0] == book_name) & (row[1] == author):
                counter += 1
                now_available = row[2]
        conn.commit()
        now_available += 1
        new_values = tuple([book_name, author, now_available])
        return new_values

    def return_fiction_book(self, name, position):
        new_values = self.fiction_book_check()
        if new_values[2] != 1:
            conn.execute("UPDATE FICTION_BOOKS set AMOUNT = ? where NAME = ? and AUTHOR = ?",
                         (new_values[2], new_values[0], new_values[1]))
        else:
            conn.execute("INSERT INTO FICTION_BOOKS VALUES (?, ?, ?)", new_values)
            conn.commit()
        self.add_to_action(name, position, new_values[0], '+')

    def show_books_catalogue(self, position, book_type):
        catalogue = []
        if book_type == 'edu':
            header = ('Subject', 'Grade', 'How many')
            if position == 'teacher':
                subject = self.get_subject_name()
                cursor = conn.execute("SELECT * FROM TEACHER_BOOKS")
                catalogue = [i for i in cursor if i[0] == subject]
            else:
                grade_number = int(''.join(filter(str.isdigit, position)))
                cursor = conn.execute(f"SELECT * FROM STUDENT_BOOKS")
                catalogue = [i for i in cursor if i[1] == grade_number]
        else:
            header = ('Name', 'Author', 'How many')
            cursor = conn.execute("SELECT * FROM FICTION_BOOKS")
            catalogue = [i for i in cursor]
        print(tabulate.tabulate([header] + catalogue))


class Person(Books):

    def get_name(self):
        name = ''
        while not name:
            name = input('Please enter your full name: ').title()
        return name

    def get_position(self):
        position = input('If you study here - enter in which grade, if you are teacher - leave this field empty: ')
        if not position:
            position = 'teacher'
        return position

    def choose_action(self):
        while True:
            action = input(
                'If you would like to get a book - enter `-`,\nto return a book - enter `+`,\nto see the '
                'books catalogue - enter `=`: ')
            if (len(action) != 1) or (action not in '+-='):
                print('You have to enter only: +, - or =')
            else:
                break
        return action

    def choose_book_type(self):
        book_type = input(
            'If you`d like to get/return/see an educational book(s) - enter something, if fiction - leave this field '
            'empty: ')
        if book_type:
            book_type = 'edu'
        else:
            book_type = 'fic'
        return book_type

    def book_picture(self):
        print('Successful!')
        super().book_picture()


class Student(Person):

    def get_book(self, name, position, book_type):
        if book_type == 'edu':
            if self.get_student_book(name, position):
                self.book_picture()
        else:
            if self.get_fiction_book(name, position):
                self.book_picture()

    def return_book(self, name, position, book_type):
        if book_type == 'edu':
            self.return_student_book(name, position)
            print('Successful!')
        else:
            if self.return_fiction_book(name, position):
                print('Successful!')


class Teacher(Person):

    def get_book(self, name, position, book_type):
        if book_type == 'edu':
            if self.get_teacher_book(name, position):
                self.book_picture()
        else:
            if self.get_fiction_book(name, position):
                self.book_picture()

    def return_book(self, name, position, book_type):
        if book_type == 'edu':
            self.return_teacher_book(name, position)
            print('Successful!')
        else:
            if self.return_fiction_book(name, position):
                print('Successful!')


class Start:

    def __init__(self):
        self.student = None
        self.teacher = None
        self.person = Person()

    def start(self):
        position = self.person.get_position()
        if position == 'teacher':
            self.teacher = Teacher()
            name = self.teacher.get_name()
            action = self.teacher.choose_action()
            book_type = self.teacher.choose_book_type()
            if action == '+':
                self.teacher.return_book(name, position, book_type)
            if action == '-':
                self.teacher.get_book(name, position, book_type)
            if action == '=':
                self.teacher.show_books_catalogue(position, book_type)
        else:
            self.student = Student()
            name = self.student.get_name()
            action = self.student.choose_action()
            book_type = self.student.choose_book_type()
            if action == '+':
                self.student.return_book(name, position, book_type)
            if action == '-':
                self.student.get_book(name, position, book_type)
            if action == '=':
                self.student.show_books_catalogue(position, book_type)


if __name__ == '__main__':
    print('WELCOME TO THE LIBRARY!')
    main_class = Start()
    main_class.start()
    conn.close()
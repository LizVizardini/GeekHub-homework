"""Створити клас Calc, який буде мати атрибут last_result та 4 методи. Методи повинні виконувати математичні операції
з 2-ма числами, а саме додавання, віднімання, множення, ділення.
- Якщо під час створення екземпляру класу звернутися до атрибута last_result він повинен повернути пусте значення.
- Якщо використати один з методів - last_result повинен повернути результат виконання ПОПЕРЕДНЬОГО методу.
    Example:
    last_result --> None
    1 + 1
    last_result --> None
    2 * 3
    last_result --> 2
    3 * 4
    last_result --> 6
    ...
- Додати документування в клас (можете почитати цю статтю:
https://realpython.com/documenting-python-code/ )"""


class Calc:
    """

    Creating class 'Calc'

    """
    last_result = None  # Creating a class attribute 'last_result'

    def plus(self, a, b):
        """

        Args:
            a: the 1st number
            b: the 2nd number

        Returns:
            the sum of args

        """
        self.last_result = None  # Assigning the previous value to the attribute
        return a + b

    def minus(self, a, b):
        """

        Args:
            a: the 1st number
            b: the 2nd number

        Returns:
            the difference of args

        """
        self.last_result = self.plus(a, b)  # Assigning the previous value to the attribute
        return a - b

    def multiply(self, a, b):
        """

        Args:
            a: the 1st number
            b: the 2nd number

        Returns:
            the product of the args

        """
        self.last_result = self.minus(a, b)  # Assigning the previous value to the attribute
        return a * b

    def divide(self, a, b):
        """

        Args:
            a: the 1st number
            b: the 2nd number

        Returns:
            fraction from division of args

        """
        self.last_result = self.multiply(a, b)  # Assigning the previous value to the attribute
        return a / b


calc_1 = Calc()  # Creating the instance of the class
print(calc_1.last_result)  # Printing the attribute value
print(calc_1.plus(1, 1))  # Printing the 'plus' method result
print(calc_1.last_result)  # The attribute value after calling the 'plus' method (returns the previous method's result)
print(calc_1.minus(2, 1))  # Printing the 'minus' method result
print(calc_1.last_result)  # The attribute value after calling the 'minus' method (returns the previous method's result)
print(calc_1.multiply(2, 2))  # Printing the 'multiply' method result
print(calc_1.last_result)  # The attribute value after calling 'multiply' method (returns the previous method's result)
print(calc_1.divide(3, 2))  # Printing the 'divide' method result
print(calc_1.last_result)  # The attribute value after calling 'divide' method (returns the previous method's result)

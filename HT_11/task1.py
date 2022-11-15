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
    last_result, new_result = None, None  # Creating a class attributes 'last_result' and 'new_result'

    def plus(self, a, b):
        """

        Args:
            a: the 1st number
            b: the 2nd number

        Returns:
            the sum of args or the last result

        """

        self.new_result = a + b
        return self.new_result

    def minus(self, a, b):
        """

        Args:
            a: the 1st number
            b: the 2nd number

        Returns:
            the difference of args

        """

        self.last_result = self.new_result  # Assigning the previous value to the attribute
        self.new_result = a - b
        return self.new_result

    def multiply(self, a, b):
        """

        Args:
            a: the 1st number
            b: the 2nd number

        Returns:
            the product of the args

        """
        self.last_result = self.new_result  # Assigning the previous value to the attribute
        self.new_result = a * b
        return self.new_result

    def divide(self, a, b):
        """

        Args:
            a: the 1st number
            b: the 2nd number

        Returns:
            fraction from division of args

        """
        self.last_result = self.new_result  # Assigning the previous value to the attribute
        self.new_result = a / b
        return self.new_result


calc_1 = Calc()  # Creating the instance of the class
print(calc_1.last_result)  # Printing the attribute value

calc_1.plus(1, 1)  # The 'plus' method
print(calc_1.last_result)  # The attribute value after calling the 'plus' method (returns the previous method's result)

calc_1.minus(3, 2)  # The 'minus' method
print(calc_1.last_result)  # The attribute value after calling the 'minus' method (returns the previous method's result)

calc_1.multiply(2, 2)  # Printing the 'multiply' method result
print(calc_1.last_result)  # The attribute value after calling 'multiply' method (returns the previous method's result)

calc_1.divide(6, 2)  # Printing the 'divide' method result
print(calc_1.last_result)  # The attribute value after calling 'divide' method (returns the previous method's result)

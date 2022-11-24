# Створіть клас, який буде повністю копіювати поведінку list, за виключенням того, що індекси в ньому мають починатися
# з 1, а індекс 0 має викидати помилку (такого ж типу, яку кидає list якщо звернутися до неіснуючого індексу).


class FirstIndexList:
    def __init__(self, lst):
        self._lst = lst

    def __getitem__(self, index):
        if index < 0:
            index += len(self._lst) + 1
        if not index:
            raise IndexError('list index out of range')
        return self._lst[index - 1]


some_list = FirstIndexList([1, 2, 3, 4, 5])
print(some_list[1])
print(some_list[-1])
print(some_list[-2])
print(some_list[0])
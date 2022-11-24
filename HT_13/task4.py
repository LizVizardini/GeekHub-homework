# Створіть клас, який буде повністю копіювати поведінку list, за виключенням того, що індекси в ньому мають починатися
# з 1, а індекс 0 має викидати помилку (такого ж типу, яку кидає list якщо звернутися до неіснуючого індексу).


class FirstIndexList:
    _lst = []

    @property
    def lst(self):
        return self._lst

    @lst.setter
    def lst(self, lst):
        self._lst = lst

    def __getitem__(self, index):
        if index < 0:
            index += len(self._lst) + 1
        if not index:
            raise IndexError('list index out of range')
        return self._lst[index - 1]


def test(iterable_sequence):
    some_list = FirstIndexList()
    some_list.lst = iterable_sequence

    print(some_list[1])
    print(some_list[-1])
    print(some_list[-2])
    print('')


test([1, 2, 3, 4, 5])
test(tuple([1, 2, 3, 4, 5]))
test(range(1, 6))
test('12345')
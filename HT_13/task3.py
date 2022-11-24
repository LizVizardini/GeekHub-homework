"""
Реалізуйте класс Transaction. Його конструктор повинен приймати такі параметри:
- amount - суму на яку було здійснено транзакцію
- date - дату переказу
- currency - валюту в якій було зроблено переказ (за замовчуванням USD)
- usd_conversion_rate - курс цієї валюти до долара (за замовчуванням 1.0)
- description - опис транзакції (за дефолтом None)
Усі параметри повинні бути записані в захищені (_attr) однойменні атрибути.
Доступ до них повинен бути забезпечений лише на читання та за допомогою механізму property.
При чому якщо description дорівнює None, то відповідне property має повертати рядок "No description provided".
Додатково реалізуйте властивість usd, що має повертати суму переказу у доларах (сума * курс)
"""

import datetime


class Transaction:
    def __init__(self, amount, date, currency='USD', usd_conversion_rate=1.0, description=None):
        self._amount = amount
        self._date = date
        self._currency = currency
        self._usd_conversion_rate = usd_conversion_rate
        self._description = description

    @property
    def amount(self):
        return round(self._amount, 2)

    @property
    def date(self):
        return self._date

    @property
    def currency(self):
        return self._currency

    @property
    def usd_conversion_rate(self):
        return self._usd_conversion_rate

    @property
    def description(self):
        if self._description is None:
            return 'No description provided'
        else:
            return self._description

    @property
    def usd(self):
        if self._currency.upper() != 'USD':
            result = round(self._amount, 2)
        else:
            result = round(self._amount * self._usd_conversion_rate, 2)
        return result


def show_all_info(transaction):
    print('\n' + '↓' * 45)
    print('Amount:', transaction.amount)
    print('Date:', transaction.date)
    print('Currency:', transaction.currency)
    print('USD conversion rate:', transaction.usd_conversion_rate)
    print('Description:', transaction.description)
    print('Amount in USD:', transaction.usd)
    print('↑' * 45)


transaction1 = Transaction(100, datetime.datetime.now().strftime("%d/%m/%Y"))
show_all_info(transaction1)

transaction2 = Transaction(3703.80, datetime.datetime.now().strftime("%d/%m/%Y"), 'UAH', 0.027, 'Second transaction')
show_all_info(transaction2)
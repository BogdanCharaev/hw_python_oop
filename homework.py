from datetime import datetime as dt, timedelta

DATE_FORMAT = '%d.%m.%Y'


class Record:
    """Класс Record принимает запись с параметрами: кол-во, коммент, дата."""
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date:
            self.date = dt.strptime(date, DATE_FORMAT).date()
        else:
            self.date = now_formated()

    def __str__(self):
        return (f'amount = {self.amount}, '
                f'comment = {self.comment}, '
                f'date = {self.date}')


def now_formated():
    """Форматирует дату."""
    return dt.now().date()


def abs_converter(number):
    """Берет число по модулю."""
    return abs(number)


def format_two_decimal_places(number):
    """
    Форматирует число до 2х знаков после запятой
    """
    return format(number, '0.2f')


def currency_converter(number, currency):
    """Конвертирует число number по курсу currency."""
    return number / currency


def abs_and_two_decimal_places(number):
    """
    Берет число по модулю и форматирует результат до 2х знаков
    после запятой.
    """
    return format_two_decimal_places(abs_converter(number))


class Calculator:
    """
    Содержит базовые функции для добавления записей, подсчета лимита

    """
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Сохраняет новую запись."""
        self.records.append(record)

    def get_today_stats(self):
        """Считает статы сегодня."""
        today_date = now_formated()
        return sum(
            record.amount for record in self.records
            if record.date == today_date
        )

    def get_limit_remained(self):
        """Считает сегодняшний лимит."""
        return self.limit - self.get_today_stats()

    def get_week_stats(self):
        """Показывает расход за неделю"""
        delta_date = (dt.now() - timedelta(days=7)).date()
        now_date = dt.now().date()
        return sum(
            record.amount for record in self.records
            if now_date >= record.date >= delta_date
        )


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        """Показывает остаток по лимиту каллорий на сегодня."""
        limit_remained = self.get_limit_remained()
        if limit_remained > 0:
            return(f'Сегодня можно съесть что-нибудь ещё, '
                   f'но с общей калорийностью не более {limit_remained} кКал')
        return('Хватит есть!')


class CashCalculator(Calculator):

    EURO_RATE = 70.99
    USD_RATE = 60.99

    def get_today_cash_remained(self, currency):
        """
        Определяет, сколько ещё денег можно потратить сегодня
        в рублях, долларах или евро
        """

        currences = {
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
            'rub': (1, 'руб')
        }

        if currency not in currences:
            return 'Валюта не представлена в списке валют.'
        limit_remained = self.get_limit_remained()

        if limit_remained == 0:
            return 'Денег нет, держись'

        rate, name = currences[currency]
        limit_remained = currency_converter(limit_remained, rate)

        if limit_remained > 0:
            limit_remained = format_two_decimal_places(limit_remained)
            return f'На сегодня осталось {limit_remained} {name}'

        limit_remained = abs_and_two_decimal_places(limit_remained)
        return f'Денег нет, держись: твой долг - {limit_remained} {name}'

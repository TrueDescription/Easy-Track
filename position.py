import json
from typing import List

from option_transaction import OptionTransaction
from transaction import *
import datetime
import pandas as pd


class Position:
    def __init__(self, name: str, ticker: str, transactions: List[Transaction], native_currency: str, date: datetime,
                 option=False):
        self.option = option
        self.date = date
        self.native_currency = native_currency
        self.name = name
        self.transactions = transactions
        self.ticker = ticker
        self.shares = 0
        self.cost = 0
        self.dividends = 0
        self.info = yf.Ticker(self.ticker).info
        self.div_history = {}
        self.currency = yf.Ticker(ticker).info['currency']
        div_actions = []
        for transaction in transactions:
            self.add_transaction(transaction, False)
        if self.transactions is not None:
            self.transactions.sort(key=lambda x: x.date)
        self.dividends_updater()

    def add_transaction(self, transaction: Transaction, flag=True):
        if self.transactions is None:
            self.transactions = [transaction]
        else:
            self.transactions.append(transaction)
        if type(transaction) == OptionTransaction:
            self.add_transaction_option(transaction, transaction.transaction_identifier)
            return
        if transaction.transaction_identifier == 'buy':
            self.shares += transaction.shares
            self.cost += transaction.cost_per_share * transaction.shares
            # figure out divedends
            # self.dividends_edit(transaction.shares, transaction.date, transaction.transaction_identifier)
            if flag:
                self.dividends_updater()
            return
            # if sell
        self.shares -= transaction.shares
        self.cost -= transaction.cost_per_share * transaction.shares
        # figure out divedends
        # self.dividends_edit(transaction.shares, transaction.date, transaction.transaction_identifier)
        if flag:
            self.dividends_updater()

    def add_transaction_option(self, transaction: OptionTransaction, transaction_identifier: str):
        self.shares += transaction.contract_amount * 100
        self.cost += self.shares * transaction.premium_per_share

    def remove_transaction(self, transaction):
        self.transactions.remove(transaction)
        self.dividends_updater()
        if transaction.transaction_identifier == 'buy':
            self.shares -= transaction.shares
            self.cost -= transaction.cost_per_share * transaction.shares
            return
        self.shares += transaction.shares
        self.cost += transaction.cost_per_share * transaction.shares
        return

    def dividends_updater(self):
        if self.option:
            return
        if not self.transactions:
            return
        history = yf.Ticker(self.ticker)
        history.history(start=self.transactions[0].date)
        div_history = history.dividends
        number_of_shares = 0
        self.div_history = {}
        self.dividends = 0
        i = 0
        for transaction in self.transactions:
            if transaction.transaction_identifier == 'buy':
                number_of_shares += transaction.shares
            if transaction.transaction_identifier == 'sell':
                number_of_shares -= transaction.shares
            while i < len(div_history.index):
                if transaction.date < div_history.index[i].to_pydatetime():
                    dividend = number_of_shares * div_history[i]
                    self.dividends += dividend
                    if div_history.index[i].to_pydatetime() in self.div_history.keys():
                        self.div_history[div_history.index[i].to_pydatetime()] += dividend
                    else:
                        self.div_history[div_history.index[i].to_pydatetime()] = dividend
                i += 1

            i = 0

    def graph(self):
        data = {}
        for transaction in self.transactions:
            res = transaction.graph()
            if isinstance(transaction, OptionTransaction):
                pass
            if res[0] in data.keys():
                data[res[0]].append(res)
            else:
                data[res[0]] = [res]
        sorted_keys = list(data.keys())
        sorted_keys.sort()
        points = []
        summation = 0
        #ticker = yf.Ticker(self.ticker)
        for key in sorted_keys:
            transactions = data[key]
            for transaction in transactions:
                if transaction[2].transaction_identifier == 'buy':
                    summation += transaction[1]
                elif transaction[2].transaction_identifier == 'sell':
                    summation -= transaction[1]
            points.append((key, summation))
        return points




def convert_currency(currency_from: str, currency_to: str, amount: float) -> float:
    if currency_from == currency_to:
        return amount
    read = json.loads(convert(currency_from, currency_to, amount))
    return float(read['amount'])


def get_current_price(symbol) -> float:
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

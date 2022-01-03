from typing import List

from transaction import *
import datetime
import pandas as pd


class Position:
    def __init__(self, name: str, ticker: str, transactions: List[Transaction]):
        self.name = name
        self.transactions = []
        self.ticker = ticker
        self.shares = 0
        curr_shares = 0
        self.cost = 0
        self.dividends = 0
        self.div_history = {}
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

from datetime import datetime

from google_currency import convert
import yfinance as yf

from transaction import Transaction


class OptionTransaction(Transaction):
    """
    Class representing a single transaction containing all pertaining information
    """

    def __init__(self, ticker: str, name: str, transaction_identifier: str, date: datetime, contract_amount: int,
                 commission: float, notes: str, premium_per_share: float, break_even: float, expiry_date: datetime,
                 strike_price: float):
        """

        :param ticker:
        :param name:
        :param transaction_identifier:
        :param date:
        :param contract_amount:
        :param commission:
        :param notes:
        :param premium_per_share:
        :param break_even:
        :param expiry_date:
        :param strike_price:
        """
        super().__init__(ticker, name, transaction_identifier, date, contract_amount, commission, notes,
                         premium_per_share)
        self.strike_price = strike_price
        self.expiry_date = expiry_date
        self.break_even = break_even
        self.premium_per_share = premium_per_share
        self.notes = notes
        self.commission = commission
        self.contract_amount = contract_amount
        self.date = date
        self.transaction_identifier = transaction_identifier
        self.name = name
        self.ticker = ticker

    def edit_shares_option(self, contract_amount: int, premium_per_share: float, break_even: float,
                           expiry_date: datetime, strike_price: float):
        self.contract_amount = contract_amount
        self.premium_per_share = premium_per_share
        self.break_even = break_even
        self.expiry_date = expiry_date
        self.strike_price = strike_price

    def edit_shares(self, shares: float, cost_per: float, commission: float, date: datetime, transaction_identifier: str
                    , notes: str):
        self.total_cost = cost_per * shares
        self.shares = shares
        self.date = date
        self.curr_value = (yf.Ticker(self.ticker).history(period='1d')['Close'][0]) * shares
        self.notes = notes
        self.commission = commission
        update = False
        if self.transaction_identifier != transaction_identifier:
            update = True
        self.transaction_identifier = transaction_identifier

    def graph(self):
        return self.date, self.contract_amount * 100, self

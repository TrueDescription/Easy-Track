from datetime import datetime

from google_currency import convert
import yfinance as yf


class OptionTransaction:
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

    def edit_shares(self, transaction_identifier: str, date: datetime, contract_amount: int,
                    commission: float, notes: str, premium_per_share: float, break_even: float, expiry_date: datetime,
                    strike_price: float):
        pass

    def graph(self):
        return self.date, self.contract_amount * 100, self

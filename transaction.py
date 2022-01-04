from datetime import datetime

from google_currency import convert
import yfinance as yf


class Transaction:
    """
    Class representing a single transaction containing all pertaining information
    """

    def __init__(self, ticker: str, name: str, transaction_identifier: str, date: datetime, shares: float,
                 commission: float,
                 notes: str, cost_per_share: float):
        """

        :param ticker: Stock ticker
        :param name: Stock name
        :param transaction_identifier: identifier for buy sell or dividend transaction
        :param date: date of transaction as a string
        :param shares: number of shares under a transaction
        :param commission: commission on transaction paid
        :param notes: extra notes on transaction
        :param curr_value: market value in chosen currency
        """
        self.cost_per_share = cost_per_share
        self.total_cost = cost_per_share * shares
        self.shares = shares
        self.date = date
        self.notes = notes
        self.name = name
        self.curr_value = 0
        self.ticker = ticker
        self.commission = commission
        self.transaction_identifier = transaction_identifier

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
        return self.date, self.shares, self

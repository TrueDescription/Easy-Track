from typing import List
from position import *
from transaction import *
import yfinance as yf
from google_currency import convert


class UserData:
    """
    Class data represents the data of previous investment history
    """

    def __init__(self, username: str, start_date: datetime):
        """

        :param username: name of user
        :param start_date: string representing the start month and year of investments; eg. '2019-1-1'
        :param portfolio_holdings_history: list representing the previous holdings of the portfolio
        :param curr_investments: list of open positions in the market
        """
        self.start_date = start_date  # Start of the x-axis
        self.positions = {}
        self.curr_investments = []  # Current open positions
        self.currency = 'cad'
        # Pull file data
        """
        try:
            user_file = open(username + 'data.txt', 'x')
            user_file.write('symbol, name, type, date, shares, commission, notes, current value, notes, cost_per_share')
        except IOError:
            user_file = open(username + 'data.txt', 'r')
            user_file.readline()
            for line in user_file:
                line_data = line.split(',')
                new_t = Transaction(line_data[0], line_data[1], line_data[2],
                                    datetime.strptime(line_data[3], '%Y-%m-%d'), float(line_data[4]),
                                    float(line_data[5]), line_data[6], float(line_data[7]))
                if line_data[0] in self.positions.keys():
                    self.positions[line_data[0]].add_transaction(new_t, False)
                else:
                    self.positions[line_data[0]] = Position(line_data[1], line_data[0], [new_t])
        for key in self.positions.keys():
            self.positions[key].dividends_updater()
            if self.positions[key].shares > 0:
                self.curr_investments.append(self.positions[key])
        """
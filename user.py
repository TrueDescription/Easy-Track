from main import *
import yfinance as yf
from google_currency import convert
import json

from option_transaction import OptionTransaction


class User:
    """
    Class representing User data such as Name and Net-worth
    """

    def __init__(self, username: str, start_date: datetime, currency: str):
        self.user_data = UserData(username, start_date)
        self.portfolio_mv = 0
        self.cash = 0
        self.total_deposits = 0
        self.dividends = 0
        self.history = []
        self.mv_history = {}
        self.currency = currency

    def make_transaction(self, ticker: str, name: str, transaction_identifier: str, date: datetime, shares: float,
                         commission: float, notes: str, cost_per_share: float):
        new_t = Transaction(ticker, name, transaction_identifier, date, shares, commission, notes, cost_per_share)
        if ticker in self.user_data.positions.keys():
            self.user_data.positions[ticker].add_transaction(new_t)
            self.update_mv()
            """if date in self.mv_history.keys():
                self.mv_history[date] += 
            else:
                self.mv_history[date] = self.portfolio_mv"""
            return
        new_position = Position(name, ticker, [], self.currency, date)
        new_position.add_transaction(new_t)
        self.user_data.positions[ticker] = new_position
        self.update_mv()
        # self.mv_history[date] = self.portfolio_mv
        return new_t

    def remove_transaction(self, transaction: Transaction):
        self.user_data.positions[transaction.ticker].remove_transaction(transaction)
        self.update_mv()

    def remove_position(self, position: Position):
        self.user_data.positions.pop(position.ticker)
        self.update_mv()

    def avg_roi(self):
        for key in self.user_data.positions:
            pass

    def update_mv(self):
        new_mv = 0
        dividends = 0
        for position in self.user_data.positions.values():
            new_mv += convert_currency(position.currency, self.currency,
                                       (position.shares * get_current_price(position.ticker)) + position.dividends)
            dividends += position.dividends
        self.dividends = dividends
        self.portfolio_mv = new_mv + self.cash
        # self.mv_history[date] = self.portfolio_mv

    def buy_security(self, position: Position, amount: float, date: datetime, commission: float, cost_per_share: float,
                     notes=''):
        self.history.append(['buy', position.ticker, date, amount])
        self.make_transaction(position.ticker, position.name, 'buy', date, amount, commission, notes, cost_per_share)
        self.cash -= convert_currency(position.currency, self.currency, amount * cost_per_share)
        # self.update_mv()

    def sell_security(self, position: Position, amount: float, date: datetime, commission: float, cost_per_share: float,
                      notes=''):
        self.cash += convert_currency(position.currency, self.currency, amount * cost_per_share)
        self.make_transaction(position.ticker, position.name, 'sell', date, amount, commission, notes, cost_per_share)
        if position.shares == 0:
            self.user_data.curr_investments.remove(position)
        # self.update_mv()
        self.history.append(['sell', position.ticker, date, amount])

    def buy_option(self, position: Position, amount: float, date: datetime, commission: float, cost_per_share: float,
                   strike_price: float, premium: float, c_or_p: str, notes=''):
        self.history.append([f'buy {c_or_p}', position.ticker, date, amount])
        self.make_transaction_option(position.ticker + f' {c_or_p}', position.name, c_or_p, date, amount, commission,
                                     notes,
                                     premium * 100)
        self.cash -= convert_currency(position.currency, self.currency, premium * 100)

    def make_transaction_option(self, ticker: str, name: str, transaction_identifier: str, date: datetime,
                                contract_amounts: int, commission: float, break_even: float
                                , notes: str, premium: float, expiry_date: datetime, strike_price: float):
        new_t = OptionTransaction(ticker, name, transaction_identifier, date, contract_amounts, commission, notes,
                                  premium, break_even, expiry_date, strike_price)
        if ticker in self.user_data.positions.keys():
            self.user_data.positions[ticker].add_transaction(new_t)
            self.update_mv()
            """if date in self.mv_history.keys():
                self.mv_history[date] += 
            else:
                self.mv_history[date] = self.portfolio_mv"""
            return
        new_position = Position(name, ticker, [], self.currency, date)
        new_position.add_transaction(new_t)
        self.user_data.positions[ticker] = new_position
        self.update_mv()
        # self.mv_history[date] = self.portfolio_mv
        return new_t

    def exercise_option(self, position: Position, amount: float, date: datetime, commission: float,
                        cost_per_share: float, strike_price: float, premium: float, c_or_p: str, notes=''):
        pass

    def sell_option(self):
        pass

    def graph(self):
        all_points = []
        info = []
        for position in self.user_data.positions.values():
            curr = position.graph()
            all_points.extend(zip(*curr[0]))
            info.append((position.ticker, position.date))
        return all_points, info

    def deposit_cash(self, amount: float, date: datetime):
        self.cash += amount
        self.portfolio_mv += amount
        self.total_deposits += amount
        self.history.append(['deposit', self.currency, date, amount])
        # self.mv_history[date] = self.portfolio_mv

    def withdraw_cash(self, amount: float, date: datetime):
        self.cash -= amount
        self.portfolio_mv -= amount
        self.total_deposits -= amount
        self.history.append(['withdraw', self.currency, date, amount])
        # self.mv_history[date] = self.portfolio_mv

    def get_cash(self):
        return self.cash + self.dividends

    def get_mv(self):
        return self.portfolio_mv


def convert_currency(currency_from: str, currency_to: str, amount: float) -> float:
    if currency_from == currency_to:
        return amount
    read = json.loads(convert(currency_from, currency_to, amount))
    return float(read['amount'])


def get_current_price(symbol) -> float:
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]


if __name__ == '__main__':
    U = User('Faisal', datetime(2019, 10, 9), 'CAD')
    U.deposit_cash(1000000, datetime(2019, 10, 9))
    print(datetime(2019, 11, 9))
    #  U.make_transaction('msft', 'microsoft', 'buy', datetime(2019, 11, 9), 1000, 0, '', 210)
    new_p = Position('Microsoft', 'msft', [], 'USD', datetime(2019, 10, 9))
    U.buy_security(new_p, 1000, datetime(2019, 10, 9), 0, 210)
    print(U.user_data.positions['msft'].shares)
    U.update_mv()
    print('a')
    print(U.get_mv())
    print(U.user_data.positions['msft'].shares)
    print(U.cash)
    print(U.user_data.positions['msft'].dividends)
    U.sell_security(U.user_data.positions['msft'], 500, datetime.now(), 0, 300)
    print('b')
    print(U.user_data.positions['msft'].shares)
    print(U.user_data.positions['msft'].dividends)
    print('c')
    print(U.cash)
    print(U.get_mv())
    print('d')
    U.buy_security(new_p, 250, datetime(2020, 10, 9), 0, 300)
    print(U.graph())

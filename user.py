from main import *


class User:
    """
    Class representing User data such as Name and Net-worth
    """

    def __init__(self, username: str, start_date: datetime):
        self.user_data = UserData(username, start_date)
        self.portfolio_mv = 0
        self.cash = 0

    def make_transaction(self, ticker: str, name: str, transaction_identifier: str, date: datetime, shares: float,
                         commission: float, notes: str, cost_per_share: float):
        new_t = Transaction(ticker, name, transaction_identifier, date, shares, commission, notes, cost_per_share)
        if ticker in self.user_data.positions.keys():
            self.user_data.positions[ticker].add_transaction(new_t)
            return
        new_p = Position(name, ticker, [])
        new_p.add_transaction(new_t)
        self.user_data.positions[ticker] = new_p
        self.update_mv()
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
        for position in self.user_data.positions.values():
            new_mv += (position.shares * get_current_price(position.ticker)) + position.dividends
        self.portfolio_mv = new_mv + self.cash

    def buy_security(self, position: Position, amount: float, date: datetime, commission: float, cost_per_share: float,
                     notes=''):
        pass

    def sell_security(self, position: Position, amount: float, date: datetime, commission: float, cost_per_share: float,
                      notes=''):
        if position.shares == 0:
            self.user_data.curr_investments.remove(position)
        self.cash += amount * cost_per_share
        self.make_transaction(position.ticker, position.name, 'sell', date, amount, commission, notes, cost_per_share)
        self.update_mv()

    def deposit_cash(self, amount: float):
        self.cash += amount
        self.portfolio_mv += amount

    def withdraw_case(self, amount: float):
        self.cash -= amount
        self.portfolio_mv -= amount

    def get_cash(self):
        return self.cash

    def get_mv(self):
        return self.portfolio_mv


def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]


if __name__ == '__main__':
    U = User('Faisal', datetime(2019, 10, 9))
    print(datetime(2019, 11, 9))
    U.make_transaction('msft', 'microsoft', 'buy', datetime(2019, 11, 9), 1000, 0, '', 210)
    print(U.user_data.positions['msft'].shares)
    U.update_mv()
    print('hellothere')
    print(U.get_mv())
    print(U.user_data.positions['msft'].shares)
    print(U.cash)
    print(U.user_data.positions['msft'].dividends)
    U.sell_security(U.user_data.positions['msft'], 500, datetime.now(), 0, 300)
    print('hellothere')
    print(U.user_data.positions['msft'].shares)
    print(U.user_data.positions['msft'].dividends)
    print('hellothere')
    print(U.cash)
    print(U.get_mv())
    print('hellothere')


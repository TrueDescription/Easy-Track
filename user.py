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
        print(new_t)
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

    def avg_roi(self):
        for key in self.user_data.positions:
            pass

    def update_mv(self):
        new_mv = 0
        for position in self.user_data.positions.values():
            print('hello')
            new_mv += position.shares * get_current_price(position.ticker) + position.dividends
            print(new_mv)
            print('hello')

    def sell_security(self, position: Position, amount: float):
        position.shares -= amount
        if position.shares == 0:
            self.user_data.curr_investments.remove(position)


def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]


if __name__ == '__main__':
    U = User('Faisal', datetime(2019, 10, 9))
    print(datetime(2019, 11, 9))
    U.make_transaction('msft', 'microsoft', 'buy', datetime(2019, 11, 9), 1000, 0, '', 210)
    print(U.user_data.positions['msft'].dividends)
    print(U)

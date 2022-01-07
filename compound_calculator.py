import json
from datetime import datetime

import yfinance as yf

from main import UserData
import numpy as np
import matplotlib.pyplot as plt

from position import Position
from user import User
import pandas as pd

from google_currency import convert


def compound_calculator(initial: float, regular_addition: float, interval: str, rate: float, c_interval: str,
                        length: int):
    interval_d = {'Weekly': 52, 'Monthly': 12, 'Bi-weekly': 26.07145, 'Yearly': 1, 'Quarterly': 4}
    interval_res = interval_d[interval]
    data = {}
    c_rate = rate
    if c_interval == 'Monthly':
        c_rate = rate / 12
        interval_amount_saved = (interval_res * regular_addition) / 12
        final = initial
        total_saved = initial
        total_interest = 0
        month = 1
        for y in range(length):
            for m in range(12):
                iteration = [regular_addition, total_saved + interval_amount_saved]
                final += interval_amount_saved
                total_saved += interval_amount_saved
                monthly_interest = final * (c_rate / 100)
                total_interest += final * (c_rate / 100)
                final += monthly_interest
                iteration.append(monthly_interest)
                iteration.append(total_interest)
                iteration.append(final)
                # month, regular addition, total_saved + interval contribution, monthly gain, total_interest, final
                if y == 0:
                    data[month] = iteration
                else:
                    data[month] = iteration
                month += 1
    return data


def extrapolator(user_data: UserData):
    """
    # Note for later: implement graph transaction, then graph position, then graph user portfolio, use that and attach
    to the right of it the above function data and graph.
    :param user_data:
    :return:
    """
    pass


def all_asset_grapher(user: User):
    all_position_graphs = []
    x = []
    y = []
    CB91_Blue = '#2CBDFE'
    CB91_Green = '#47DBCD'
    CB91_Pink = '#F3A0F2'
    CB91_Purple = '#9D2EC5'
    CB91_Violet = '#661D98'
    CB91_Amber = '#F5B14C'
    color_list = [CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber,
                  CB91_Purple, CB91_Violet]
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)
    for ticker in list(user.user_data.positions.keys()):
        actual_position = user.user_data.positions[ticker]
        res = asset_grapher(actual_position.graph(), actual_position.ticker, actual_position.date)
        plt.plot(res[0], res[1], label=actual_position.ticker)
        plt.ticklabel_format(useOffset=False, axis='y')
        plt.fill_between(res[0], res[1], alpha=0.5)

    plt.xlabel('Date')
    plt.ylabel('Market Value')
    plt.legend()
    plt.show()

    """
    graph_data = user.graph()
    points_refined = graph_data[0]
    info = graph_data[1]
    print(points_refined)
    print(info)
    x = points_refined[0][0]
    y = points_refined[0][1]
    i = 1
    x_final = []
    y_final = []
    mk_history = yf.Ticker(points_refined[1]).history(start=points_refined[2])
    print(mk_history)
    indexes = list(mk_history.index)
    curr_shares = y[0]
    for date in indexes:
        if date >= x[i]:
            curr_shares = y[i]
            i += 1
        x_final.append(date)
        y_final.append(curr_shares * mk_history[f'{date.year}-{date.month}-{date.day}'])
    plt.plot(x_final, y_final)
    plt.xlabel('Date')
    plt.ylabel('Market Value')
    plt.show()
    """


def asset_grapher(points: list, ticker: str, start_date: datetime):
    #print(f'{points} | {ticker} | {start_date}')
    flag = True
    if len(points) == 1:
        flag = False
    mk_history = yf.Ticker(ticker).history(start=start_date)['Close']
    #print(mk_history)
    indexes = list(mk_history.index)
    curr_shares = points[0][1]
    x = []
    y = []
    i = 1
    for date in indexes:
        if flag and date >= points[i][0]:
            curr_shares = points[i][1]
            i += 1
        if i >= len(points):
            flag = False
        x.append(date)
        y.append(curr_shares * mk_history[f'{date.year}-{date.month}-{date.day}'])

        # print(curr_shares * mk_history[f'{date.year}-{date.month}-{date.day}'])
    # print(x)
    # print(y)
    # plt.plot(x, y)
    # plt.xlabel('Date')
    # plt.ylabel('Market Value')
    # plt.show()
    return [x, y]


def convert_currency(currency_from: str, currency_to: str, amount: float) -> float:
    if currency_from == currency_to:
        return amount
    read = json.loads(convert(currency_from, currency_to, amount))
    return float(read['amount'])

    # plt.plot(x, y)
    # plt.xlabel('Date')
    # plt.ylabel('Market Value')
    # plt.show()


if __name__ == '__main__':
    U = User('Faisal', datetime(2019, 10, 9), 'CAD')
    U.deposit_cash(1000000, datetime(2019, 10, 9))
    #  U.make_transaction('msft', 'microsoft', 'buy', datetime(2019, 11, 9), 1000, 0, '', 210)
    new_p = Position('Microsoft', 'msft', [], 'USD', datetime(2019, 10, 9))
    new_p2 = Position('Google', 'googl', [], 'USD', datetime(2020, 3, 13))
    U.buy_security(new_p, 1000, datetime(2019, 10, 9), 0, 210)
    U.buy_security(new_p2, 250, datetime(2020, 3, 13), 0, 2900)
    U.buy_security(new_p2, 1, datetime(2020, 5, 13), 0, 2900)
    # U.update_mv()
    U.sell_security(U.user_data.positions['msft'], 500, datetime.now(), 0, 300)
    U.buy_security(new_p, 250, datetime(2020, 10, 9), 0, 300)
    all_asset_grapher(U)

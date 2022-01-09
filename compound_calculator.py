import json
import time
from datetime import datetime

import yfinance as yf
from dateutil.relativedelta import relativedelta

from main import UserData
import numpy as np
import matplotlib.pyplot as plt

from position import Position
from user import User
import pandas as pd

from google_currency import convert


def create_pie_charts(user: User):
    # Dividends
    tickers = []
    amount = []
    distribution_amounts = []
    sectors = []
    sectors_distribution = []
    industries = []
    industry_distrubution = []
    for ticker in user.user_data.positions.keys():
        ap = user.user_data.positions[ticker]
        tickers.append(ticker)
        amount.append(ap.dividends)
        distribution_amounts.append(convert_currency(ap.currency, user.currency, get_current_price(ticker) * ap.shares))
        sector = ap.info['sector']
        if sector in sectors:
            sectors_distribution[sectors.index(sector)] += ap.cost
        else:
            sectors.append(sector)
            sectors_distribution.append(ap.cost)
        industry = ap.info['industry']
        if industry in industries:
            industry_distrubution[industries.index(industry)] += ap.cost
        else:
            industries.append(industry)
            industry_distrubution.append(ap.cost)
    if max(amount) != 0:
        fig1 = plt.figure()
        ax = fig1.add_axes([0, 0, 1, 1])
        ax.pie(amount, labels=tickers, autopct='%1.2f%%')
        plt.show()
    if len(distribution_amounts) != 0:
        fig2 = plt.figure()
        ax2 = fig2.add_axes([0, 0, 1, 1])
        ax2.pie(distribution_amounts, labels=tickers, autopct='%1.2f%%')
        plt.show()
    if len(sectors) != 0:
        fig3 = plt.figure()
        ax3 = fig3.add_axes([0, 0, 1, 1])
        ax3.pie(sectors_distribution, labels=sectors, autopct='%1.2f%%')
        plt.show()
    if len(industries) != 0:
        fig3 = plt.figure()
        ax3 = fig3.add_axes([0, 0, 1, 1])
        ax3.pie(industry_distrubution, labels=industries, autopct='%1.2f%%')
        plt.show()


def get_current_price(symbol) -> float:
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]


def compound_calculator(initial: float, regular_addition: float, interval: str, rate: float, c_interval: str,
                        length: int, graph=True, alpha=1.0, t_interest=0):
    interval_d = {'Weekly': 52, 'Monthly': 12, 'Bi-weekly': 26, 'Yearly': 1, 'Quarterly': 4}
    interval_res = interval_d[interval]
    data = {}
    c_rate = rate
    x_months = []
    y_interest = []
    y_final = []
    Light = '#23b6db'
    Dark = '#3d6f8d'
    color_list = [Light, Dark]
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)
    if c_interval == 'Monthly':
        c_rate = rate / 12
        interval_amount_saved = (interval_res * regular_addition) / 12
        final = initial
        total_saved = initial
        total_interest = t_interest
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
                x_months.append(month)
                y_interest.append(total_interest)
                y_final.append(final)
                month += 1
    # print(graph)
    if graph:
        # print('hellloooooooo')
        plt.plot(x_months, y_final)
        plt.plot(x_months, y_interest)
        plt.fill_between(x_months, y_final, alpha=alpha)
        plt.fill_between(x_months, y_interest, alpha=alpha)
        plt.xlim(left=1)
        plt.show()
    return data, x_months, y_final, y_interest


def extrapolator(user: User):
    """
    # Note for later: implement graph transaction, then graph position, then graph user portfolio, use that and attach
    to the right of it the above function data and graph.
    :param user:
    :return:
    """
    data = all_asset_grapher(user, False)
    history = data[0]
    div_history = data[1]
    big_data = {}
    summation = 0
    start = None
    next_date = None
    k = 1
    div_keys = list(div_history.keys())
    if len(div_history) > 0:
        start = div_keys[0]
        summation += div_history[start]
        if len(div_history) > 1:
            next_date = div_keys[1]
    total_positions = len(user.user_data.positions)
    max_date = None
    for item in history:
        all_x = item[0]
        all_y = item[1]
        i = 0
        while i < len(all_x):
            if all_x[i] in big_data.keys():
                big_data[all_x[i]][0] += all_y[i]
                big_data[all_x[i]][1] += 1
            else:
                big_data[all_x[i]] = [all_y[i], 1]
            if start is not None and all_x[i] > start:
                big_data[all_x[i]][0] += summation
                # print(summation)
            elif start is not None and next_date is not None:
                if next_date <= all_x[i]:
                    k += 1
                    try:
                        start = div_keys[k]
                        next_date = div_keys[k + 1]
                    except IndexError:
                        start = div_keys[k]
                        next_date = None
                    summation += div_history[start]
            i += 1
    big_data_keys = list(big_data.keys())
    for key in big_data_keys:
        if big_data[key][1] != total_positions:
            big_data.pop(key)
        else:
            big_data[key] = big_data[key][0]
            if max_date is None or key > max_date:
                max_date = key
    all_points = list(big_data.items())
    all_points.sort(key=lambda date: date[0])

    # value_pairs = list(big_data.items())
    final_x, final_y = list(zip(*all_points))
    t_interest = (((user.portfolio_mv - user.cash) / user.total_deposits) - 1) * (user.portfolio_mv - user.cash)
    extrap_data = compound_calculator(big_data[max_date], 0, 'Monthly', 13, 'Monthly', 5, graph=False, alpha=0.5,
                                      t_interest=t_interest)
    x_extrap = extrap_data[1]
    y_extrap = extrap_data[2]
    y_interest = extrap_data[3]
    for i in range(len(x_extrap)):
        x_extrap[i] = max_date + relativedelta(months=x_extrap[i]) - relativedelta(months=1)
    plt.vlines(x=x_extrap[0], ymin=0, ymax=big_data[max_date], label='Start of Projection', color='#000000')
    plt.plot(x_extrap, y_extrap, label='Projected Growth', color='#2CBDFE')
    plt.plot(x_extrap, y_interest, label='Interest Growth', color='#3d6f8d')
    plt.fill_between(x_extrap, y_extrap, alpha=0.3, color='#2CBDFE')
    plt.fill_between(x_extrap, y_interest, alpha=0.3, color='#3d6f8d')
    plt.plot(final_x, final_y, label='Net Worth', color='#2CBDFE')
    plt.ticklabel_format(style='plain', axis='y')
    plt.fill_between(final_x, final_y, alpha=0.3, color='#2CBDFE')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Market Value')
    plt.legend()
    plt.show()


def all_asset_grapher(user: User, graph=True):
    CB91_Blue = '#2CBDFE'
    CB91_Green = '#47DBCD'
    CB91_Pink = '#F3A0F2'
    CB91_Purple = '#9D2EC5'
    CB91_Violet = '#661D98'
    CB91_Amber = '#F5B14C'
    color_list = [CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber,
                  CB91_Purple, CB91_Violet]
    data = []
    div_data = {}
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)
    for ticker in list(user.user_data.positions.keys()):
        actual_position = user.user_data.positions[ticker]
        res = asset_grapher(actual_position.graph(), actual_position.ticker, actual_position.date)
        if graph:
            plt.plot(res[0], res[1], label=actual_position.ticker)
            plt.ticklabel_format(useOffset=False, axis='y')
            plt.fill_between(res[0], res[1], alpha=0.5)
            continue
        data.append((res[0], res[1]))
        update_dict(div_data, actual_position.div_history)
        # div_data.extend(list(actual_position.div_history.items()))
    if graph:
        plt.xlabel('Date')
        plt.ylabel('Market Value')
        plt.legend()
        plt.show()
    # print([data, div_data])
    return [data, div_data]


def update_dict(to: dict, data_from: dict):
    for key in data_from.keys():
        if key in to.keys():
            to[key] += data_from[key]
        else:
            to[key] = data_from[key]


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
    # print(f'{points} | {ticker} | {start_date}')
    flag = True
    if len(points) == 1:
        flag = False
    mk_history = yf.Ticker(ticker).history(start=start_date)['Close']
    # print(mk_history)
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
    # """
    t2 = time.time()
    U = User('Faisal', datetime(2019, 10, 9), 'CAD')
    U.deposit_cash(1000000, datetime(2019, 10, 9))
    #  U.make_transaction('msft', 'microsoft', 'buy', datetime(2019, 11, 9), 1000, 0, '', 210)
    new_p = Position('Microsoft', 'msft', [], 'USD', datetime(2020, 5, 9))
    # new_p2 = Position('Google', 'googl', [], 'USD', datetime(2020, 3, 13))
    U.buy_security(new_p, 1000, datetime(2020, 5, 9), 0, 210)
    # new_p3 = Position('Bitcoin', 'BTC-USD', [], 'USD', datetime(2019, 3, 13))
    # U.buy_security(new_p3, 10, datetime(2019, 3, 13), 0, 4000)
    # U.buy_security(new_p2, 250, datetime(2020, 3, 13), 0, 2900)
    # U.buy_security(new_p2, 1, datetime(2020, 5, 13), 0, 2900)
    # U.update_mv()
    # U.sell_security(U.user_data.positions['msft'], 500, datetime(2021, 12, 13), 0, 300)
    # U.buy_security(new_p, 1000, datetime(2021, 10, 9), 0, 210)
    t3 = time.time()
    print(f'Transaction Times:|{t3 - t2}|')
    # U.buy_security(new_p, 250, datetime(2020, 10, 9), 0, 300)
    # all_asset_grapher(U)
    t0 = time.time()
    create_pie_charts(U)
    t1 = time.time()
    print(f'Total Time:|{t1 - t0}|')
    """
    data = compound_calculator(12500, 1000, 'Monthly', 13, 'Monthly', 5)
    print(data[60])
    """

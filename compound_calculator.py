from main import UserData


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

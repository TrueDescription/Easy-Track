import numpy as np
from scipy.stats import norm
from yahoo_fin import options


def d(sigma, S, K, r, t):
    d1 = 1 / (sigma * np.sqrt(t)) * (np.log(S / K) + (r + sigma ** 2 / 2) * t)
    d2 = d1 - sigma * np.sqrt(t)
    return d1, d2


def call_price(sigma, S, K, r, t, d1, d2):
    C = norm.cdf(d1) * S - norm.cdf(d2) * K * np.exp(-r * t)
    return C


def put_price(sigma, S, K, r, t, d1, d2):
    P = -norm.cdf(-d1) * S + norm.cdf(-d2) * K * np.exp(-r * t)
    return P


def delta(d_1, contract_type):
    if contract_type == 'c':
        return norm.cdf(d_1)
    if contract_type == 'p':
        return -norm.cdf(-d_1)


def gamma(d2, S, K, sigma, r, t):
    return K * np.exp(-r * t) * (norm.pdf(d2) / (S ** 2 * sigma * np.sqrt(t)))


def theta(d1, d2, S, K, sigma, r, t, contract_type):
    if contract_type == 'c':
        theta = -S * sigma * norm.pdf(d1) / (2 * np.sqrt(t)) - r * K * np.exp(-r * t) * norm.cdf(d2)
    if contract_type == 'p':
        theta = -S * sigma * norm.pdf(-d1) / (2 * np.sqrt(t)) + r * K * np.exp(-r * t) * norm.cdf(-d2)

    return theta


def vega(sigma, S, K, r, t):
    d1, d2 = d(sigma, S, K, r, t)
    v = S * norm.pdf(d1) * np.sqrt(t)
    return v

"""if __name__ == '__main__':
    execfile"""
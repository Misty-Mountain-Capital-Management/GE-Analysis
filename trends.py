import json
from scipy.interpolate import lagrange
from rs_ge import *

def get_trends_prices(prices):
    trends = [None]
    for i in range(1, len(prices) - 1):
        # Simple assumption; between any two values, there is a slope.
        # for points x=a, x=b, and x=c, we assume the slope at point x=b is the average of the slope between
        # x=a -> x=b, and x=b -> c=c
        new_diff = ((prices[i] - prices[i - 1]) + (prices[i + 1] - prices[i])) / 2.
        trends.append(new_diff)
    trends.append(None)

    return trends

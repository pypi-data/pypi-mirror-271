from numbers import Complex
from typing import Sequence

import numpy as np
from matplotlib import pyplot as plt

from marib import PPS


class Test(object):
    def __init__(self, method):
        self.Method = method

    def __call__(self, pps, query=(), interval: Sequence[Complex] = None, num=100):
        pps.plot('r-', 'data_line')

        answer = PPS(query, self.Method(pps)(query))
        answer.plot(label='query')

        if interval is None:
            interval = np.linspace(min(pps)[0], max(pps)[0], num)

        predict_line = PPS(interval, self.Method(pps)(interval))
        predict_line.plot('b:', 'predict_line')
        plt.legend()
        plt.show()

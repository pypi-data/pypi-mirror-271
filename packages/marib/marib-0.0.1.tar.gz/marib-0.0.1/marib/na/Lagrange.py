from numbers import Complex
from typing import Sequence

from marib.PPS import PPS


class Lagrange(object):
    """
    Lagrange's interpolation.

    L(x) = y0*l0(x) + y1*l1(x) + ... + yn*ln(x)

    This should have the same result as the Newton's interpolation.
    """

    def __init__(self, pps: PPS):
        self.x = pps.x
        self.y = pps.y

    def _omega(self, xj, rmv=-1):
        """
        A math function for computing w(x) = (x - x0)(x - x1)...(x - xn).
        :param rmv: remove specific item in the product, defaults -1 (not remove any)
        :param xj: x to compute
        :return: w(xj)
        """
        idx = list(range(len(self.x)))
        if rmv != -1:
            idx.remove(rmv)

        res = 1
        for i in idx:
            res *= (xj - self.x[i])
        return res

    def _l(self, i):
        return lambda x: self._omega(x, i) / self._omega(self.x[i], i)

    def __call__(self, query: Complex | Sequence[Complex]):
        if isinstance(query, Complex):
            res = 0
            for i in range(len(self.y)):
                res += self.y[i] * self._l(i)(query)
            return res
        else:
            return [self.__call__(q) for q in query]

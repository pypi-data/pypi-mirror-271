from numbers import Complex
from typing import Sequence

from marib.PPS import PPS


class Newton(object):
    """
    Newton's interpolation.

    f(x) = f(x0) + f[x0, x1](x - x0) + ... + f[x0, x1, ..., xn](x - x0)(x - x1)...(x - xn)

    This should have the same result as the Lagrange's interpolation.
    """

    def __init__(self, pps: PPS):
        pps.keep_order()
        self.pps = pps
        self._Tb: list[list] = []
        self._update_Tb(extend=False)

    def add_sample(self, pps: PPS):
        do_extend = max(pps) <= min(self.pps) or max(self.pps) <= min(pps)
        self.pps += pps
        self._update_Tb(extend=do_extend)
        return self

    def _update_Tb(self, *, extend=True):
        x, y = self.pps.x, self.pps.y

        if extend:
            s = len(self._Tb)
            _Tb = self._Tb
            _Tb[0] = self.pps.y
        else:
            s = 0
            _Tb = [self.pps.y]

        for i in range(1, self.pps.n):
            ith_diff, pre_diff = [], _Tb[i - 1]
            for j in range(max(0, s - i), len(pre_diff) - 1):
                ith_diff.append((pre_diff[j + 1] - pre_diff[j]) / (x[i + j] - x[j]))
            if i < len(_Tb):
                _Tb[i].extend(ith_diff)
            else:
                _Tb.append(ith_diff)

        self._Tb = _Tb

    def _omega(self, n, xj):
        """
        A math function for computing w(x) = (x - x0)(x - x1)...(x - xn).
        :param n: n in the math function
        :param xj: x to compute
        :return: w(xj)
        """
        res = 1
        for i in range(n):
            res *= (xj - self.pps.x[i])
        return res

    def __call__(self, query: Complex | Sequence[Complex], max_pow=-1):
        """
        Compute the answer of the query by Newton interpolation.

        f(x) = f(x0) + f[x0, x1](x - x0) + f[x0, x1, x2](x - x0)(x - x1)(x - x2) + ...

        :param query: x-value expected to query
        :param max_pow: the max power of Newton interpolation polynomial, defaults -1 (as high as possible)
        :return: answer of the query by Newton interpolation
        """
        if max_pow == -1:
            max_pow = len(self._Tb) - 1
        if isinstance(query, Complex):
            res = 0
            for i in range(max_pow + 1):
                res += self._Tb[i][0] * self._omega(i, query)
            return res
        else:
            return [self.__call__(q, max_pow) for q in query]

from numbers import Real, Complex
from typing import Callable, Sequence

from marib.PPS import PPS
from marib.vec import vec


class LeastSquare(object):
    """
    Least square.
    Same as np.polyfit.
    """

    def __init__(self, pps: PPS, max_pow=5, weight: Callable[[Real], Real] = lambda x: 1):
        self.n = max_pow
        self.x = vec(pps.x)
        self.y = vec(pps.y)
        self.omega = vec([weight(xi) for xi in self.x])
        self._Ptb = [vec([1]), vec([-sum(self.omega * self.x) / sum(self.omega), 1])]
        self._A = []
        self._solve_Param()

    def _P(self, k, x):
        """
        A math function for computing polynomial P(x) = a0 + a1 * x + a2 * x^2 + ... + an * x^n
        :param k: which polynomial
        :param x: x to compute
        :return: P(x)
        """
        if isinstance(x, Real):
            pow_seq = vec([x ** i for i in range(len(self._Ptb[k]))])
            return sum(pow_seq * self._Ptb[k])
        else:
            return vec([self._P(k, xi) for xi in x])

    def _solve_Param(self):
        x, y, w = self.x, self.y, self.omega
        _Ptb = self._Ptb
        for k in range(1, self.n):
            a = sum(w * x * self._P(k, x)**2) / sum(w * self._P(k, x)**2)
            b = sum(w * self._P(k, x)**2) / sum(w * self._P(k - 1, x)**2)
            _Ptb.append(vec([-a, 1]) ** _Ptb[k] - b * _Ptb[k - 1])
        for k in range(self.n + 1):
            self._A.append(sum(w * y * self._P(k, x)) / sum(w * self._P(k, x)**2))

    def __call__(self, query: Complex | Sequence[Complex]):
        if isinstance(query, Complex):
            res = 0
            for i in range(self.n + 1):
                res += self._A[i] * self._P(i, query)
            return res
        else:
            return [self.__call__(q) for q in query]

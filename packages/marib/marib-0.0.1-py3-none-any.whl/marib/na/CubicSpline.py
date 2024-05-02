from numbers import Complex
from typing import Sequence

import numpy as np

from marib.PPS import PPS


class CubicSpline(object):
    """
    CubicSpline interpolation.
    """
    FDB = 1  # FIRST_DERIVATIVE_BOUNDARY
    SDB = 2  # SECOND_DERIVATIVE_BOUNDARY
    NDB = 3  # NATURAL_DERIVATIVE_BOUNDARY

    def __init__(self, pps: PPS, boundary: PPS = None, btype=NDB):
        pps.keep_order()
        self.pps: PPS = pps
        self.boundary: PPS = boundary
        self.btype: int = btype
        self._Mtx: np.ndarray = np.ndarray(0)
        self._run_spline()

    def _run_spline(self):
        x, y, n = self.pps.x, self.pps.y, self.pps.n - 1  # to ensure index n can be reached.
        fl, fr = [0, 0] if self.boundary is None else sorted(self.boundary.y)

        def h(i): return x[i + 1] - x[i]
        def f(i, j): return (y[i] - y[j]) / (x[i] - x[j])

        if self.btype == CubicSpline.FDB:
            lamda_0, u_n = 1, 1
            d_0 = 6 / h(0) * (f(0, 1) - fl)
            d_n = 6 / h(n - 1) * (fr - f(n - 1, n))
        elif self.btype == CubicSpline.SDB or self.btype == CubicSpline.NDB:
            lamda_0, u_n = 0, 0
            d_0, d_n = 2 * fl, 2 * fr
        else:
            lamda_0, u_n = 0, 0
            d_0, d_n = 2 * fl, 2 * fr

        matrix = np.eye(n + 1) * 2
        for r in range(1, n):
            u = h(r - 1) / (h(r - 1) + h(r))
            matrix[r][r - 1] = u
            matrix[r][r + 1] = 1 - u
        matrix[0][1] = lamda_0
        matrix[n][-2] = u_n

        d = [d_0] + [6 * (f(i, i + 1) - f(i - 1, i)) / (h(i - 1) + h(i)) for i in range(1, n)] + [d_n]
        self._Mtx = np.linalg.inv(matrix) @ np.array(d)

    def _find_interval(self, xj: Complex):
        x = self.pps.x
        for i in range(self.pps.n - 1):
            if x[i] <= xj <= x[i + 1]:
                return i
        return 0 if xj < x[0] else self.pps.n - 2  # interval num is 1 less than point num, and here return its index.

    def __call__(self, query: Complex | Sequence[Complex]):
        x, y, n = self.pps.x, self.pps.y, self.pps.n - 1  # to ensure index n can be reached.
        _Mtx = self._Mtx

        def h(i): return x[i + 1] - x[i]

        def inter_call(xi):
            if isinstance(xi, Complex):
                j = self._find_interval(xi)
                return (_Mtx[j]*(x[j + 1] - xi)**3 + _Mtx[j + 1]*(xi - x[j])**3 +
                        (6*y[j] - _Mtx[j]*h(j)**2)*(x[j + 1] - xi) + (6*y[j + 1] - _Mtx[j + 1]*h(j)**2)*(xi - x[j])
                        ) / (6 * h(j))
            else:
                return [self.__call__(q) for q in query]
        return inter_call(query)

from numbers import Real
from typing import Callable

import numpy as np

from marib import vec


class Integration(object):
    """
    Integration of a math function f from a to b.
    """
    ZERO = 1e-9

    def __init__(self, a: Real, b: Real, f: Callable[[Real], Real]):
        self.a = a
        self.b = b
        self.f = f

    def _f(self, x):
        """
        A math function for computing f(x).
        :param x: x to compute
        :return: f(x)
        """
        try:
            return self.f(x)
        except (ZeroDivisionError, ValueError):
            return self.f(Integration.ZERO)

    def brute_force(self, dx=0.01):
        """
        Compute this integration by brute force method.
        :param dx: step
        :return: the answer of this integration
        """
        res, x = 0, self.a
        while x <= self.b:
            res += self._f(x) * dx
            x += dx
        return res

    def trapezoid(self, n=1):
        """
        In each interval, using I = h/2 * (f(a) + f(b)), where h = (b - a) / n.
        :param n: amount of intervals
        :return: the answer of this integration
        """
        h = (self.b - self.a) / n
        x = [self.a + i * h for i in range(n + 1)]

        res = 0
        for i in range(len(x) - 1):
            res += self._f(x[i]) + self._f(x[i + 1])
        return h / 2 * res

    def simpson(self, n=1):
        """
        In each interval, using I = h/6 * (f(a) + 4*f((a + b) / 2) + f(b)), where h = (b - a) / n.
        :param n: amount of intervals
        :return: the answer of this integration
        """
        h = (self.b - self.a) / n
        x = [self.a + i * h for i in range(n + 1)]

        res = 0
        for i in range(len(x) - 1):
            res += self._f(x[i]) + 4 * self._f((x[i] + x[i + 1]) / 2) + self._f(x[i + 1])
        return h / 6 * res

    def romberg(self, epsilon=1e-5):
        """
        Romberg's method.
        :param epsilon: the maximum deviation
        :return: the answer of this integration, with deviation no bigger than epsilon
        """
        a, b, f = self.a, self.b, self._f
        x = [a, b]

        def nxT(t):  # T2n = 0.5 * (Tn + (b - a) / n * sum(f(xi)))
            nonlocal x
            n = len(x) - 1
            mid = [(x[i] + x[i + 1]) / 2 for i in range((len(x) - 1))]
            x = sorted(x + mid)
            return 0.5 * (t + (b - a) / n * sum([f(xi) for xi in mid]))

        t1 = (b - a) / 2 * (f(b) + f(a))
        t2 = nxT(t1)
        _Tb = [[t1], [t2, (4 * t2 - t1) / 3]]
        while abs(_Tb[-1][0] - _Tb[-2][0]) > epsilon:
            pre, tn = _Tb[-1], _Tb[-1][0]
            res = [nxT(tn)]
            for i in range(len(pre)):
                res.append((4 * res[i] - pre[i]) / 3)
            _Tb.append(res)
        return _Tb[-1][-1]

    def self_adaptive(self, epsilon=1e-5):
        """
        Self adaptive with Simpson's method.
        :param epsilon: the maximum deviation
        :return: the answer of this integration, with deviation no bigger than epsilon
        """
        a, b = self.a, self.b

        def adaptive_inner(l, r, pre_res):
            m = (l + r) / 2
            Il = Integration(l, m, self._f).simpson()
            Ir = Integration(m, r, self._f).simpson()
            cur_res = Il + Ir
            # print(f"l: {l}, r: {r}, I: {cur_res}")
            if abs(pre_res - cur_res) < epsilon:
                return (16 * cur_res - pre_res) / 15
            else:
                return adaptive_inner(l, m, Il) + adaptive_inner(m, r, Ir)

        return adaptive_inner(a, b, self.simpson())

    def gauss_legendre(self, n=0):
        a, b = self.a, self.b
        if a == -1 and b == 1:
            p = [vec([1]), vec([0, 1])]
            for i in range(2, n + 2):  # need roots of P_{n + 1}
                p.append(vec([0, 2 - 1/i]) ** p[i - 1] - (1 - 1/i) * p[i - 2])
            x = np.roots(p[-1][::-1])
            _M_int, _M_x = [], []  # vec(int) = pow_vec(x) * pow_vec(x)T * vec(a)
            for i in range(n + 1):
                _M_int.append(0 if i & 1 else 2 / (i + 1))
                _M_x.append(x ** i)
            _M_a = np.linalg.inv(_M_x) @ _M_int
            res = 0
            for i in range(n + 1):
                res += _M_a[i] * self._f(x[i])
            return res
        else:
            return Integration(-1, 1, lambda t: (b - a) / 2 * self.f(0.5 * ((b - a) * t + a + b))).gauss_legendre(n)

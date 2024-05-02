from numbers import Real
from typing import Callable, Sequence, Dict, Tuple


class PPS(Sequence):
    """
    Planar Point Set.
    """

    def __init__(self,
                 a: Dict[Real, Real] | Sequence[Tuple[Real, Real]] | Sequence[Real] | 'PPS' = None,
                 b: Sequence[Real] | Callable[[Real], Real] = None,
                 *, keep_order=False):
        self.n: int = 0
        self.x: list[Real] = []
        self.y: list[Real] = []
        self.x2y: dict[Real, Real] = {}
        self._keep_order = keep_order
        self._assign_(a, b)

    def _assign_(self, a, b):
        if a is None: return

        if b is None:
            if isinstance(a, Dict):
                self.x = list(a.keys())
                self.y = list(a.values())
            elif isinstance(a, Sequence):
                self.x = [tp[0] for tp in a]
                self.y = [tp[1] for tp in a]
        else:
            if isinstance(b, Callable):
                self.x = list(a)
                self.y = [b(xi) for xi in a]
            else:
                if len(a) != len(b):
                    raise Exception("Point set must have same size.")
                self.x = list(a)
                self.y = list(b)

        if len(self.x) != len(set(self.x)):
            raise Exception("Repeat x-value exists in point set.")

        self.x2y = {xi: yi for xi, yi in zip(self.x, self.y)}
        self.n = len(self.x2y)
        if self._keep_order: self.sort()

    def __add__(self, other: 'PPS'):
        """
        Add two PPS together.
        :param other: A PPS instance.
        :return: PPS, with the union of two point set.
        """
        if isinstance(other, PPS):
            return PPS(self.x + other.x, self.y + other.y,
                       keep_order=self._keep_order or other._keep_order)
        else:
            raise Exception("PPS can only add with PPS.")

    def __iadd__(self, other):
        return self.__add__(other)

    def sort(self, *, key=None, reverse=False) -> None:
        tmp = sorted(self.x2y.items(), key=key, reverse=reverse)
        for i in range(len(tmp)):
            self.x[i] = tmp[i][0]
            self.y[i] = tmp[i][1]

    def to_point_list(self):
        return [(xi, yi) for xi, yi in zip(self.x, self.y)]

    def keep_order(self, keep=True):
        """
        If a PPS instance is set to keep order, its x-value will be kept in increasing order after operations.
        :param keep: keep order.
        :return:
        """
        self._keep_order = keep
        if self._keep_order:
            self.sort()

    def plot(self, fmt='o', label='', *, scatter=False):
        """
        Plot self with plt.
        :param fmt: a string like '[color][marker][line]'
        :param label:
        :param scatter: plot scatter graph
        :return:
        """
        import matplotlib.pyplot as plt
        if scatter:
            plt.scatter(self.x, self.y)
        else:
            plt.plot(self.x, self.y, fmt, label=label)

    def __getitem__(self, item):
        return self.x2y[item]

    def __iter__(self):
        return self.to_point_list().__iter__()

    def __str__(self):
        return str(self.to_point_list())

    def __repr__(self):
        return f"PPS{self.x, self.y}"

    def __len__(self):
        return self.n

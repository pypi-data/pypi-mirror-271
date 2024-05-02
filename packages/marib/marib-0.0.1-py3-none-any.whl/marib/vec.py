from numbers import Real
from typing import Sequence, Callable


class vec(Sequence):
    """
    vector.
    """

    def __init__(self, seq: Sequence[Real]):
        self.seq = list(seq)

    def _op_dispatcher_(self, other, op: Callable[[Real, Real], Real]):
        if isinstance(other, vec):
            diff = max(len(self), len(other))
            self.seq += [0] * (diff - len(self))
            other.seq += [0] * (diff - len(other))
            return vec([op(x, y) for x, y in zip(self, other)])
        elif isinstance(other, Real):
            return vec([op(x, other) for x in self])
        else:
            raise Exception("Unsupported operation.")

    def __add__(self, other):
        return self._op_dispatcher_(other, lambda x, y: x + y)

    def __sub__(self, other):
        return self._op_dispatcher_(other, lambda x, y: x - y)

    def __mul__(self, other):
        return self._op_dispatcher_(other, lambda x, y: x * y)

    def __truediv__(self, other):
        return self._op_dispatcher_(other, lambda x, y: x / y)

    def __floordiv__(self, other):
        return self._op_dispatcher_(other, lambda x, y: x // y)

    def __pow__(self, other):
        """
        Convolution of a and b.
        """
        if isinstance(other, vec):
            res = [0] * (len(self) + len(other) - 1)
            for i in range(len(self) - 1, -1, -1):
                for j in range(len(other) - 1, -1, -1):
                    res[i + j] += self[i] * other[j]
            return vec(res)
        elif isinstance(other, Real):
            return vec([x ** other for x in self])
        else:
            raise Exception("Unsupported operation.")

    def __getitem__(self, item):
        return self.seq.__getitem__(item)

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __isub__(self, other):
        return self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __iter__(self):
        return self.seq.__iter__()

    def __len__(self):
        return self.seq.__len__()

    def __str__(self):
        return self.seq.__str__()

    def __repr__(self):
        return self.seq.__repr__()

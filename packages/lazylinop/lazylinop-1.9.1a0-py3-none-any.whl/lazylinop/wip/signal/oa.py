import numpy as np
from lazylinop import LazyLinOp
import sys
sys.setrecursionlimit(100000)


def oa(L: int, X: int, overlap: int = 1):
    """return overlap-add linear operator.
    The overlap-add linear operator adds last overlap of block i > 0
    with first overlap of block i + 1.
    Of note, block i = 0 (of size L - overlap) does not change.

    Args:
        L: int
        Block size.
        X: int
        Number of blocks.
        overlap: int
        Size of the overlap < L (strictly positive).

    Returns:
        LazyLinOp or np.ndarray

    Raises:
        ValueError
            L is strictly positive.
        ValueError
            X is strictly positive.
        ValueError
            overlap must be > 0 and <= L

    Examples:
        >>> from lazylinop.wip.signal import oa
        >>> import numpy as np
        >>> signal = np.full(5, 1.0)
        >>> oa(1, 5, overlap=1) @ signal
        array([5.])
        >>> signal = np.full(10, 1.0)
        >>> oa(2, 5, overlap=1) @ signal
        array([1., 2., 2., 2., 2., 1.])
    """
    if L <= 0:
        raise ValueError("L is strictly positive.")
    if X <= 0:
        raise ValueError("X is strictly positive.")
    if overlap < 0 or overlap > L:
        raise ValueError("overlap must be > 0 and <= L.")
    M = L * X - (X - 1) * overlap

    def _matmat(x):
        # x is always 2d
        y = np.full((M, x.shape[1]), 0.0 * x[0, 0], dtype=x.dtype)
        y[:L, :] = x[:L, :]
        offset = L - overlap
        for i in range(X - 1):
            y[offset:(offset + L), :] += x[((i + 1) * L):((i + 2) * L), :]
            offset += L - overlap
        return y

    def _rmatmat(x):
        # x is always 2d
        y = np.full((X * L, x.shape[1]), 0.0 * x[0, 0], dtype=x.dtype)
        for i in range(X):
            y[(i * L):((i + 1) * L), :] = x[(i * (L - overlap)):
                                            (i * (L - overlap) + L), :]
        return y

    return LazyLinOp(
        (M, X * L),
        matmat=lambda x: _matmat(x),
        rmatmat=lambda x: _rmatmat(x)
    )


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

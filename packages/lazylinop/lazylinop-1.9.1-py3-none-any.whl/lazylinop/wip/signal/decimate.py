import numpy as np
from lazylinop import LazyLinOp
import sys
sys.setrecursionlimit(100000)


def decimate(N: int, start: int = 0, end: int = None, every: int = 2):
    """Constructs a decimation lazy linear operator.
    The length of the output is ceil((end - start) / every).
    If the shape of the input array is (N, batch size) the operator
    has a shape = (ceil((end - start) / every), batch size).

    Args:
        N: int
            Length of the input.
        start: int, optional
            First element to keep, default is 0.
        end: int, optional
            Stop decimation (not included), default is None.
        every: int, optional
            Keep element every this number, default is 2.

    Returns:
        The decimation LazyLinOp

    Raises:
        ValueError
            every is < 1.
        ValueError
            start is < 0.
        ValueError
            start is >= number of elements along axis.
        ValueError
            end is > number of elements along axis.
        Exception
            end is <= start.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.signal import decimate
        >>> x = np.arange(10)
        >>> x
        array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> decimate(x.shape[0], 0, 10, every=2) @ x
        array([0, 2, 4, 6, 8])
        >>> X = np.arange(30).reshape((10, 3))
        >>> X
        array([[ 0,  1,  2],
               [ 3,  4,  5],
               [ 6,  7,  8],
               [ 9, 10, 11],
               [12, 13, 14],
               [15, 16, 17],
               [18, 19, 20],
               [21, 22, 23],
               [24, 25, 26],
               [27, 28, 29]])
        >>> decimate(X.shape[0], 0, 10, every=2) @ X
        array([[ 0,  1,  2],
               [ 6,  7,  8],
               [12, 13, 14],
               [18, 19, 20],
               [24, 25, 26]])
    """
    if every < 1:
        raise ValueError("every is < 1.")
    if start < 0:
        raise ValueError("start is < 0.")
    if start >= N:
        raise ValueError("start is >= number of elements along axis.")
    if end is not None:
        if end > N:
            raise ValueError("end is > number of elements along axis.")
        if end <= start:
            raise Exception("end is <= start.")

    def _matmat(x, start, end, every):
        # x is always 2d
        L = int(np.ceil((end - start) / every))
        return x[start + np.arange(L) * every, :]

    def _rmatmat(x, start, end, every):
        # x is always 2d
        y = np.zeros((end, x.shape[1]), dtype=x.dtype)
        indices = np.arange(x.shape[0])
        y[start + indices * every, :] = x[indices, :]
        return y

    last = N if end is None else end
    L = int(np.ceil((last - start) / every))
    return LazyLinOp(
        shape=(L, N),
        matmat=lambda x: _matmat(x, start, last, every),
        rmatmat=lambda x: _rmatmat(x, start, last, every)
    )


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

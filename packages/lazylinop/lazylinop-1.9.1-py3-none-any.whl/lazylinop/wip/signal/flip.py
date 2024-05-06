import numpy as np
from lazylinop import LazyLinOp
import sys
sys.setrecursionlimit(100000)


def flip(shape: tuple, start: int = 0, end: int = None, axis: int = 0):
    """Constructs a flip lazy linear operator.

    Args:
        shape: tuple
        shape of the input
        start: int, optional
        flip from start (default is 0)
        end: int, optional
        stop flip (not included, default is None)
        axis: int, optional
        if axis=0 (default) flip per column, if axis=1 flip per row
        it does not apply if shape[1] is None.

    Returns:
        The flip LazyLinOp

    Raises:
        ValueError
            start is < 0.
        ValueError
            start is >= number of elements along axis.
        ValueError
            end is < 1.
        ValueError
            end is > number of elements along axis.
        Exception
            end is <= start.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.signal import flip
        >>> x = np.arange(6)
        >>> x
        array([0, 1, 2, 3, 4, 5])
        >>> y = flip(x.shape, 0, 5) @ x
        >>> y
        array([4, 3, 2, 1, 0, 5])
        >>> z = flip(x.shape, 2, 4) @ x
        >>> z
        array([0, 1, 3, 2, 4, 5])
        >>> X = np.eye(5, M=5, k=0)
        >>> X
        array([[1., 0., 0., 0., 0.],
               [0., 1., 0., 0., 0.],
               [0., 0., 1., 0., 0.],
               [0., 0., 0., 1., 0.],
               [0., 0., 0., 0., 1.]])
        >>> flip(X.shape, 1, 4) @ X
        array([[1., 0., 0., 0., 0.],
               [0., 0., 0., 1., 0.],
               [0., 0., 1., 0., 0.],
               [0., 1., 0., 0., 0.],
               [0., 0., 0., 0., 1.]])
    """
    N = shape[0]
    A = N
    if len(shape) == 2:
        M = shape[1]

    if start < 0:
        raise ValueError("start is < 0.")
    if start >= A:
        raise ValueError("start is >= number of elements along axis.")
    if end is not None and end < 1:
        raise ValueError("end is < 1.")
    if end is not None and end > A:
        raise ValueError("end is > number of elements along axis.")
    if end is not None and end <= start:
        raise Exception("end is <= start.")

    def _matmat(x, start, end):
        # x is always 2d
        y = np.copy(x)
        y[start:end, :] = x[end - 1 - np.arange(end - start), :]
        return y

    return LazyLinOp(
        shape=(N, N),
        matmat=lambda x: _matmat(x, start, N if end is None else end),
        rmatmat=lambda x: _matmat(x, start, N if end is None else end)
    )


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

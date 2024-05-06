import numpy as np
from lazylinop import LazyLinOp
import sys
sys.setrecursionlimit(100000)


def mslices(shape: tuple, start: np.ndarray, end: np.ndarray):
    """Constructs a multiple slices lazy linear operator.
    Element start[i] must be lesser than element end[i].
    Element end[i] must be greater or equal than element start[i - 1].
    If start[i] = end[i], extract only one element.

    Args:
        shape: tuple
            Shape of the input.
        start: np.ndarray
            List of first element to keep.
        end: np.ndarray
            List of last element to keep.

    Returns:
        The multiple slices LazyLinOp

    Raises:
        Exception
            start and end do not have the same length.
        ValueError
            start must be positive.
        ValueError
            end must be strictly positive.
        Exception
            end must be >= start.
        Exception
            start must be < shape[0].
        Exception
            end must be < shape[0].
        Exception
            start is empty.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.signal import mslices
        >>> x = np.arange(10)
        >>> x
        array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> mslices(x.shape, [0, 5], [2, 8]) @ x
        array([0, 1, 2, 5, 6, 7, 8])
    """
    if type(start) is list:
        start = np.asarray(start)
    if type(end) is list:
        end = np.asarray(end)
    S = start.shape[0]
    E = end.shape[0]
    if S != E:
        raise Exception("start and end do not have the same length.")
    if S == 0:
        raise Exception("start is empty.")

    L = 0
    for s in range(S):
        if start[s] < 0:
            raise ValueError("start must be positive.")
        if end[s] < 0:
            raise ValueError("end must be strictly positive.")
        if end[s] < start[s]:
            raise Exception("end must be >= start.")
        if start[s] >= shape[0]:
            raise Exception("start must be < shape[0].")
        if end[s] >= shape[0]:
            raise Exception("end must be < shape[0].")
        L += end[s] - start[s] + 1

    def _matmat(x, start, end):
        # x is always 2d
        y = np.empty((L, x.shape[1]), dtype=x.dtype)
        offset = 0
        for s in range(S):
            y[offset:(offset + end[s] - start[s] + 1), :] = (
                x[start[s]:(end[s] + 1), :]
            )
            offset += end[s] - start[s] + 1
        return y

    def _rmatmat(x, start, end):
        # x is always 2d
        y = np.zeros((shape[0], x.shape[1]), dtype=x.dtype)
        offset = 0
        for s in range(S):
            y[start[s]:(end[s] + 1), :] = (
                x[offset:(offset + end[s] - start[s] + 1), :]
            )
            offset += end[s] - start[s] + 1
        return y

    return LazyLinOp(
        shape=(L, shape[0]),
        matmat=lambda x: _matmat(x, start, end),
        rmatmat=lambda x: _rmatmat(x, start, end)
    )


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

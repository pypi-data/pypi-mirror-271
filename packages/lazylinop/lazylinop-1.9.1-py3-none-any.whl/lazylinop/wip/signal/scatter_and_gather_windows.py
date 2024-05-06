import numpy as np
from lazylinop import eye, hstack, LazyLinOp, vstack
import sys
sys.setrecursionlimit(100000)


def scatter_and_gather_windows(N: int, window: int, nhop: int):
    r"""Constructs a scatter and gather windows lazy linear operator.
    For a given signal, window size (window) and number of
    elements (nhop) between two consecutive windows the
    lazy linear operator concatenates the windows into a
    signal that is larger than the original one. The number
    of windows is given by 1 + (signal length - window) // nhop.
    Therefore, the length of the output signal is nwindows * window.
    If batch greater than 1, apply to each column.

    Args:
        N: int
            Length of the input array.
        window: int
            Size of the window.
        nhop: int
            Number of elements between two windows.

    Return:
        LazyLinOp

    Raises:
        ValueError
            window argument expects a value > 0 and <= signal length.
        ValueError
            nhop argument expects a value > 0 and <= window.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.signal import scatter_and_gather_windows
        >>> x = np.array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9.])
        >>> scatter_and_gather_windows(x.shape[0], 5, 2) @ x
        array([0., 1., 2., 3., 4., 2., 3., 4., 5., 6., 4., 5., 6., 7., 8.])
        >>> X = x.reshape(5, 2)
        >>> X
        array([[0., 1.],
               [2., 3.],
               [4., 5.],
               [6., 7.],
               [8., 9.]])
        >>> scatter_and_gather_windows(X.shape[0], 3, 2) @ X
        array([[0., 1.],
               [2., 3.],
               [4., 5.],
               [4., 5.],
               [6., 7.],
               [8., 9.]])

    .. seealso::
        `stft function <https://faustgrp.gitlabpages.inria.fr/lazylinop/
        api_signal.html#lazylinop.wip.signal.stft>`_.
    """

    if window <= 0 or window > N:
        raise ValueError("window argument expects a value > 0" +
                         " and <= signal length.")
    if nhop <= 0 or nhop > window:
        raise ValueError("nhop argument expects a value > 0 and <= window.")

    # number of windows in the original signal
    nwindows = 1 + (N - window) // nhop

    def _matmat(window, nhop, x):
        # x is always 2d
        Op = eye(window, n=N, k=0)
        for i in range(1, nwindows, 1):
            Op = vstack((Op, eye(window, n=N, k=i * nhop)))
        return Op @ x

    def _rmatmat(window, nhop, x):
        # x is always 2d
        Op = eye(N, n=window, k=0)
        for i in range(1, nwindows, 1):
            Op = hstack((Op, eye(N, n=window, k=-i * nhop)))
        return Op @ x

    return LazyLinOp(
        shape=(nwindows * window, N),
        matmat=lambda x: _matmat(window, nhop, x),
        rmatmat=lambda x: _rmatmat(window, nhop, x)
    )


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

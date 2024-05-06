import numpy as np
from lazylinop import LazyLinOp
from lazylinop import eye, hstack, LazyLinOp, vstack
import sys
sys.setrecursionlimit(100000)


def slices(N: int, start: np.ndarray,
           end: np.ndarray, window: int = None,
           nhop: int = None, offset: tuple = (0, None)):
    """Constructs a multiple slices lazy linear operator.

    - If window and hop are :code:`None` (default) extract slices
      given by the intervals [start[i], end[i]] for all i < len(start).
      Element start[i] must be lesser than element end[i].
      Element end[i] must be greater or equal than element start[i - 1].
      If start[i] = end[i], extract only one element.

    - If window and nhop are not :code:`None` extract slices given by
      window and nhop arguments.
      For a given signal, window size (window) and number of
      elements (nhop) between two consecutive windows the
      lazy linear operator concatenates the windows into a
      signal that could be larger than the original one. The number
      of windows is given by 1 + (signal length - window) // nhop.
      Therefore, the length of the output signal is nwindows * window.

    If batch greater than 1, apply to each column.

    Args:
        N: int
            Length of the input.
        start: np.ndarray
            List of first element to keep.
        end: np.ndarray
            List of last element to keep.
        window: int, optional
            Size of the window.
        nhop: int, optional
            Number of elements between two windows.
        offset: tuple, optional
            First element to keep, default is 0.
            Last element to keep, default is None.

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
            start must be < N.
        Exception
            end must be < N.
        Exception
            start is empty.
        ValueError
            window argument expects a value > 0 and <= signal length.
        ValueError
            nhop argument expects a value > 0.
        ValueError
            offset[0] is < 0.
        ValueError
            offset[0] >= number of elements.
        ValueError
            offset[1] > number of elements.
        Exception
            offset[1] is <= offset[0].

    Examples:
        >>> import numpy as np
        >>> import lazylinop as lz
        >>> # use list to extract multiple slices
        >>> x = np.arange(10)
        >>> x
        array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> lz.wip.signal.slices(x.shape[0], [0, 5], [2, 8]) @ x
        array([0, 1, 2, 5, 6, 7, 8])
        >>> # use window = 1 and nhop
        >>> x = np.arange(10)
        >>> x
        array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> lz.wip.signal.slices(x.shape[0], [], [], 1, 2, (0, 10)) @ x
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
        >>> lz.wip.signal.slices(x.shape[0], [], [], 1, 2, (0, 10)) @ X
        array([[ 0,  1,  2],
               [ 6,  7,  8],
               [12, 13, 14],
               [18, 19, 20],
               [24, 25, 26]])
        >>> # use window > 1 and nhop
        >>> x = np.array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9.])
        >>> lz.wip.signal.slices(x.shape[0], [], [], 5, 2) @ x
        array([0., 1., 2., 3., 4., 2., 3., 4., 5., 6., 4., 5., 6., 7., 8.])
        >>> X = x.reshape(5, 2)
        >>> X
        array([[0., 1.],
               [2., 3.],
               [4., 5.],
               [6., 7.],
               [8., 9.]])
        >>> lz.wip.signal.slices(X.shape[0], [], [], 3, 2) @ X
        array([[0., 1.],
               [2., 3.],
               [4., 5.],
               [4., 5.],
               [6., 7.],
               [8., 9.]])
    """

    if window is not None and nhop is not None:
        if window <= 0 or window > N:
            raise ValueError("window argument expects a value > 0" +
                             " and <= signal length.")
        if nhop <= 0:
            raise ValueError("nhop argument expects a value > 0.")

        if window == 1:
            # Decimation every nhop elements
            if offset[0] < 0:
                raise ValueError("offset[0] is < 0.")
            if offset[0] >= N:
                raise ValueError("offset[0] >= number of elements.")
            if offset[1] is not None:
                if offset[1] > N:
                    raise ValueError("offset[1] > number of elements.")
                if offset[1] <= offset[0]:
                    raise Exception("offset[1] is <= offset[0].")

            def _matmat(x, a, b, every):
                # x is always 2d
                L = int(np.ceil((b - a) / every))
                return x[a + np.arange(L) * every, :]

            def _rmatmat(x, a, b, every):
                # x is always 2d
                y = np.zeros((N, x.shape[1]), dtype=x.dtype)
                indices = np.arange(x.shape[0])
                y[a + indices * every, :] = x[indices, :]
                return y

            M = N if offset[1] is None else offset[1]
            return LazyLinOp(
                shape=(int(np.ceil((M - offset[0]) / nhop)), N),
                matmat=lambda x: _matmat(x, offset[0], M, nhop),
                rmatmat=lambda x: _rmatmat(x, offset[0], M, nhop)
            )
        else:
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
    else:
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
            if start[s] >= N:
                raise Exception("start must be < N.")
            if end[s] >= N:
                raise Exception("end must be < N.")
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
            y = np.zeros((N, x.shape[1]), dtype=x.dtype)
            offset = 0
            for s in range(S):
                y[start[s]:(end[s] + 1), :] = (
                    x[offset:(offset + end[s] - start[s] + 1), :]
                )
                offset += end[s] - start[s] + 1
            return y

        return LazyLinOp(
            shape=(L, N),
            matmat=lambda x: _matmat(x, start, end),
            rmatmat=lambda x: _rmatmat(x, start, end)
        )


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

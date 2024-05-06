import numpy as np
import scipy as sp
from lazylinop import LazyLinOp
from lazylinop.basicops import eye
from lazylinop.basicops import mpad
from lazylinop.basicops import vstack
from lazylinop.wip.signal import anti_eye
from lazylinop.wip.signal import fft
from lazylinop.wip.signal import slices
import sys
import warnings
sys.setrecursionlimit(100000)
warnings.simplefilter(action='always')


def dst(N, type: int = 2, n: int = None, norm: str = 'backward',
        workers: int = None, orthogonalize: bool = None,
        backend: str = 'scipy'):
    """
    Returns a :class:`.LazyLinOp` for the DST of size N.

    If the input array is a batch of vectors,
    apply DST per column. The function provides two
    backends. One is based on the DST from SciPy
    while the other one builds DST from lazylinop
    building blocks.

    Args:
        N: int
            Size of the input (N > 0).
        type: int, optional
            Defaut is 2.
            See `SciPy DST <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dst.html#scipy-fft-dst>`_ for more details.
        n: int, optional
            Default is None.
            See `SciPy DST <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dst.html#scipy-fft-dst>`_ for more details.
        norm: str, optional
            Default is 'backward'.
            See `SciPy DST <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dst.html#scipy-fft-dst>`_ for more details.
        workers: int, optional
            Default is None.
            It only works when ``backend='lazylinop'``.
            See `SciPy DST <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dst.html#scipy-fft-dst>`_ for more details.
        orthogonalize: bool, optional
            Default is None.
            See `SciPy DST <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dst.html#scipy-fft-dst>`_ for more details.
        backend: str, optional
            - ``'scipy'`` (default) uses ``scipy.fft.dst`` to compute DST.
            - ``'lazylinop'`` uses building-blocks to compute DST.
            lazylinop backend computation of ``L @ x`` is equivalent to
            ``sp.fft.dst(x, type, n, 0, norm, False, 1, orthogonalize)``.

    Returns:
        :class:`.LazyLinOp`

    Raises:
        Exception
            DST I: N and n must be > 1.
        Exception
            N and n must be >= 1.
        ValueError
            norm must be either 'backward', 'ortho' or 'forward'.
        ValueError
            type must be either 1, 2, 3 or 4.

    Example:
        >>> import lazylinop as lz
        >>> import numpy as np
        >>> import scipy as sp
        >>> F = lz.wip.signal.dst(32)
        >>> x = np.random.rand(32)
        >>> y = sp.fft.dst(x)
        >>> np.allclose(F @ x, y)
        True

    .. seealso::
        `Wikipedia <https://en.wikipedia.org/wiki/Discrete_sine_transform>`_,
        `SciPy DST <https://docs.scipy.org/doc/scipy/,
        reference/generated/ scipy.fft.dst.html#scipy-fft-dst>`_,
        `SciPy DSTn <https://docs.scipy.org/doc/scipy/reference/
        generated/scipy.fft.dstn.html>`_.
    """

    if backend == 'scipy':
        return _scipy_dst(N, type, n, norm, workers, orthogonalize)

    # Length of the output
    M = N if n is None else n

    if (N <= 1 or M <= 1) and type == 1:
        raise Exception("DST I: N and n must be > 1.")
    if N < 1 or M < 1:
        raise Exception("N and n must be >= 1.")

    if norm not in ['ortho', 'forward', 'backward']:
        raise ValueError("norm must be either 'backward'," +
                         " 'ortho' or 'forward'.")

    if type == 1:
        # L @ x is equivalent to
        # sp.fft.dst(x, 1, n, 0, norm, False, 1, orthogonalize)
        # up to a scale factor depending on norm.
        S1 = slices(2 * (M + 1), start=[1], end=[M])
        F = fft(2 * (M + 1))
        L = S1 @ F @ vstack((eye(M + 2, n=M, k=-1),
                             -anti_eye(M)))
    elif type == 2:
        # L @ x is equivalent to
        # sp.fft.dst(x, 2, n, 0, norm, False, 1, orthogonalize)
        # up to a scale factor depending on norm.
        # Append -flip(x) to the original input x.
        # Interleave with zeros such that the first element is zero.
        # Compute the DFT of length 4 * M and keep first M elements.
        S1 = slices(4 * M, start=[1], end=[M])
        F = fft(4 * M)
        P = mpad(1, 2 * M, 1, ('before'))
        L = S1 @ F @ P @ vstack((eye(M, n=M, k=0),
                                 -anti_eye(M)))
        if orthogonalize:
            # Divide last element of the output by sqrt(2).
            L = _mult_xi(M, [M - 1], [1.0 / np.sqrt(2.0)]) @ L
    elif type == 3:
        # L @ x is equivalent to
        # sp.fft.dst(x, 3, n, 0, norm, False, 1, orthogonalize)
        # up to a scale factor depending on norm.
        # type 3 is transpose of type 2 if last element
        # of x is multiplied by 1 / 2 if not orthogonalize,
        # sqrt(2) / 2 if orthogonalize.
        S1 = slices(4 * M, start=[1], end=[M])
        F = fft(4 * M)
        P = mpad(1, 2 * M, 1, ('before'))
        L = (S1 @ F @ P @ vstack((eye(M, n=M, k=0),
                                  -anti_eye(M)))).T
        Q = _mult_xi(M, [M - 1],
                     [0.5 * (np.sqrt(2.0) if orthogonalize else 1.0)])
        L = L @ Q
    elif type == 4:
        # L @ x is equivalent to
        # sp.fft.dst(x, 4, n, 0, norm, False, 1, orthogonalize)
        # up to a scale factor depending on norm.
        # Append flip(x), -x and -flip(x) to the original input x.
        # Interleave with zeros such that the first element is zero.
        # Compute the DFT of length 8 * M and keep M odd elements.
        S1 = slices(8 * M,
                    start=np.arange(1, 2 * M + 1, 2),
                    end=np.arange(1, 2 * M + 1, 2))
        F = fft(8 * M)
        P = mpad(1, 4 * M, 1, ('before'))
        L = 0.5 * (
            S1 @ F @ P @ vstack(
                (
                    vstack((eye(M, n=M, k=0),
                            anti_eye(M))),
                    vstack((-eye(M, n=M, k=0),
                            -anti_eye(M)))
                )
            )
        )
    else:
        raise ValueError("type must be either 1, 2, 3 or 4.")

    if M != N:
        # Pad with zero or truncate the input
        L = L @ eye(M, N, k=0)

    if norm == 'ortho':
        scale = [
            np.sqrt(2 * (L.shape[0] + 1)),
            np.sqrt(2 * L.shape[0]),
            np.sqrt(2 * L.shape[0]),
            np.sqrt(2 * L.shape[0])
        ]
    if norm == 'forward':
        scale = [
            2 * (L.shape[0] + 1),
            2 * L.shape[0],
            2 * L.shape[0],
            2 * L.shape[0]
        ]

    # Use a function to apply scale factor
    # and orthogonalize if True.
    def _matmat(L, x):
        _dtype_sanitized_x(x, 'dst')
        y = -np.imag(L @ x)
        if norm == 'ortho' or norm == 'forward':
            y /= scale[type - 1]
        return y

    return LazyLinOp(
        shape=(L.shape[0], N),
        matmat=lambda x: _matmat(L, x),
        rmatmat=lambda x: _matmat(L.H, x),
        dtype='float'
    )


def _scipy_dst(N, type: int = 2, n: int = None, norm: str = 'backward',
               workers: int = None, orthogonalize: bool = None):
    """
    Returns a LazyLinOp for the DST of size N.
    If the input array is a batch of vectors,
    apply DST per column.

    Args:
        N: int
            Size of the input (N > 0).
        type: int, optional
            Defaut is 2.
            See `SciPy DST <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dst.html#scipy-fft-dst>`_ for more details.
        n: int, optional
            Default is None.
            See `SciPy DST <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dst.html#scipy-fft-dst>`_ for more details.
        norm: str, optional
            Default is 'backward'.
            See `SciPy DST <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dst.html#scipy-fft-dst>`_ for more details.
        workers: int, optional
            Default is None
            See `SciPy DST <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dst.html#scipy-fft-dst>`_ for more details.
        orthogonalize: bool, optional
            Default is None.
            See `SciPy DST <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dst.html#scipy-fft-dst>`_ for more details.

    Returns:
        LazyLinOp

    Raises:
        ValueError
            norm must be either 'backward', 'ortho' or 'forward'.
        ValueError
            type must be either 1, 2, 3 or 4.

    .. seealso::
        `SciPy DST <https://docs.scipy.org/doc/scipy/
        reference/generated/ scipy.fft.dst.html#scipy-fft-dst>`_.
        `SciPy DSTn <https://docs.scipy.org/doc/scipy/reference/
        generated/scipy.fft.dstn.html>`_.
    """

    # Length of the output
    M = N if n is None else n

    if norm == 'ortho':
        scale = 1
    elif norm == 'forward':
        scale = 1 / M
    elif norm == 'backward':
        scale = M
    else:
        raise ValueError("norm must be either 'backward'," +
                         " 'ortho' or 'forward'.")

    n_workers = -1 if workers is None else workers

    if (not np.isscalar(type) or type - np.floor(type) != 0
       or type < 1 or type > 4):
        raise ValueError("type must be either 1, 2, 3 or 4.")

    def _matmat(x):
        _dtype_sanitized_x(x, 'dst')
        # x is always 2d
        return sp.fft.dstn(x, type, (None), 0, norm,
                           False, n_workers, orthogonalize=orthogonalize)


    def _rmatmat(x):
        _dtype_sanitized_x(x, 'dst')
        # x is always 2d
        return sp.fft.idstn(x, type, (None), 0, norm, False,
                             n_workers, orthogonalize=orthogonalize) * scale

    L = LazyLinOp(
        shape=(M, M),
        matmat=lambda x: _matmat(x),
        rmatmat=lambda x: _rmatmat(x),
        dtype='float'
    )

    # Pad or truncate the input with the help of lazylinop.
    # Therefore, do not modify sp.fft.(i)dst(n) argument n=None.
    return L @ eye(M, N, k=0) if M != N else L


def _mult_xi(N, idx, a):
    """Constructs a LazyLinOp that multiplies some of the elements
    of an input array by a factor and left unchanged the others.

    Args:
        N: int
            Length of the input array.
        idx: list
            List of indices.
        a: list
            List of factors.

    Returns:
        LazyLinOp
    """

    def _matmat(x):
        # x is always 2d
        y = np.copy(x)
        for i, v in enumerate(idx):
            y[v, :] *= a[i]
        return y

    return LazyLinOp(
        shape=(N, N),
        matmat=lambda x: _matmat(x),
        rmatmat=lambda x: _matmat(x)
    )


def _dtype_sanitized_x(x, func):
    if 'complex' in str(x.dtype):
        # do not use np.iscomplex
        # x can not be a numpy array
        # (e.g. x a scipy mat)
        raise ValueError(str(func)+" is a real function but x is not real")
    return x


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

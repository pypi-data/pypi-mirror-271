import numpy as np
import scipy as sp
from lazylinop import LazyLinOp
from lazylinop.basicops import eye
from lazylinop.basicops import mpad
from lazylinop.basicops import vstack
from lazylinop.wip.signal import anti_eye
from lazylinop.wip.signal import fft
from lazylinop.wip.signal import slices
from lazylinop.wip.signal.dst import _mult_xi, _dtype_sanitized_x
import sys
import warnings
sys.setrecursionlimit(100000)
warnings.simplefilter(action='always')


def dct(N, type: int = 2, n: int = None, norm: str = 'backward',
        workers: int = None, orthogonalize: bool = None,
        backend: str = 'scipy'):
    """
    Returns a :class:`.LazyLinOp` for the DCT of size N.

    If the input array is a batch of vectors,
    apply DCT per column. The function provides two
    backends. One is based on the DCT from SciPy
    while the other one builds DCT from lazylinop
    building blocks.

    Args:
        N: int
            Size of the input (N > 0).
        type: int, optional
            Defaut is 2.
            See `SciPy DCT <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dct.html#scipy-fft-dct>`_ for more details.
        n: int, optional
            Default is None.
            See `SciPy DCT <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dct.html#scipy-fft-dct>`_ for more details.
        norm: str, optional
            Default is 'backward'.
            See `SciPy DCT <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dct.html#scipy-fft-dct>`_ for more details.
        workers: int, optional
            Default is None
            See `SciPy DCT <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dct.html#scipy-fft-dct>`_ for more details.
        orthogonalize: bool, optional
            Default is None.
            See `SciPy DCT <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dct.html#scipy-fft-dct>`_ for more details.
        backend: str, optional
            - ``'scipy'`` (default) uses ``scipy.fft.dct`` to compute DCT.
            - ``'lazylinop'`` uses building-blocks to compute DCT.
            lazylinop backend computation of ``L @ x`` is equivalent to
            ``sp.fft.dct(x, type, n, 0, norm, False, 1, orthogonalize)``.

    Returns:
        :class:`.LazyLinOp`

    Raises:
        Exception
            DCT I: size of the input must be >= 2.
        ValueError
            norm must be either 'backward', 'ortho' or 'forward'.
        ValueError
            type must be either 1, 2, 3 or 4.

    Example:
        >>> import lazylinop as lz
        >>> import numpy as np
        >>> import scipy as sp
        >>> F = lz.wip.signal.dct(32)
        >>> x = np.random.rand(32)
        >>> y = sp.fft.dct(x)
        >>> np.allclose(F @ x, y)
        True

    .. seealso::
        `Wikipedia <https://en.wikipedia.org/
        wiki/Discrete_sine_transform>`_,
        `A fast cosine transform in one and two dimensions
        <https://ieeexplore.ieee.org/document/1163351>`_,
        `SciPy DCT <https://docs.scipy.org/doc/scipy/
        reference/generated/ scipy.fft.dct.html#scipy-fft-dct>`_,
        `SciPy DCTn <https://docs.scipy.org/doc/scipy/reference/
        generated/scipy.fft.dctn.html>`_.
    """

    if backend == 'scipy':
        return _scipy_dct(N, type, n, norm, workers, orthogonalize)

    # Length of the output
    M = N if n is None else n

    if norm not in ['ortho', 'forward', 'backward']:
        raise ValueError("norm must be either 'backward'," +
                         " 'ortho' or 'forward'.")

    if type == 1:
        # L @ x is equivalent to
        # sp.fft.dct(x, 1, n, 0, norm, False, 1, False)
        # up to a scale factor depending on norm.
        if M < 2:
            raise Exception("DCT I: size of the input must be >= 2.")
        S1 = slices(2 * (M - 1), start=[0], end=[M - 1])
        F = fft(2 * (M - 1))
        L = S1 @ F
        if M > 2:
            S2 = slices(M, start=[1], end=[M - 2])
            L = L @ vstack((eye(M, n=M, k=0),
                            anti_eye(M - 2) @ S2))
        if orthogonalize:
            L = L @ _mult_xi(M, [0, M - 1], [np.sqrt(2.0)] * 2)
            L = _mult_xi(M, [0, M - 1], [1.0 / np.sqrt(2.0)] * 2) @ L
    elif type == 2:
        # L @ x is equivalent to
        # sp.fft.dct(x, 2, n, 0, norm, False, 1, False)
        # Append flip(x) to the original input x.
        # Interleave with zeros such that the first element is zero.
        # Compute the DFT of length 4 * M and keep first M elements.
        S1 = slices(4 * M, start=[0], end=[M - 1])
        F = fft(4 * M)
        P = mpad(1, 2 * M, 1, ('before'))
        L = S1 @ F @ P @ vstack((eye(M, n=M, k=0),
                                 anti_eye(M)))
        if orthogonalize:
            # Divide first element of the output by sqrt(2).
            L = _mult_xi(M, [0], [1.0 / np.sqrt(2.0)]) @ L
    elif type == 3:
        # L @ x is equivalent to
        # sp.fft.dct(x, 3, n, 0, norm, False, 1, False)
        # up to a scale factor depending on norm.
        # type 3 is transpose of type 2 if first element
        # of x is divided by 2.
        S1 = slices(4 * M, start=[0], end=[M - 1])
        F = fft(4 * M)
        P = mpad(1, 2 * M, 1, ('before'))
        L = (S1 @ F @ P @ (
            vstack((eye(M, n=M, k=0),
                    anti_eye(M))))).T @ _mult_xi(M, [0], [0.5])
        if orthogonalize:
            L = L @ _mult_xi(M, [0], [np.sqrt(2.0)])
    elif type == 4:
        # L @ x is equivalent to
        # sp.fft.dct(x, 4, n, 0, norm, False, 1, False)
        # Append -flip(x), -x and flip(x) to the original input x.
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
                            -anti_eye(M))),
                    vstack((-eye(M, n=M, k=0),
                            anti_eye(M)))
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
            np.sqrt(2 * (L.shape[0] - 1)),
            np.sqrt(2 * L.shape[0]),
            np.sqrt(2 * L.shape[0]),
            np.sqrt(2 * L.shape[0])
        ]
    elif norm == 'forward':
        scale = [
            2 * (L.shape[0] - 1),
            2 * L.shape[0],
            2 * L.shape[0],
            2 * L.shape[0]
        ]
    else:
        scale = [1.0] * 4

    return LazyLinOp(
        shape=(L.shape[0], N),
        matmat=lambda x: (
            np.real(L @ _dtype_sanitized_x(x, 'dct')) if norm == 'backward'
            else np.real(L @ _dtype_sanitized_x(x, 'dct')) / scale[type - 1]
        ),
        rmatmat=lambda x: np.real(L.T @ x),
        dtype='float'
    )


def _scipy_dct(N, type: int = 2, n: int = None, norm: str = 'backward',
               workers: int = None, orthogonalize: bool = None):
    """
    Returns a LazyLinOp for the DCT of size N.
    If the input array is a batch of vectors,
    apply DCT per column.

    Args:
        N: int
            Size of the input (N > 0).
        type: int, optional
            Defaut is 2.
            See `SciPy DCT <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dct.html#scipy-fft-dct>`_ for more details.
        n: int, optional
            Default is None.
            See `SciPy DCT <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dct.html#scipy-fft-dct>`_ for more details.
        norm: str, optional
            Default is 'backward'.
            See `SciPy DCT <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dct.html#scipy-fft-dct>`_ for more details.
        workers: int, optional
            Default is None
            See `SciPy DCT <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dct.html#scipy-fft-dct>`_ for more details.
        orthogonalize: bool, optional
            Default is None.
            See `SciPy DCT <https://docs.scipy.org/doc/scipy/
            reference/generated/
            scipy.fft.dct.html#scipy-fft-dct>`_ for more details.

    Returns:
        LazyLinOp

    Raises:
        ValueError
            norm must be either 'backward', 'ortho' or 'forward'.
        ValueError
            type must be either 1, 2, 3 or 4.

    .. seealso::
        `SciPy DCT <https://docs.scipy.org/doc/scipy/
        reference/generated/ scipy.fft.dct.html#scipy-fft-dct>`_.
        `SciPy DCTn <https://docs.scipy.org/doc/scipy/reference/
        generated/scipy.fft.dctn.html>`_.
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
        _dtype_sanitized_x(x, 'dct')
        # x is always 2d
        return sp.fft.dctn(x, type, (None), 0, norm,
                           False, n_workers, orthogonalize=orthogonalize)

    def _rmatmat(x):
        _dtype_sanitized_x(x, 'dct')
        # x is always 2d
        return sp.fft.idctn(x, type, (None), 0, norm, False,
                            n_workers, orthogonalize=orthogonalize) * scale

    L = LazyLinOp(
        shape=(M, M),
        matmat=lambda x: _matmat(x),
        rmatmat=lambda x: _rmatmat(x),
        dtype='float'
    )

    # Pad or truncate the input with the help of lazylinop.
    # Therefore, do not modify sp.fft.(i)dct(n) argument n=None.
    return L @ eye(M, N, k=0) if M != N else L

# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

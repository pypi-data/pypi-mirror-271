import numpy as np
from lazylinop import binary_dtype, LazyLinOp, zeros


def anti_eye(m: int, n: int = None, k: int = 0, dtype: str = 'float'):
    """Constructs a :class:`.LazyLinOp` whose equivalent array is filled with
    ones on the k-th antidiagonal and zeros everywhere else.

    ``L = anti_eye(m, n, k)`` is such that ``L.toarray() ==
    numpy.flip(numpy.eye(m, n, k), axis=1)``.

    Args:
        m: ``int``
            Number of rows.
        n: ``int``, optional
            Number of columns (default is ``m``).
        k: ``int``, optional
            Anti-diagonal to place ones on.

            - zero for the main antidiagonal (default),
            - positive integer for an upper antidiagonal.
            - negative integer for a lower antidiagonal,

            if ``k >= n`` or ``k <= - m`` then ``anti_eye(m, n, k)`` is
            ``zeros((m, n))`` (k-th antidiagonal is out of operator shape).

        dtype: ``str`` or ``numpy.dtype``, optional
            Defaultly ``'float'``.

    Returns:
        The anti-eye :class:`.LazyLinOp`.

    Raises:
        ValueError
            "m and n must be >= 1."

    Examples:
        >>> import lazylinop as lz
        >>> import numpy as np
        >>> x = np.arange(3)
        >>> L = lz.wip.signal.anti_eye(3)
        >>> np.allclose(L @ x, np.flip(x))
        True
        >>> L = lz.wip.signal.anti_eye(3, n=3, k=0)
        >>> L.toarray()
        array([[0., 0., 1.],
               [0., 1., 0.],
               [1., 0., 0.]])
        >>> L = lz.wip.signal.anti_eye(3, n=3, k=1)
        >>> L.toarray()
        array([[0., 1., 0.],
               [1., 0., 0.],
               [0., 0., 0.]])
        >>> L = lz.wip.signal.anti_eye(3, n=3, k=-1)
        >>> L.toarray()
        array([[0., 0., 0.],
               [0., 0., 1.],
               [0., 1., 0.]])
        >>> L = lz.wip.signal.anti_eye(3, n=4, k=0)
        >>> L.toarray()
        array([[0., 0., 0., 1.],
               [0., 0., 1., 0.],
               [0., 1., 0., 0.]])
        >>> L = lz.wip.signal.anti_eye(3, n=4, k=1)
        >>> L.toarray()
        array([[0., 0., 1., 0.],
               [0., 1., 0., 0.],
               [1., 0., 0., 0.]])
        >>> L = lz.wip.signal.anti_eye(3, n=4, k=-1)
        >>> L.toarray()
        array([[0., 0., 0., 0.],
               [0., 0., 0., 1.],
               [0., 0., 1., 0.]])

    .. seealso::
        :py:func:`.eye`,
        :py:func:`.LazyLinOp.toarray`,
        `numpy.eye
        <https://numpy.org/doc/stable/reference/generated/numpy.eye.html>`_,
        `numpy.flip
        <https://numpy.org/doc/stable/reference/generated/numpy.flip.html>`_.
    """
    nn = m if n is None else n
    if m < 1 or nn < 1:
        raise ValueError("m and n must be >= 1.")

    if k >= nn or k <= - m:
        # diagonal is out of shape
        # return zeros LazyLinOp
        return zeros((m, nn))

    def _matmat(x, m, n, k):
        # x is always 2d
        out_dtype = binary_dtype(dtype, x.dtype)
        y = np.zeros((m, x.shape[1]), dtype=x.dtype)
        if k == 0:
            # Main anti-diagonal
            nr = min(m, n)
            y[:nr, :] = x[-1:- 1 - nr:-1]
        elif k > 0:
            # Above anti-diagonal
            # k <= n
            nr = max(0, min(m, n - k))
            y[:nr] = x[-1 - k:-1 - k - nr:-1]
        else:
            # Below anti-diagonal (k < 0)
            nr = max(0, min(m + k, n))
            y[-k:-k+nr] = x[-1:- 1 - nr:-1]
        return y.astype(out_dtype)

    return LazyLinOp(
        shape=(m, nn),
        matmat=lambda x: _matmat(x, m, nn, k),
        rmatmat=lambda x: _matmat(x, nn, m, k),
        dtype=dtype
    )

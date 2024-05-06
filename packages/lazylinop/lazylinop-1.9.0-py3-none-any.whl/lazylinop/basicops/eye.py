from lazylinop import LazyLinOp, binary_dtype
from scipy.sparse import issparse, vstack as svstack, csr_matrix as szeros
import numpy as np


def eye(m, n=None, k=0, dtype='float'):
    """
    Returns the :class:`LazyLinOp` for eye (identity matrix and variants).

    Args:
        m: ``int``
            Number of rows.
        n: ``int``, optional
             Number of columns. Default is ``m``.
        k: ``int``, optional
             Diagonal to place ones on.

             - zero for the main diagonal (default),
             - positive integer for an upper diagonal,
             - negative integer for a lower diagonal.

        dtype: ``str`` or ``numpy.dtype``, optional
            Data type of the :class:`LazyLinOp` (Defaultly ``'float'``).

    Example:
        >>> import lazylinop as lz
        >>> le1 = lz.eye(5)
        >>> le1
        <5x5 LazyLinOp with dtype=float64>
        >>> le1.toarray()
        array([[1., 0., 0., 0., 0.],
               [0., 1., 0., 0., 0.],
               [0., 0., 1., 0., 0.],
               [0., 0., 0., 1., 0.],
               [0., 0., 0., 0., 1.]])
        >>> le2 = lz.eye(5, 2)
        >>> le2
        <5x2 LazyLinOp with dtype=float64>
        >>> le2.toarray()
        array([[1., 0.],
               [0., 1.],
               [0., 0.],
               [0., 0.],
               [0., 0.]])
        >>> le3 = lz.eye(5, 3, 1)
        >>> le3
        <5x3 LazyLinOp with dtype=float64>
        >>> le3.toarray()
        array([[0., 1., 0.],
               [0., 0., 1.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.]])
        >>> le4 = lz.eye(5, 3, -1)
        >>> le4
        <5x3 LazyLinOp with dtype=float64>
        >>> le4.toarray()
        array([[0., 0., 0.],
               [1., 0., 0.],
               [0., 1., 0.],
               [0., 0., 1.],
               [0., 0., 0.]])

        .. seealso::
            `scipy.sparse.eye <https://docs.scipy.org/doc/scipy/reference/
            generated/scipy.sparse.eye.html>`_,
            `numpy.eye <https://numpy.org/devdocs/reference/generated/
            numpy.eye.html>`_.
    """
    def matmat(x, m, n, k):
        # x is always 2d
        nonlocal dtype
        out_dtype = binary_dtype(dtype, x.dtype)
        # if eye is the identity just return x
        if k == 0 and m == n:
            return x
        minmn = min(m, n)
        if issparse(x):
            x = x.tocsr()
            _zeros = szeros
            _vstack = svstack
        else:
            _zeros = np.zeros
            _vstack = np.vstack
        if k < 0:
            neg_k = True
            nz = _zeros((abs(k), x.shape[1]), dtype=out_dtype)
            limk = min(minmn, m - abs(k))
            k = 0
        else:
            limk = min(minmn, n - k)
            neg_k = False
        mul = x[k: k + limk, :]
        if neg_k:
            mul = _vstack((nz, mul))
        if mul.shape[0] < m:
            z = _zeros((m - mul.shape[0], mul.shape[1]), dtype=out_dtype)
            t = (mul, z)
            mul = _vstack(t)
        return mul.astype(out_dtype)
    n = n if n is not None else m
    return LazyLinOp((m, n), matmat=lambda x: matmat(x, m, n, k),
                     rmatmat=lambda x: matmat(x, n, m, -k),
                     dtype=dtype)

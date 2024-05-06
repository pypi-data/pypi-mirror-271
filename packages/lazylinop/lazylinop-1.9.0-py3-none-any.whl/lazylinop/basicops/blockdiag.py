from lazylinop import binary_dtype, LazyLinOp, aslazylinops
import numpy as np


def block_diag(*ops):
    """
    Returns the block diagonal :class:`LazyLinOp` of operators ``ops``.

    Args:
        ops:
             The diagonal blocks as :class:`LazyLinOp`-s or other
             compatible linear operators.

    Returns:
        The diagonal block :class:`LazyLinOp`.

    Example:
        >>> import numpy as np
        >>> import lazylinop as lz
        >>> from lazylinop import aslazylinop
        >>> import scipy
        >>> nt = 10
        >>> d = 64
        >>> v = np.random.rand(d)
        >>> terms = [np.random.rand(64, 64) for _ in range(10)]
        >>> ls = lz.block_diag(*terms) # ls is the block diagonal LazyLinOp
        >>> np.allclose(scipy.linalg.block_diag(*terms), ls.toarray())
        True

    .. seealso::
        `scipy.linalg.block_diag <https://docs.scipy.org/doc/scipy/reference/
        generated/scipy.linalg.block_diag.html>`_,
        :func:`.aslazylinop`
    """

    ops = aslazylinops(*ops)

    def lAx(A, x):
        return A @ x

    def lAHx(A, x):
        return A.T.conj() @ x

    roffsets = [0]
    coffsets = [0]  # needed for transpose case
    for i in range(len(ops)):
        roffsets += [roffsets[i] + ops[i].shape[1]]
        coffsets += [coffsets[i] + ops[i].shape[0]]
        if i == 0:
            dtype = ops[0].dtype
        else:
            dtype = binary_dtype(dtype, ops[i].dtype)

    def matmat(x, lmul, offsets):
        # x is always 2d
        Ps = [None for _ in range(len(ops))]
        n = len(ops)
        # x can only be a numpy array or a scipy mat
        # hence Ps[i] is a numpy array whatever are ops
        for i, A in enumerate(ops):
            Ps[i] = lmul(A, x[offsets[i]:offsets[i+1]])
        S = Ps[0]
        for i in range(1, n):
            S = np.vstack((S, Ps[i]))
        return S

    return LazyLinOp((coffsets[-1], roffsets[-1]), matmat=lambda x:
                     matmat(x, lAx, roffsets),
                     rmatmat=lambda x: matmat(x, lAHx, coffsets),
                     dtype=dtype)

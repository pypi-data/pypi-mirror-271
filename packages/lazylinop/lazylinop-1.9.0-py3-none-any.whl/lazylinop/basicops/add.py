from lazylinop import LazyLinOp, aslazylinops


def add(*ops):
    r"""
    Returns a :class:`LazyLinOp` add of linear operators ``ops`` ($\sum_i
    ops[i]$).

    Args:
        ops: (compatible linear operators)
            Operators to add up.

    Returns:
        The :class:`LazyLinOp` for the sum of ops.

    Example:
        >>> import numpy as np
        >>> import lazylinop as lz
        >>> from lazylinop import aslazylinop
        >>> nt = 10
        >>> d = 8
        >>> v = np.random.rand(d)
        >>> terms = [np.ones((d, d)) for i in range(nt)]
        >>> # terms are all Fausts here
        >>> ls = lz.add(*terms) # ls is the LazyLinOp add of terms
        >>> np_sum = 0
        >>> for i in range(nt): np_sum += terms[i]
        >>> np.allclose(ls @ v, nt * np.ones((d, d)) @ v)
        True

    .. seealso::
        :func:`.aslazylinop`
    """

    def lAx(A, x):
        return A @ x

    def lAHx(A, x):
        return A.T.conj() @ x

    ops = aslazylinops(*ops)

    for i, op in enumerate(ops[1:]):
        if op.shape != ops[0].shape:
            raise ValueError('Dimensions must agree')

    def matmat(x, lmul):
        Ps = [None for _ in range(len(ops))]
        n = len(ops)
        for i, A in enumerate(ops):
            Ps[i] = lmul(A, x)
        S = Ps[-1]
        for i in range(n-2, -1, -1):
            S = S + Ps[i]
        return S

    return LazyLinOp(ops[0].shape, matmat=lambda x: matmat(x, lAx),
                     rmatmat=lambda x: matmat(x, lAHx))

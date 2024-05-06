import sys
from lazylinop.basicops import eye, vstack
from lazylinop.wip.signal import anti_eye

sys.setrecursionlimit(100000)


def bc(L: int, n: int = 1, bn: int = 0,
       an: int = 0, boundary: str = 'periodic'):
    r"""Builds a periodic or symmetric boundary condition :class:`.LazyLinOp`.

    For an input $x_1, x_2, \ldots, x_N$:

    - A symmetric boundary condition is such that:

      $x_N, ..., x_2, x_1 | x_1, x_2, ..., x_N | x_N, ..., x_2, x_1$

    - A periodic boundary condition is such that:

      $x_1, x_2, ..., x_N | x_1, x_2, ..., x_N | x_1, x_2, ..., x_N$

    If the input is a 2d array, it  works on each column and returns the
    resulting horizontal concatenation (a 2d-array).

    Args:
        L: ``int``
            Size of the input.
        n: ``int``, optional
            Duplicate the signal this number of times on both side.
        bn: ``int``, optional
            Add this number of elements before.
            It first adds n times the input to the left of the
            original input and then adds bn elements.
        an: ``int``, optional
            Add this number of elements after.
            It first adds n times the input to the right of the
            original input and then adds an elements.
        boundary: ``str``, optional
            ``'wrap'``/``'periodic'`` (default) or ``'symm'``/``'symmetric'``
            boundary condition.

    Returns:
        :class:`.LazyLinOp`

    Raises:
        ValueError
            L must be strictly positive.
        ValueError
            n must be >= 0.
        ValueError
            bn and an must be >= 0.
        ValueError
            bn and an must be <= L.
        ValueError
            boundary is either 'periodic' ('wrap') or 'symmetric' ('symm').

    Examples:
        >>> import lazylinop as lz
        >>> import numpy as np
        >>> N = 3
        >>> x = np.arange(N).astype(np.float_)
        >>> L = lz.wip.signal.bc(N, n=1, boundary='periodic')
        >>> L @ x
        array([0., 1., 2., 0., 1., 2., 0., 1., 2.])
        >>> L = lz.wip.signal.bc(N, n=1, boundary='symmetric')
        >>> L @ x
        array([2., 1., 0., 0., 1., 2., 2., 1., 0.])
        >>> X = np.array([[0., 0.], [1., 1.], [2., 2.]])
        >>> X
        array([[0., 0.],
               [1., 1.],
               [2., 2.]])
        >>> L @ X
        array([[2., 2.],
               [1., 1.],
               [0., 0.],
               [0., 0.],
               [1., 1.],
               [2., 2.],
               [2., 2.],
               [1., 1.],
               [0., 0.]])
        >>> L = lz.wip.signal.bc(N, n=1, bn=1, boundary='periodic')
        >>> L @ x
        array([2., 0., 1., 2., 0., 1., 2., 0., 1., 2.])
        >>> L = lz.wip.signal.bc(N, n=1, bn=2, an=1, boundary='symmetric')
        >>> L @ x
        array([1., 2., 2., 1., 0., 0., 1., 2., 2., 1., 0., 0.])

    .. seealso::
        :func:`.vstack`, :func:`.hstack`, :func:`.bc2d`
    """
    if L <= 0:
        raise ValueError("L must be strictly positive.")
    if n < 0:
        raise ValueError("n must be >= 0.")
    if bn < 0 or an < 0:
        raise ValueError("an and bn must be >= 0.")
    if bn > L or an > L:
        raise ValueError("bn and an must be <= L.")

    if boundary == 'symmetric' or boundary == 'symm':
        if (n % 2) == 0:
            Op = eye(L, n=L, k=0)
            flip = True
        else:
            Op = anti_eye(L) @ eye(L, n=L, k=0)
            flip = False
        for i in range(1, n + 1 + n):
            if flip:
                Op = vstack((Op, anti_eye(L) @ eye(L, n=L, k=0)))
                flip = False
            else:
                Op = vstack((Op, eye(L, n=L, k=0)))
                flip = True
        if bn > 0:
            if (n % 2) == 0:
                # flip
                Op = vstack((eye(bn, n=L, k=L - bn) @ anti_eye(L), Op))
            else:
                # do not flip
                Op = vstack((eye(bn, n=L, k=L - bn), Op))
        if an > 0:
            if (n % 2) == 0:
                # flip
                Op = vstack((Op, eye(an, n=L, k=0) @ anti_eye(L)))
            else:
                # do not flip
                Op = vstack((Op, eye(an, n=L, k=0)))
        return Op
    elif boundary == 'periodic' or boundary == 'wrap':
        Op = eye(L, n=L, k=0)
        for i in range(n + n):
            Op = vstack((Op, eye(L, n=L, k=0)))
        if bn > 0:
            Op = vstack((eye(bn, n=L, k=L - bn), Op))
        if an > 0:
            Op = vstack((Op, eye(an, n=L, k=0)))
        return Op
    else:
        raise ValueError("boundary is either 'periodic' ('wrap')" +
                         " or 'symmetric' ('symm').")


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

from lazylinop import LazyLinOp
import sys
from lazylinop.basicops import kron
from lazylinop.wip.signal import bc

sys.setrecursionlimit(100000)


def bc2d(shape: tuple, x: int = 1, y: int = 1,
         b0: int = 0, a0: int = 0, b1: int = 0,
         a1: int = 0, boundary: str = 'periodic'):
    """Constructs a periodic or symmetric boundary condition lazy
    linear operator. It will be applied to a flattened image.
    It basically add image on bottom, left, top and right side.
    Symmetric boundary condition is something like (on both axis):
    xN, ..., x2, x1 | x1, x2, ..., xN | xN, ..., x2, x1
    while a periodic boundary condition is something like (on both axis):
    x1, x2, ..., xN | x1, x2, ..., xN | x1, x2, ..., xN

    Args:
        shape: tuple
        Shape of the image
        x: int, optional
        2 * x + 1 signals along the first axis
        y: int, optional
        2 * y + 1 signals along the second axis
        b0: int, optional
        Add b0 lines before (along x).
        a0: int, optional
        Add a0 lines after (along x).
        b1: int, optional
        Add b1 lines before (along y).
        a1: int, optional
        Add a1 lines after (along y).
        boundary: str, optional
        wrap/periodic (default) or symm/symmetric boundary condition

    Returns:
        LazyLinOp

    Raises:
        ValueError
            x and y must be >= 0.
        ValueError
            shape expects tuple (R, C).
        ValueError
            b0, a0, b1 and a1 must be >= 0.
        ValueError
            b0 (resp. b1) must be < shape[0] (resp. shape[1]).
        ValueError
            a0 (resp. a1) must be < shape[0] (resp. shape[1]).
        ValueError
            boundary excepts 'wrap', 'periodic', 'symm' or 'symmetric'.

    Examples:
        >>> from lazylinop.wip.signal import bc2d
        >>> import numpy as np
        >>> X = np.array([[0., 1.], [2., 3.]])
        >>> X
        array([[0., 1.],
               [2., 3.]])
        >>> Op = bc2d(X.shape, x=1, y=1, boundary='periodic')
        >>> (Op @ X.ravel()).reshape(2 * (2 * 1 + 1), 2 * (2 * 1 + 1))
        array([[0., 1., 0., 1., 0., 1.],
               [2., 3., 2., 3., 2., 3.],
               [0., 1., 0., 1., 0., 1.],
               [2., 3., 2., 3., 2., 3.],
               [0., 1., 0., 1., 0., 1.],
               [2., 3., 2., 3., 2., 3.]])
        >>> X = np.array([[0., 1.], [2., 3.], [4., 5.]])
        >>> X
        array([[0., 1.],
               [2., 3.],
               [4., 5.]])
        >>> Op = bc2d(X.shape, x=1, y=0, a0=2, a1=1, boundary='symmetric')
        >>> (Op @ X.ravel()).reshape(3 * (2 * 1 + 1) + 2, 2 * (2 * 0 + 1) + 1)
        array([[4., 5., 5.],
               [2., 3., 3.],
               [0., 1., 1.],
               [0., 1., 1.],
               [2., 3., 3.],
               [4., 5., 5.],
               [4., 5., 5.],
               [2., 3., 3.],
               [0., 1., 1.],
               [0., 1., 1.],
               [2., 3., 3.]])
    """
    if len(shape) != 2:
        raise ValueError("shape expects tuple (R, C).")
    if x < 0 or y < 0:
        raise ValueError("x and y must be >= 0.")
    if b0 < 0 or a0 < 0 or b1 < 0 or a1 < 0:
        raise ValueError("b0, a0, b1 and a1 must be >= 0.")
    if b0 >= shape[0] or b1 >= shape[1]:
        raise ValueError("b0 (resp. b1) must be < shape[0] (resp. shape[1]).")
    if a0 >= shape[0] or a1 >= shape[1]:
        raise ValueError("a0 (resp. a1) must be < shape[0] (resp. shape[1]).")
    if (
            boundary != 'wrap' and
            boundary != 'periodic' and
            boundary != 'symm' and
            boundary != 'symmetric'
    ):
        raise ValueError("boundary excepts 'wrap', 'periodic'," +
                         " 'symm' or 'symmetric'.")

    # Use bc and kron lazy linear operators to write bc2d
    # Kronecker product trick: A @ X @ B^T = kron(A, B) @ vec(X)
    Op = kron(bc(shape[0], n=x, bn=b0, an=a0, boundary=boundary),
              bc(shape[1], n=y, bn=b1, an=a1, boundary=boundary))
    return Op


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

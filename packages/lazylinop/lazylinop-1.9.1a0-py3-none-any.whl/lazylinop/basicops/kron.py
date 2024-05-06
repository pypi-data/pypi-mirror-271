from lazylinop import LazyLinOp, binary_dtype, aslazylinops
import numpy as np


def kron(op1, op2):
    r"""
    Returns the :class:`LazyLinOp` for the Kronecker product $op1 \otimes op2$.

    .. note::
        This specialization is particularly optimized for multiplying the
        operator by a vector.

    Args:
        op1: (compatible linear operator)
            scaling factor,
        op2: (compatible linear operator)
            block factor.

    Returns:
        The Kronecker product :class:`LazyLinOp`.

    Example:
        >>> import numpy as np
        >>> import lazylinop as lz
        >>> from pyfaust import rand
        >>> op1 = np.random.rand(100, 100)
        >>> op2 = np.random.rand(100, 100)
        >>> AxB = np.kron(op1,op2)
        >>> lAxB = lz.kron(op1, op2)
        >>> x = np.random.rand(AxB.shape[1], 1)
        >>> print(np.allclose(AxB@x, lAxB@x))
        True
        >>> from timeit import timeit
        >>> timeit(lambda: AxB @ x, number=10) # doctest:+ELLIPSIS
        0...
        >>> # example: 0.4692082800902426
        >>> timeit(lambda: lAxB @ x, number=10) # doctest:+ELLIPSIS
        0...
        >>> # example 0.03464869409799576

    .. seealso::
        - numpy.kron_,
        - scipy.sparse.kron_,
        - pylops.Kronecker_,
        - :func:`.aslazylinop`,
        - `Kronecker product on Wikipedia
          <https://en.wikipedia.org/wiki/Kronecker_product>`_.

.. _numpy.kron:
    https://numpy.org/doc/stable/reference/generated/numpy.kron.html
.. _scipy.sparse.kron:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.kron.html
.. _pylops.Kronecker:
    https://pylops.readthedocs.io/en/stable/api/generated/pylops.Kronecker.html
    """
    op1, op2 = aslazylinops(op1, op2)

    def _kron(op1, op2, shape, op):

        if isinstance(op, np.ndarray):
            op = np.asfortranarray(op)

        # op is always 2d

        if (hasattr(op, 'reshape') and
           hasattr(op, '__matmul__') and hasattr(op, '__getitem__')):

            dtype = binary_dtype(binary_dtype(op1.dtype, op2.dtype), op.dtype)
            res = np.empty((shape[0], op.shape[1]), dtype=dtype)

            def out_col(j, ncols):
                for j in range(j, min(j + ncols, op.shape[1])):
                    op_mat = op[:, j].reshape((op1.shape[1], op2.shape[1]))
                    # Do we multiply from left to right or from right to left?
                    m, k = op1.shape
                    k, n = op_mat.shape
                    n, p = op2.T.shape
                    ltor = m * k * n + m * n * p
                    rtol = m * k * p + k * n * p
                    if ltor < rtol:
                        res[:, j] = ((op1 @ op_mat) @ op2.T).reshape(shape[0])
                    else:
                        res[:, j] = (op1 @ (op_mat @ op2.T)).reshape(shape[0])

            ncols = op.shape[1]
            out_col(0, ncols)

        else:
            raise TypeError('op must possess reshape, __matmul__ and'
                            ' __getitem__ attributes to be multiplied by a'
                            ' Kronecker LazyLinOp (use toarray on the'
                            ' latter to multiply by the former)')
        return res

    shape = (op1.shape[0] * op2.shape[0], op1.shape[1] * op2.shape[1])
    return LazyLinOp(shape,
                     matmat=lambda x: _kron(op1, op2, shape, x),
                     rmatmat=lambda x: _kron(op1.T.conj(), op2.T.conj(),
                                             (shape[1], shape[0]), x),
                     dtype=binary_dtype(op1.dtype, op2.dtype))

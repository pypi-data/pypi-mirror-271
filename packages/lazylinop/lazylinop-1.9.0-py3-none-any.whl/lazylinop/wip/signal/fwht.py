import numpy as np
import scipy as sp
from lazylinop import aslazylinop, LazyLinOp
from lazylinop.basicops import kron
from lazylinop.wip.signal import is_power_of_two
import sys
import warnings
from warnings import warn
sys.setrecursionlimit(100000)
warnings.simplefilter(action='always')


def fwht(N: int, backend: str = 'pyfaust', disable_jit: int = 0):
    r"""Creates a Fast-Walsh-Hadamard-Transform lazy linear operator.
    The size of the signal has to be a power of two greater than 1.

    Args:
        N: int
            Size the input array.
        backend: str, optional
            It can be 'direct', 'kronecker', 'pyfaust' (default),
            'pytorch' (wip) or 'scipy'.

            - 'kronecker' uses kron to compute FWHT.
            - 'direct' uses N * log(N) algorithm and Numba jit to compute FWHT.
            - 'pytorch' does not work yet.
            - 'scipy' uses scipy.linalg.hadamard.
            - 'pyfaust' uses wht from pyfaust.
            - 'auto' uses 'pyfaust' for :math:`N<=32768`, 'direct' otherwise.
              Of note, this condition depends on your hardware. It may change
              in the near future.
        disable_jit: int, optional
            If 0 (default) enable Numba jit.

    Returns:
        LazyLinOp

    Raises:
        ValueError
            The size of the signal must be a power of two,
            greater or equal to two.
        ValueError
            backend argument expects either 'direct',
            'kronecker', 'pytorch' (do not work yet), pyfaust or 'scipy'.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop.wip.signal import fwht
        >>> x = np.random.randn(16)
        >>> y = fwht(x.shape[0]) @ x
        >>> np.allclose(y, sp.linalg.hadamard(x.shape[0]) @ x)
        True
        >>> X = np.random.randn(8, 4)
        >>> Y = fwht(X.shape[0]) @ X
        >>> np.allclose(Y, sp.linalg.hadamard(X.shape[0]) @ X)
        True

    .. seealso::
        `Wikipedia <https://en.wikipedia.org/wiki/Hadamard_transform>`_,
        `scipy.linalg.hadamard <https://docs.scipy.org/doc/scipy/reference/
        generated/scipy.linalg.hadamard.html>`_,
        `pyfaust wht <https://faustgrp.gitlabpages.inria.fr/faust/last-doc/
        html/namespacepyfaust.html#a35453cb41a399968807f4483a331669b>`_.
    """

    new_backend = backend
    try:
        import numba as nb
        from numba import njit, prange
        _T = nb.config.NUMBA_NUM_THREADS
        nb.config.THREADING_LAYER = 'omp'
        nb.config.DISABLE_JIT = disable_jit
    except ImportError:
        if new_backend == 'direct':
            warn("Did not find Numba, switch to 'pyfaust' backend.")
            new_backend = 'pyfaust'

    if not is_power_of_two(N) or N < 2:
        raise ValueError("The size of the signal must be a power of two," +
                         " greater or equal to two.")

    # elif new_backend == 'pytorch':
    #     raise Exception('PyTorch backend is Work-in-Progress.')
    #     from math import log2, sqrt
    #     import torch
    #     def _matmat(x):
    #         output = torch.Tensor(x)
    #         xshape = x.shape
    #         if len(xshape) == 1:
    #             output = output.unsqueeze(0)
    #         batch_dim, L = output.shape
    #         D = int(log2(L))
    #         H, F = 2, 1
    #         for d in range(D):
    #             output = output.view(batch_dim, L // H, H)
    #             h1, h2 = output[:, :, :F], output[:, :, F:]
    #             output = torch.cat((h1 + h2, h1 - h2), dim=-1)
    #             H *= 2
    #             F = H // 2

    #     return LazyLinOp(
    #         shape=(N, N),
    #         matvec=lambda x: _matmat(x),
    #         rmatvec=lambda x: _matmat(x),
    #         dtype='float'
    #     )

    if new_backend == 'scipy':
        return LazyLinOp(
            shape=(N, N),
            matvec=lambda x: sp.linalg.hadamard(N) @ x,
            rmatvec=lambda x: sp.linalg.hadamard(N) @ x,
            dtype='float'
        )
    elif new_backend == 'pyfaust' or (new_backend == 'auto'
                                      and N <= 32768):
        from pyfaust import wht
        return aslazylinop(wht(N, normed=False))
    elif new_backend == 'kronecker':
        H1 = np.array([[1.0, 1.0], [1.0, -1.0]])
        D = int(np.log2(N))
        if D == 1:
            return aslazylinop(H1)
        elif D == 2:
            return kron(H1, H1)
        else:
            Hd = kron(H1, H1)
            for d in range(1, D - 1):
                Hd = kron(H1, Hd)
            return Hd
    elif new_backend == 'direct' or (new_backend == 'auto'
                                     and N > 32768):

        def _matmat(x):
            # x is always 2d

            @njit(cache=True)
            def _1d(x):
                H = 1
                D = int(np.floor(np.log2(N)))
                tmp1, tmp2 = 0.0, 0.0
                y = np.empty(N, dtype=x.dtype)
                for i in range(N):
                    y[i] = x[i]
                for d in range(D):
                    for i in range(0, N, 2 * H):
                        for j in range(i, i + H):
                            tmp1 = y[j]
                            tmp2 = y[j + H]
                            y[j] = tmp1 + tmp2
                            y[j + H] = tmp1 - tmp2
                    H *= 2
                return y

            @njit(parallel=True, cache=True)
            def _2d(x):
                batch_size = x.shape[1]
                H = 1
                D = int(np.floor(np.log2(N)))
                NperT = int(np.ceil(N / _T))
                tmp1 = np.empty(_T, dtype=x.dtype)
                tmp2 = np.empty(_T, dtype=x.dtype)
                y = np.empty((N, batch_size), dtype=x.dtype)
                if ((N * batch_size) / _T) > 100000:
                    for t in prange(_T):
                        for i in range(t * NperT, min(N, (t + 1) * NperT), 1):
                            for b in range(batch_size):
                                y[i, b] = x[i, b]
                else:
                    for i in range(N):
                        for b in range(batch_size):
                            y[i, b] = x[i, b]
                for d in range(D):
                    for i in range(0, N, 2 * H):
                        for j in range(i, i + H):
                            # NumPy uses row-major format
                            for b in range(batch_size):
                                tmp1[0] = y[j, b]
                                tmp2[0] = y[j + H, b]
                                y[j, b] = tmp1[0] + tmp2[0]
                                y[j + H, b] = tmp1[0] - tmp2[0]
                    H *= 2
                return y

            return _1d(x.ravel()).reshape(-1, 1) if x.shape[1] == 1 else _2d(x)

        return LazyLinOp(
            shape=(N, N),
            matmat=lambda x: _matmat(x),
            rmatmat=lambda x: _matmat(x),
            dtype='float'
        )
    else:
        raise ValueError("backend argument expects either 'direct', \
        'kronecker', 'pytorch' (do not work yet), 'pyfaust' or 'scipy'.")


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

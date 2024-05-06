import numpy as np
import scipy as sp
from lazylinop import aslazylinop, LazyLinOp
from lazylinop.basicops import eye
from lazylinop.wip.signal import is_power_of_two
import sys
import warnings
from warnings import warn
sys.setrecursionlimit(100000)
warnings.simplefilter(action='always')


def fft(N, backend: str = 'scipy', disable_jit: int = 0, **kwargs):
    """
    Returns a LazyLinOp for the DFT of size N.

    Args:
        N: int
            Size of the input (N > 0).
        backend:
            'scipy' (default) or 'pyfaust' for the underlying computation
            of the DFT. If we denote F the LazyLinOp DFT, X a batch of
            vectors and F @ X the DFT of X, backend 'scipy' uses
            fft (resp. fftn) encapsulation when batch size is 1 (resp. > 1).
            'iterative' backend use Numba prange function and shows good
            performances when the size of the signal is greater than 1e6
            and the size of the batch of vectors is greater than 1000.
            We do not recommend to use it for small size.
        kwargs:
            Any key-value pair arguments to pass to the SciPy or
            pyfaust dft backend.

    Returns:
        LazyLinOp

    Raises:
        ValueError
            Invalid norm value for 'scipy' backend.
        ValueError
            backend must be either 'scipy' or 'pyfaust'.

    Example:
        >>> from lazylinop.wip.signal import fft
        >>> import numpy as np
        >>> F1 = fft(32, norm='ortho')
        >>> F2 = fft(32, backend='pyfaust')
        >>> x = np.random.rand(32)
        >>> np.allclose(F1 @ x, F2 @ x)
        True
        >>> y = F1 @ x
        >>> np.allclose(F1.H @ y, x)
        True
        >>> np.allclose(F2.H @ y, x)
        True

    .. seealso::
        `<https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft.html>`_
        `<https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fftn.html>`_
        `<https://faustgrp.gitlabpages.inria.fr/faust/last-doc/html/namespacepyfaust.html#a2695e35f9c270e8cb6b28b9b40458600>`_
    """

    new_backend = backend
    try:
        import numba as nb
        from numba import njit, prange, set_num_threads, threading_layer
        nb.config.THREADING_LAYER = 'omp'
        T = nb.config.NUMBA_NUM_THREADS
        nb.config.DISABLE_JIT = disable_jit
    except ImportError:
        if new_backend == 'direct':
            warn("Did not find Numba, switch backend to 'scipy'.")
            new_backend = 'scipy'

    if new_backend == 'scipy':
        if 'n' in kwargs.keys() and kwargs['n'] is not None:
            L = kwargs['n']
        else:
            L = N
            kwargs['n'] = N

        if 'norm' in kwargs:
            if kwargs['norm'] == 'ortho':
                norm = 1
            elif kwargs['norm'] == 'forward':
                norm = 1 / L
            elif kwargs['norm'] == 'backward':
                norm = L
            else:
                raise ValueError("Invalid norm value for 'scipy' backend.")
        else:
            # default is backward
            norm = L

        def _matmat(x):
            # x is always 2d
            batch_size = x.shape[1]
            if batch_size == 1:
                y = sp.fft.fft(x, axis=0, **kwargs)
            else:
                tmp = kwargs['n']
                kwargs['s'] = (L)
                kwargs.pop('n', None)
                y = sp.fft.fftn(x, axes=0, **kwargs)
                kwargs['n'] = tmp
                kwargs.pop('s', None)
            return y

        def _rmatmat(x):
            # x is always 2d
            batch_size = x.shape[1]
            if batch_size == 1:
                y = sp.fft.ifft(x, axis=0, **kwargs) * norm
            else:
                kwargs['s'] = (L)
                tmp = kwargs['n']
                kwargs.pop('n', None)
                y = sp.fft.ifftn(x, axes=0, **kwargs) * norm
                kwargs['n'] = tmp
                kwargs.pop('s', None)
            return y

        F = LazyLinOp(
            shape=(L, N),
            matmat=lambda x: _matmat(x),
            rmatmat=lambda x: _rmatmat(x),
            dtype='complex'
        )
    elif new_backend == 'pyfaust':
        if not is_power_of_two(N):
            raise Exception("pyfaust allows power of two only.")
        else:
            from pyfaust import dft
            F = aslazylinop(dft(N, **kwargs))
    elif new_backend == 'iterative':
        if not is_power_of_two(N) or N == 1:
            raise ValueError("signal length is not a power of 2.")

        def _matmat(x, adjoint):

            @njit(cache=True)
            def _reverse(a: int, b: int) -> int:
                res = 0
                for i in range(b):
                    if a & (1 << i):
                        res |= 1 << (b - 1 - i)
                return res

            # Because of Numba split 1d and 2d cases
            @njit(parallel=True, cache=True)
            def _1d(x, adjoint):
                x = x.astype(np.complex_)
                N = x.shape[0]
                D = int(np.log2(N))
                y = np.empty(N, dtype=np.complex_)
                # Bit-reversal permutations
                # Enough work to do therefore we use prange
                NperT = int(np.ceil(N / T))
                for t in prange(T):
                    for i in range(t * NperT, min(N, (t + 1) * NperT), 1):
                        y[i] = x[i]
                for t in prange(T):
                    for i in range(t * NperT, min(N, (t + 1) * NperT), 1):
                        tmp = _reverse(i, D)
                        if i < tmp:
                            y[i], y[tmp] = y[tmp], y[i]
                # Compute DFT with iterative algorithm
                wmk = np.empty(T, dtype=np.complex_)
                u = np.empty(T, dtype=np.complex_)
                v = np.empty(T, dtype=np.complex_)
                # Enough work to do therefore we use prange
                iterations = np.empty(T, dtype=np.int_)
                for d in range(D):
                    hstep = 2 ** d
                    step = 2 * hstep
                    wm = np.exp((2 * int(adjoint) - 1) * 2.0j * np.pi / step)
                    NperT = step * int(np.ceil(N / (T * step)))
                    for t in prange(T):
                        iterations[t] = 0
                        for n in range(t * NperT, (t + 1) * NperT, step):
                            if n > (N - step):
                                continue
                            wmk[t] = 1.0 + 0.0j
                            for k in range(0, hstep, 1):
                                u[t] = y[n + k]
                                v[t] = wmk[t] * y[n + k + hstep]
                                y[n + k] = u[t] + v[t]
                                y[n + k + hstep] = u[t] - v[t]
                                iterations[t] += 1
                                wmk[t] *= wm
                return y

            # Because of Numba split 1d and 2d cases
            # @njit(parallel=True, cache=True)
            @njit(cache=True)
            def _2d(x, adjoint):
                x = x.astype(np.complex_)
                N, batch_size = x.shape
                D = int(np.log2(N))
                y = np.empty((N, batch_size), dtype=np.complex_)
                # Bit-reversal permutations
                for i in range(N):
                    for b in range(batch_size):
                        y[i, b] = x[i, b]
                ii = 0
                for i in range(1, N):
                    bit = N >> 1
                    # print(t, ii & bit)
                    while (ii & bit):
                        ii ^= bit
                        bit >>= 1
                    ii ^= bit
                    if i < ii:
                        for b in range(batch_size):
                            y[i, b], y[ii, b] = y[ii, b], y[i, b]
                # for i in range(N):
                #     tmp = _reverse(i, D)
                #     if i < tmp:
                #         for b in range(batch_size):
                #             y[i, b], y[tmp, b] = y[tmp, b], y[i, b]
                # Compute DFT with iterative algorithm
                wmk = np.empty(T, dtype=np.complex_)
                backup_wmk = np.empty(T, dtype=np.complex_)
                u = np.empty(T, dtype=np.complex_)
                v = np.empty(T, dtype=np.complex_)
                iterations = np.empty(T, dtype=np.int_)
                # Enough work to do therefore we use prange ?
                BperT = int(np.ceil(batch_size / T))
                hstep = np.empty(T, dtype=np.int_)
                step = np.empty(T, dtype=np.int_)
                twopi = (2 * int(adjoint) - 1) * 2.0j * np.pi
                # for t in prange(T):
                #     for b in range(t * BperT,
                #                    min(batch_size, (t + 1) * BperT), 1):
                #         for d in range(D):
                #             hstep[t] = 2 ** d
                #             step[t] = 2 * hstep[t]
                #             wm = np.exp(twopi / step[t])
                #             for n in range(0, N, step[t]):
                #                 wmk[t] = 1.0 + 0.0j
                #                 for k in range(0, hstep[t], 1):
                #                     u[t] = y[n + k, b]
                #                     v[t] = wmk[t] * y[n + k + hstep[t], b]
                #                     # y[n + k, b] = u[t] + v[t]
                #                     y[n + k, b] += v[t]
                #                     y[n + k + hstep[t], b] = u[t] - v[t]
                #                     iterations[t] += 1
                #                     wmk[t] *= wm
                for d in range(D):
                    hstep[0] = 2 ** d
                    step[0] = 2 * hstep[0]
                    wm = np.exp(twopi / step[0])
                    for n in range(0, N, step[0]):
                        wmk[0] = 1.0 + 0.0j
                        for k in range(0, hstep[0], 1):
                            for b in range(batch_size):
                                u[0] = y[n + k, b]
                                v[0] = wmk[0] * y[n + k + hstep[0], b]
                                # y[n + k, b] = u[0] + v[0]
                                y[n + k, b] += v[0]
                                y[n + k + hstep[0], b] = u[0] - v[0]
                                iterations[0] += 1
                            wmk[0] *= wm
                return y

            return _1d(x.ravel(), adjoint).reshape(-1, 1) if x.shape[1] == 1 else _2d(x, adjoint)

        F = LazyLinOp(
            shape=(N, N),
            matmat=lambda x: _matmat(x, False),
            rmatmat=lambda x: _matmat(x, True)
        )
    else:
        raise ValueError("backend must be either 'scipy' or 'pyfaust'.")
    return F


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

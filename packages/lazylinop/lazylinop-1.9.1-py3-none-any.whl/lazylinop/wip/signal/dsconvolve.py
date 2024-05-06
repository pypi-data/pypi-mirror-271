import numpy as np
from lazylinop import LazyLinOp
import sys
import warnings
from warnings import warn
warnings.simplefilter(action='always')
sys.setrecursionlimit(100000)


def dsconvolve(in1: int, in2: np.ndarray, mode: str = 'full',
               offset: int = 0, every: int = 2, disable_jit: int = 0):
    """Creates convolution plus down-sampling lazy linear operator.
    If input is a 2d array shape=(in1, batch), return convolution per column.
    offset (0 or 1) argument determines the first element to compute while
    every argument determines distance between two elements (1 or 2).
    The ouput of convolution followed by down-sampling C @ x is equivalent
    to :code:`scipy.signal.convolve(x, in2, mode)[offset::every]`.

    Args:
        in1: int
            Length of the input.
        in2: np.ndarray
            1d kernel to convolve with the signal, shape is (K, ).
        mode: str, optional

            - 'full' computes convolution (input + padding).
            - 'valid' computes 'full' mode and extract centered output
              that does not depend on the padding.
            - 'same' computes 'full' mode and extract centered output
              that has the same shape that the input.
        offset: int, optional
            First element to keep (default is 0).
        every: int, optional
            Keep element every this number (default is 2).
        disable_jit: int, optional
            If 0 (default) enable Numba jit.

    Returns:
        LazyLinOp

    Raises:
        ValueError
            Number of dimensions of the kernel must be 1.
        ValueError
            Negative input length.
        ValueError
            mode is either 'full' (default), 'valid' or 'same'
        Exception
            Length of the input are expected (int).
        ValueError
            Size of the kernel is greater than the size of
            signal and mode is valid.
        Exception
            mode, offset and every are incompatibles with kernel
            and signal sizes.
        ValueError
            offset must be either 0 or 1.
        ValueError
            every must be either 1 or 2.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop.wip.signal import dsconvolve
        >>> x = np.random.rand(1024)
        >>> kernel = np.random.rand(32)
        >>> Op = dsconvolve(x.shape, kernel, mode='same', offset=0, every=2)
        >>> c1 = Op @ x
        >>> c2 = sp.signal.convolve(x, kernel, mode='same', method='auto')
        >>> np.allclose(c1, c2[0::2])
        True

    .. seealso::
        `SciPy convolve function <https://docs.scipy.org/doc/scipy/
        reference/generated/scipy.signal.convolve.html>`_,
        `SciPy correlate function <https://docs.scipy.org/doc/scipy/
        reference/generated/scipy.signal.correlate.html>`_.
    """

    try:
        import numba as nb
        from numba import njit, prange
        nb.config.THREADING_LAYER = 'omp'
        T = nb.config.NUMBA_NUM_THREADS
        nb.config.DISABLE_JIT = disable_jit
    except ImportError:
        warn("Did not find Numba.")

        def njit(*args, **kwargs):
            lambda f: f

        def prange(*args, **kwargs):
            range(
                *args,
                **({k: v for k, v in kwargs.items() if k not in ("parallel",)})
            )

        T = 1

    if mode not in ['full', 'valid', 'same']:
        raise ValueError("mode is either 'full' (default), 'valid' or 'same'.")

    # Check if length of the input has been passed to the function
    if type(in1) is not int:
        raise Exception("Length of the input are expected (int).")

    if in2.ndim != 1:
        raise ValueError("Number of dimensions of the kernel must be 1.")
    if in1 <= 0:
        raise Exception("Negative input length.")

    K = in2.shape[0]

    if K > in1 and mode == 'valid':
        raise ValueError("Size of the kernel is greater than the size" +
                         " of the signal and mode is valid.")
    if offset != 0 and offset != 1:
        raise ValueError('offset must be either 0 or 1.')
    if every != 1 and every != 2:
        raise ValueError('every must be either 1 or 2.')

    # Length of the output as a function of convolution mode
    dims = np.array([in1 + K - 1, in1 - K + 1, in1, in1], dtype=np.int_)
    imode = (
        0 * int(mode == 'full') +
        1 * int(mode == 'valid') +
        2 * int(mode == 'same')
    )
    start = (dims[0] - dims[imode]) // 2 + offset
    end = min(dims[0], start + dims[imode] - offset)
    L = int(np.ceil((dims[imode] - offset) / every))
    if L <= 0:
        raise Exception("mode, offset and every are incompatibles" +
                        " with kernel and signal sizes.")

    def _matmat(x, kernel, T):
        # x is always 2d
        batch_size = x.shape[1]
        perT = int(np.ceil((dims[0] - start) / T))
        use_parallel_1d = bool((perT * K) > 100000)
        use_parallel_2d = bool((perT * K * batch_size) > 100000)

        # Because of Numba split 1d and 2d
        @njit(parallel=use_parallel_1d, cache=True)
        def _1d(x, kernel):
            _T = T
            if not use_parallel_1d:
                _T = 1
                perT = dims[0] - start
            y = np.full(L, 0.0 * (kernel[0] * x[0]))
            for t in prange(_T):
                for i in range(
                        start + t * perT,
                        min(end, start + (t + 1) * perT)):
                    # Down-sampling
                    if ((i - start) % every) == 0:
                        for j in range(max(0, i - in1 + 1), min(K, i + 1)):
                            y[(i - start) // every] += kernel[j] * x[i - j]
            return y

        @njit(parallel=use_parallel_2d, cache=True)
        def _2d(x, kernel):
            _T = T
            if not use_parallel_2d:
                _T = 1
                perT = dims[0] - start
            y = np.full((L, batch_size), 0.0 * (kernel[0] * x[0, 0]))
            for t in prange(_T):
                for i in range(
                        start + t * perT,
                        min(end, start + (t + 1) * perT)):
                    # Down-sampling
                    if ((i - start) % every) == 0:
                        for j in range(max(0, i - in1 + 1), min(K, i + 1)):
                            # NumPy uses row-major format
                            for b in range(batch_size):
                                y[(i - start) // every,
                                  b] += kernel[j] * x[i - j, b]
            return y

        return _1d(x.ravel(), kernel).reshape(-1, 1) if x.shape[1] == 1 else _2d(x, kernel)

    def _rmatmat(x, kernel, T):
        # x is always 2d
        batch_size = x.shape[1]
        rperT = int(np.ceil(dims[2] / T))
        use_rparallel_1d = bool((rperT * K) > 100000)
        use_rparallel_2d = bool((rperT * K * batch_size) > 100000)

        # Because of Numba split 1d and 2d
        @njit(parallel=use_rparallel_1d, cache=True)
        def _1d(x, kernel):
            _T = T
            if not use_rparallel_1d:
                _T = 1
                rperT = dims[2]
            a = 0 if imode == 0 and offset == 0 else 1
            y = np.full(dims[2], 0.0 * (kernel[0] * x[0]))
            for t in prange(_T):
                for i in range(t * rperT, min(dims[2], (t + 1) * rperT)):
                    if every == 2:
                        jstart = (i - a * start) - (i - a * start) // every
                    elif every == 1:
                        jstart = i - a * start
                    else:
                        pass
                    for j in range(L):
                        if j < jstart:
                            continue
                        if every == 2:
                            k = (i - a * start) % 2 + (j - jstart) * every
                        elif every == 1:
                            k = j - jstart
                        else:
                            pass
                        if k < K:
                            y[i] += kernel[k] * x[j]
            return y

        @njit(parallel=use_rparallel_2d, cache=True)
        def _2d(x, kernel):
            _T = T
            if not use_rparallel_2d:
                _T = 1
                rperT = dims[2]
            a = 0 if imode == 0 and offset == 0 else 1
            y = np.full((dims[2], batch_size), 0.0 * (kernel[0] * x[0, 0]))
            for t in prange(_T):
                for i in range(t * rperT, min(dims[2], (t + 1) * rperT)):
                    if every == 2:
                        jstart = (i - a * start) - (i - a * start) // every
                    elif every == 1:
                        jstart = i - a * start
                    else:
                        pass
                    for j in range(L):
                        if j < jstart:
                            continue
                        if every == 2:
                            k = (i - a * start) % 2 + (j - jstart) * every
                        elif every == 1:
                            k = j - jstart
                        else:
                            pass
                        if k < K:
                            # NumPy uses row-major format
                            for b in range(batch_size):
                                y[i, b] += kernel[k] * x[j, b]
            return y

        return _1d(x.ravel(), kernel).reshape(-1, 1) if x.shape[1] == 1 else _2d(x, kernel)

    return LazyLinOp(
        shape=(L, dims[2]),
        matmat=lambda x: _matmat(x, in2, T),
        rmatmat=lambda x: _rmatmat(x, in2, T),
        dtype=in2.dtype
    )

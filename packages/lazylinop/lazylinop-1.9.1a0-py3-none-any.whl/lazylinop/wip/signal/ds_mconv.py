import numpy as np
from lazylinop import LazyLinOp
import sys
import warnings
from warnings import warn

warnings.simplefilter(action="always")
sys.setrecursionlimit(100000)


def ds_mconv(
    in1: int,
    in2: np.ndarray,
    in3: np.ndarray,
    mode: str = "full",
    offset: int = 0,
    disable_jit: int = 0,
):
    """Creates convolution plus down-sampling lazy linear operator.
    It first computes convolution with in2 and in3 filters.
    Then, it performs down-sampling (keep 1 every 2) on both convolution
    results (it is useful for Discrete-Wavelet-Transform).
    If input x is a 1d array, C @ x return concatenation of both convolution.
    If input X is a 2d array, C @ X return concatenation per column.
    offset (0 or 1) argument determines the first element to compute.
    The ouput C @ x is equivalent to the concatenation of
    :code:`scipy.signal.convolve(x, in2, mode)[offset::2]` and
    :code:`scipy.signal.convolve(x, in3, mode)[offset::2]`.

    Args:
        in1: int
            Length of the input.
        in2: np.ndarray
            First 1d kernel to convolve with the signal, shape is (K, ).
        in3: np.ndarray
            Second 1d kernel to convolve with the signal, shape is (K, ).
        mode: str, optional

            - 'full' computes convolution (input + padding).
            - 'valid' computes 'full' mode and extract centered output
              that does not depend on the padding.
            - 'same' computes 'full' mode and extract centered output
              that has the same shape that the input.
        offset: int, optional
            First element to keep (default is 0).
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
        Exception
            in2 and in3 must have the same length.
        ValueError
            Size of the kernel is greater than the size of
            signal and mode is valid.
        Exception
            mode and offset values are incompatibles with
            kernel and signal sizes.
        ValueError
            offset must be either 0 or 1.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop.wip.signal import ds_conv_lh
        >>> x = np.random.rand(1024)
        >>> l = np.random.rand(32)
        >>> h = np.random.rand(32)
        >>> Op = ds_conv_lh(x.shape, l, h, mode='same', offset=0)
        >>> c1 = Op @ x
        >>> c2 = sp.signal.convolve(x, l, mode='same', method='auto')
        >>> c3 = sp.signal.convolve(x, h, mode='same', method='auto')
        >>> np.allclose(c1, np.hstack((c2[0::2], c3[0::2])))
        True

    .. seealso::
        `SciPy convolve function <https://docs.scipy.org/doc/scipy/
        reference/generated/scipy.signal.convolve.html>`_,
        `SciPy correlate function <https://docs.scipy.org/doc/scipy/
        reference/generated/scipy.signal.correlate.html>`_.
    """

    numba_ok = True if disable_jit == 0 else False
    if not numba_ok:

        def njit(*args, **kwargs):
            lambda f: f

        def prange(*args, **kwargs):
            range(
                *args, **(
                    {
                        k: v for
                        k, v in kwargs.items() if k not in
                        (
                            "parallel",
                        )
                    }
                )
            )

    try:
        import numba as nb
        from numba import njit, prange
        nb.config.THREADING_LAYER = "omp"
        T = nb.config.NUMBA_NUM_THREADS
        nb.config.DISABLE_JIT = disable_jit
    except ImportError:
        warn("Did not find Numba.")
        T = 1

    if mode not in ["full", "valid", "same"]:
        raise ValueError("mode is either 'full' (default), 'valid' or 'same'.")

    # Check if length of the input has been passed to the function
    if type(in1) is not int:
        raise Exception("Length of the input are expected (int).")

    if in2.ndim != 1 or in3.ndim != 1:
        raise ValueError("Number of dimensions of the kernel must be 1.")
    if in1 <= 0:
        raise Exception("Negative input length.")

    H = in3.shape[0]
    if H != in2.shape[0]:
        raise Exception("in2 and in3 must have the same length.")
    K = H

    if K > in1 and mode == "valid":
        raise ValueError(
            "Size of the kernel is greater than the size"
            + " of the signal and mode is valid."
        )
    if offset != 0 and offset != 1:
        raise ValueError("offset must be either 0 or 1.")

    every = 2

    # Length of the output as a function of convolution mode
    dims = np.array([in1 + K - 1, in1 - K + 1, in1, in1], dtype=np.int_)
    imode = (
        0 * int(mode == "full") +
        1 * int(mode == "valid") +
        2 * int(mode == "same")
    )
    start = (dims[0] - dims[imode]) // 2 + offset
    end = min(dims[0], start + dims[imode] - offset)
    L = int(np.ceil((dims[imode] - offset) / every))
    if L <= 0:
        raise Exception(
            "mode and offset values every are incompatibles"
            + " with kernel and signal sizes."
        )

    def _matmat(x, in2, in3, _T):
        # x is always 2d
        batch_size = x.shape[1]
        perT = int(np.ceil((dims[0] - start) / _T))
        perT += perT % every
        use_parallel = bool((perT * K * batch_size) > 1000)

        # Because of Numba split 1d and 2d
        @njit(parallel=use_parallel, cache=True)
        def _1d(x, in2, in3):
            y = np.full(2 * L, 0.0 * (in2[0] * in3[0] * x[0]))
            for t in prange(_T):
                for i in range(start + t * perT,
                               min(end, start + (t + 1) * perT),
                               every):
                    # i - j < in1
                    # i - j >= 0
                    # j < K
                    for j in range(max(0, i - in1 + 1), min(K, i + 1), 1):
                        y[(i - start) // every] += in2[j] * x[i - j]
                        y[L + (i - start) // every] += (
                            in3[j] * x[i - j]
                        )
            return y

        @njit(parallel=use_parallel, cache=True)
        def _2d(x, in2, in3):
            y = np.full((2 * L, batch_size), 0.0 * (in2[0] * in3[0] * x[0, 0]))
            for t in prange(_T):
                for i in range(start + t * perT,
                               min(end, start + (t + 1) * perT),
                               every):
                    # i - j < in1
                    # i - j >= 0
                    # j < K
                    for j in range(max(0, i - in1 + 1), min(K, i + 1), 1):
                        # NumPy uses row-major format
                        for b in range(batch_size):
                            y[(i - start) // every, b] += (
                                in2[j] * x[i - j, b]
                            )
                            y[L + (i - start) // every, b] += (
                                in3[j] * x[i - j, b]
                            )
            return y

        return _1d(x.ravel(), in2, in3).reshape(-1, 1) if x.shape[1] == 1 else _2d(x, in2, in3)

    def _rmatmat(x, in2, in3, T):
        # x is always 2d
        batch_size = x.shape[1]
        rperT = int(np.ceil(dims[2] / T))
        use_rparallel = bool((rperT * K * batch_size) > 1000)

        # Because of Numba split 1d and 2d
        @njit(parallel=use_rparallel, cache=True)
        def _1d(x, in2, in3):
            a = 0 if imode == 0 and offset == 0 else 1
            y = np.full(dims[2], 0.0 * (in2[0] * in3[0] * x[0]))
            for t in prange(T):
                for i in range(t * rperT, min(dims[2], (t + 1) * rperT)):
                    if every == 2:
                        jstart = (i - a * start) - (i - a * start) // every
                    elif every == 1:
                        jstart = i - a * start
                    else:
                        pass
                    for j in range(max(0, jstart), L):
                        if every == 2:
                            k = (i - a * start) % 2 + (j - jstart) * every
                        elif every == 1:
                            k = j - jstart
                        else:
                            pass
                        if k < K:
                            y[i] += in2[k] * x[j]
                            y[i] += in3[k] * x[L + j]
            return y

        @njit(parallel=use_rparallel, cache=True)
        def _2d(x, in2, in3):
            a = 0 if imode == 0 and offset == 0 else 1
            y = np.full((dims[2], batch_size),
                        0.0 * (in2[0] * in3[0] * x[0, 0]))
            for t in prange(T):
                for i in range(t * rperT, min(dims[2], (t + 1) * rperT)):
                    if every == 2:
                        jstart = (i - a * start) - (i - a * start) // every
                    elif every == 1:
                        jstart = i - a * start
                    else:
                        pass
                    for j in range(max(0, jstart), L):
                        if every == 2:
                            k = (i - a * start) % 2 + (j - jstart) * every
                        elif every == 1:
                            k = j - jstart
                        else:
                            pass
                        if k < K:
                            # NumPy uses row-major format
                            for b in range(batch_size):
                                y[i, b] += in2[k] * x[j, b]
                                y[i, b] += in3[k] * x[L + j, b]
            return y

        return _1d(x.ravel(), in2, in3).reshape(-1, 1) if x.shape[1] == 1 else _2d(x, in2, in3)

    return LazyLinOp(
        shape=(2 * L, dims[2]),
        matmat=lambda x: _matmat(x, in2, in3, T),
        rmatmat=lambda x: _rmatmat(x, in2, in3, T),
        dtype=in2.dtype,
    )

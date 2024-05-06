import numpy as np
import scipy as sp
import sys
from lazylinop import aslazylinop, binary_dtype, LazyLinOp, mpad2
from lazylinop.basicops import block_diag, diag, eye, kron
from lazylinop.wip.signal import fft, is_power_of_two, oa
import warnings
from warnings import warn

sys.setrecursionlimit(100000)
warnings.simplefilter(action='always')


def convolve(in1: int, in2: np.ndarray, mode: str = 'full',
             method: str = 'scipy encapsulation', disable_jit: int = 0):
    r"""Creates a lazy linear operator that corresponds to the
    convolution of a signal of size in1 with a kernel in2.
    If signal is a 2d array (in1, batch), return convolution per column.
    Kernel argument in2 must be 1d array even if input signal is a 2d array.

    Args:
        in1: int
            Length of the input.
        in2: np.ndarray
            1d kernel to convolve with the signal, shape is (K, ).
        mode: str, optional

            - 'full' computes convolution (input + padding).
            - 'valid' computes 'full' mode and extract centered output that
              does not depend on the padding.
            - 'same' computes 'full' mode and extract centered output that has
              the same shape that the input.
            - 'circ' computes circular convolution
        method: str, optional

            - 'auto' use best implementation.
            - 'direct' direct computation using nested for loops.
              It uses Numba jit.
              Larger the signal is better the performances are.
              Larger the batch size is better the performances are.
            - 'scipy encapsulation' (default) to use lazy encapsulation
              of Scipy.signal convolve function. For large batch
              and small signal sizes, it uses encapsulation of
              :code:`sp.linalg.toeplitz`.
            - 'pyfaust toeplitz' to use pyfaust implementation
              of Toeplitz matrix.
            - 'oa' to use lazylinop implementation of overlap-add method.

        The following methods only work with :code:`mode='circ'`.

            - 'scipy fft' use Scipy implementation of FFT
              to compute circular convolution.
            - 'pyfaust circ' use pyfaust implementation of circulant matrix.
            - 'pyfaust dft' use pyfaust implementation of DFT.
        disable_jit: int, optional
            If 0 (default) disable Numba jit.

    Returns:
        LazyLinOp

    Raises:
        Exception
        Negative dimension of the signal and/or the kernel is not equal to 1.
        ValueError
        mode is either 'full' (default), 'valid', 'same' or 'circ'.
        Exception
        in1 expects int.
        ValueError
        Size of the kernel is greater than the size
        of signal and mode is valid.
        ValueError
        method is not in:
        'auto',
        'direct',
        'scipy encapsulation',
        'pyfaust toeplitz',
        'oa',
        'scipy fft',
        'pyfaust circ',
        'pyfaust dft'
        ValueError
        method='pyfaust circ', 'scipy fft' or 'pyfaust dft'
        works only with mode='circ'.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.signal import convolve
        >>> import scipy as sp
        >>> x = np.random.rand(1024)
        >>> kernel = np.random.rand(32)
        >>> c1 = convolve(x.shape[0], kernel, mode='same', method='direct') @ x
        >>> c2 = sp.signal.convolve(x, kernel, mode='same', method='auto')
        >>> np.allclose(c1, c2)
        True
        >>> N = 32768
        >>> x = np.random.rand(N)
        >>> kernel = np.random.rand(48)
        >>> c1 = convolve(N, kernel, mode='circ', method='scipy fft') @ x
        >>> c2 = convolve(N, kernel, mode='circ', method='pyfaust dft') @ x
        >>> np.allclose(c1, c2)
        True

    .. seealso::
        `SciPy convolve function <https://docs.scipy.org/doc/scipy/
        reference/generated/scipy.signal.convolve.html>`_,
        `SciPy correlate function <https://docs.scipy.org/doc/scipy/
        reference/generated/scipy.signal.correlate.html>`_.
    """
    if mode not in ['full', 'valid', 'same', 'circ']:
        raise ValueError("mode is either 'full' (default)," +
                         " 'valid', 'same' or 'circ'.")

    methods = [
        'auto',
        'direct',
        'scipy encapsulation',
        'pyfaust toeplitz',
        'oa',
        'scipy fft',
        'pyfaust circ',
        'pyfaust dft'
    ]

    circmethods = [
        'auto',
        'direct',
        'scipy fft',
        'pyfaust circ',
        'pyfaust dft'
    ]

    if mode == 'circ' and method not in circmethods:
        raise ValueError("mode 'circ' expects method" +
                         " to be in " + str(circmethods))

    if mode != 'circ' and (
            method == 'pyfaust circ' or
            method == 'scipy fft' or
            method == 'pyfaust dft'
    ):
        raise ValueError("method='pyfaust circ', 'scipy fft'" +
                         " or 'pyfaust dft' works only with mode='circ'.")

    if type(in1) is not int:
        raise Exception("in1 expects int.")

    if in1 <= 0 or in2.ndim != 1:
        raise Exception("Negative dimension of the signal and/or" +
                        " the kernel is not equal to 1.")

    K = in2.shape[0]
    if K > in1 and mode == 'valid':
        raise ValueError("Size of the kernel is greater than" +
                         " the size of the signal and mode is valid.")

    if mode == 'circ':
        if method == 'auto':
            compute = 'circ.scipy fft'
        else:
            compute = 'circ.' + method
    else:
        if method == 'auto':
            if K < np.log2(in1):
                compute = 'direct'
            else:
                compute = 'scipy encapsulation'
        else:
            compute = method

    try:
        import numba as nb
        from numba import njit, prange, set_num_threads, threading_layer
        # from numba.core import types
        # from numba.typed import Dict
        _T = nb.config.NUMBA_NUM_THREADS
        nb.config.THREADING_LAYER = 'omp'
        nb.config.DISABLE_JIT = disable_jit
    except ImportError:
        if compute == 'direct':
            warn("Did not find Numba, switch to 'scipy encapsulation'.")
            compute = 'scipy encapsulation'

    # Length of the output as a function of convolution mode
    dim = {'full': in1 + K - 1, 'valid': in1 - K + 1, 'same': in1, 'circ': in1}
    start = (dim['full'] - dim[mode]) // 2
    rmode = {'full': 'valid', 'valid': 'full', 'same': 'same', 'circ': 'circ'}
    rstart = (dim['full'] - dim[rmode[mode]]) // 2

    dims = np.array([in1 + K - 1, in1 - K + 1, in1, in1], dtype=np.int_)
    imode = 0 * int(mode == 'full') + 1 * int(mode == 'valid') + \
        2 * int(mode == 'same') + 3 * int(mode == 'circ')

    # Check which method is asked for
    if compute == 'direct':

        # dim = Dict.empty(
        #     key_type=types.unicode_type,
        #     value_type=types.int64
        # )
        # dim['full'] = in1 + K - 1
        # dim['valid'] = in1 - K + 1
        # dim['same'] = in1
        # dim['circ'] = in1

        # Because of Numba split 1d and 2d
        @njit(parallel=True, cache=True)
        def _matvec(x, kernel):
            K = kernel.shape[0]
            length = in1 + K - 1
            y = np.full(dims[imode], 0.0 * (kernel[0] * x[0]))
            # y[n] = sum(h[k] * s[n - k], k, 0, K - 1)
            # n - k > 0 and n - k < len(s)
            perT = int(np.ceil(length / _T))
            for t in prange(_T):
                # i - j >= 0
                # i - j < in1
                for i in range(t * perT, min(length, (t + 1) * perT), 1):
                    if i >= start and i < (start + dims[imode]):
                        for j in range(
                                min(max(0, i - in1 + 1), min(K, i + 1)),
                                min(K, i + 1),
                                1
                        ):
                            y[i - start] += kernel[j] * x[i - j]
            return y

        @njit(parallel=True, cache=True)
        def _matmat(x, kernel):
            K = kernel.shape[0]
            batch_size = x.shape[1]
            length = in1 + K - 1
            y = np.full((dims[imode], batch_size), 0.0 * (kernel[0] * x[0, 0]))
            # y[n] = sum(h[k] * s[n - k], k, 0, K - 1)
            # n - k > 0 and n - k < len(s)
            perT = int(np.ceil(length / _T))
            for t in prange(_T):
                # i - j >= 0
                # i - j < in1
                for i in range(t * perT, min(length, (t + 1) * perT), 1):
                    if i >= start and i < (start + dims[imode]):
                        for j in range(
                                min(max(0, i - in1 + 1), min(K, i + 1)),
                                min(K, i + 1),
                                1
                        ):
                            # NumPy uses row-major format
                            for b in range(batch_size):
                                y[i - start, b] += kernel[j] * x[i - j, b]
            return y

        # Because of Numba split 1d and 2d
        @njit(parallel=True, cache=True)
        def _rmatvec(x, kernel):
            K = kernel.shape[0]
            S = x.shape[0]
            length = S + K - 1
            y = np.full(dims[2], 0.0 * (kernel[0] * x[0]))
            # y[n] = sum(h[k] * s[k + n], k, 0, K - 1)
            # k + n < len(s)
            perT = int(np.ceil(length / _T))
            for t in prange(_T):
                for i in range(t * perT, min(length, (t + 1) * perT), 1):
                    if i >= rstart and i < (rstart + dims[2]):
                        for j in range(K):
                            if (j - i + S - 1) >= 0 and (j - i + S - 1) < S:
                                y[dims[2] - 1 - (i - rstart)] += (
                                    kernel[j] * np.conjugate(x[j - i + S - 1])
                                )
            return y

        @njit(parallel=True, cache=True)
        def _rmatmat(x, kernel):
            K = kernel.shape[0]
            S, batch_size = x.shape
            length = S + K - 1
            y = np.full((dims[2], batch_size), 0.0 * (kernel[0] * x[0, 0]))
            # y[n] = sum(h[k] * s[k + n], k, 0, K - 1)
            # k + n < len(s)
            perT = int(np.ceil(length / _T))
            for t in prange(_T):
                for i in range(t * perT, min(length, (t + 1) * perT), 1):
                    if i >= rstart and i < (rstart + dims[2]):
                        for j in range(K):
                            if (j - i + S - 1) >= 0 and (j - i + S - 1) < S:
                                # NumPy uses row-major format
                                for b in range(batch_size):
                                    y[dims[2] - 1 - (i - rstart), b] += (
                                        kernel[j] * np.conjugate(
                                            x[j - i + S - 1, b]
                                        )
                                    )
            return y

        C = LazyLinOp(
            shape=(dim[mode], dim['same']),
            matmat=lambda x: (
                _matvec(x, in2) if x.ndim == 1
                else _matmat(x, in2)
            ),
            rmatmat=lambda x: (
                _rmatvec(x, in2) if x.ndim == 1
                else _rmatmat(x, in2)
            )
        )
    elif compute == 'scipy encapsulation':
        def _matmat(x):
            # x is always 2d
            batch_size = x.shape[1]
            if in2.shape[0] == 2 and batch_size >= 100:
                # Because kernel length is 2 override compute
                # and use the following dedicated function.
                return _conv_filter2(in1, in2, mode=mode) @ x
            elif in2.shape[0] == 3 and batch_size >= 100:
                # Because kernel length is 3 override compute
                # and use the following dedicated function.
                return _conv_filter3(in1, in2, mode=mode) @ x
            elif (
                    mode != 'valid' and
                    batch_size >= 128 and
                    x.shape[0] <= 512 and
                    in2.shape[0] >= 4
            ):
                # In that case using Toeplitz matrix is faster
                y = aslazylinop(
                    sp.linalg.toeplitz(
                        np.pad(in2, (0, x.shape[0] - 1)),
                        r=np.zeros(x.shape[0], dtype=in2.dtype)
                    ))[start:(start + dim[mode]), :] @ x
            else:
                y = np.empty((dim[mode], batch_size),
                             dtype=(x[0, 0] * in2[0]).dtype)
                # Use Dask ?
                for b in range(batch_size):
                    y[:, b] = sp.signal.convolve(x[:, b],
                                                 in2, mode=mode,
                                                 method='auto')
            return y

        def _rmatmat(x):
            # x is always 2d
            batch_size = x.shape[1]
            y = np.empty((dim['same'], batch_size),
                         dtype=(x[0, 0] * in2[0]).dtype)
            # Use Dask ?
            for b in range(batch_size):
                y[:, b] = np.flip(
                    sp.signal.convolve(np.flip(x[:, b]),
                                       in2,
                                       mode=rmode[mode],
                                       method='auto')
                )
            return y
        C = LazyLinOp(
            shape=(dim[mode], dim['same']),
            matmat=lambda x: _matmat(x),
            rmatmat=lambda x: _rmatmat(x),
            dtype=in2.dtype
        )
    elif compute == 'pyfaust toeplitz':
        from pyfaust import toeplitz
        iscomplex = 'complex' in str(in2.dtype)

        def _scalar2array(x):
            if x.shape == ():
                return x.reshape(1, )
            else:
                return x

        def _iscomplex(x, in2):
            return (
                'complex' in str(in2.dtype) or
                'complex' in str(x.dtype)
            )

        C = LazyLinOp(
            shape=(dim[mode], dim['same']),
            matmat=lambda x: _scalar2array(toeplitz(
                np.pad(in2, (0, in1 - 1)),
                np.pad([in2[0]], (0, in1 - 1)),
                diag_opt=False
            )[start:(start + dim[mode]), :] @ x) if _iscomplex(x, in2)
            else np.real(_scalar2array(toeplitz(
                    np.pad(in2, (0, in1 - 1)),
                    np.pad([in2[0]], (0, in1 - 1)),
                    diag_opt=False
            )[start:(start + dim[mode]), :] @ x)),
            rmatmat=lambda x: (
                _scalar2array(
                    toeplitz(
                        np.pad(in2, (0, in1 - 1)),
                        np.pad([in2[0]], (0, in1 - 1)),
                        diag_opt=False
                    )[start:(start + dim[mode]), :].T.conj() @ x
                ) if _iscomplex(x, in2)
                else np.real(_scalar2array(toeplitz(
                        np.pad(in2, (0, in1 - 1)),
                        np.pad([in2[0]], (0, in1 - 1)),
                        diag_opt=False
                )[start:(start + dim[mode]), :].T.conj() @ x))
            )
        )
    elif compute == 'oa':
        C = _oaconvolve(in1, in2, mode=mode, fft_backend='scipy')
    elif 'circ.' in compute:
        tmp_method = method.replace('circ.', '')
        C = _circconvolve(in1, in2, tmp_method, disable_jit)
    else:
        raise ValueError("method is not in " + str(methods))

    return LazyLinOp(
        shape=C.shape,
        matmat=lambda x: (
            C @ x if 'complex' in [str(x.dtype), str(in2.dtype)]
            else np.real(C @ x)
        ),
        rmatmat=lambda x: (
            C.H @ x if 'complex' in [str(x.dtype), str(in2.dtype)]
            else np.real(C.H @ x)
        ),
        dtype=in2.dtype
    )


def _conv_filter2(N: int, in2: np.ndarray, mode: str = 'full'):
    """Construct a convolution lazy linear operator between
    input array of length N and kernel of length 2.

    Args:
        N: int
            Length of the input array.
        in2: np.ndarray
            Kernel (length is 2).
        mode: str, optional
            Convolution mode must be either 'full' (default),
            'valid' or 'same'.

    Returns:
        LazyLinOp
    """
    K = in2.shape[0]
    if mode == 'full':
        L = N + K - 1
    elif mode == 'valid':
        L = N - K + 1
    elif mode == 'same':
        L = N
    else:
        pass
    start = (N + K - 1 - L) // 2
    end = start + L

    def _matmat(x):
        # x is always 2d
        batch_size = x.shape[1]
        if mode == 'full':
            y = np.zeros((L, batch_size),
                         dtype=binary_dtype(x.dtype, in2.dtype))
            y[:N, :] = in2[0] * x[:N, :]
            y[1:(N + 1), :] += in2[1] * x[:N, :]
        elif mode == 'valid':
            y = np.zeros((L, batch_size),
                         dtype=binary_dtype(x.dtype, in2.dtype))
            y[:L, :] = in2[1] * x[:L, :]
            y[:L, :] += in2[0] * x[1:(1 + L), :]
        elif mode == 'same':
            y = in2[0] * x[:N, :]
            y[1:N] += in2[1] * x[:(N - 1), :]
        return y

    def _rmatmat(x):
        # x is always 2d
        batch_size = x.shape[1]
        if mode == 'full':
            y = np.zeros((N, batch_size),
                         dtype=binary_dtype(x.dtype, in2.dtype))
            y[:N, :] = in2[0] * x[:N, :]
            y[:N, :] += in2[1] * x[1:min(L + 1, N + 1), :]
        elif mode == 'valid':
            y = np.zeros((N, batch_size),
                         dtype=binary_dtype(x.dtype, in2.dtype))
            y[:L, :] = in2[1] * x[:L, :]
            y[1:(1 + L), :] += in2[0] * x[:L, :]
        elif mode == 'same':
            y = in2[0] * x[:N, :]
            y[:(N - 1), :] += in2[1] * x[1:N, :]
        return y

    return LazyLinOp(
        shape=(L, N),
        matmat=lambda x: _matmat(x),
        rmatmat=lambda x: _rmatmat(x)
    )


def _conv_filter3(N: int, in2: np.ndarray, mode: str = 'full'):
    """Construct a convolution lazy linear operator between
    input array of length N and kernel of length 2.

    Args:
        N: int
            Length of the input array.
        in2: np.ndarray
            Kernel (length is 2).
        mode: str, optional
            Convolution mode must be either 'full' (default),
            'valid' or 'same'.

    Returns:
        LazyLinOp
    """
    K = in2.shape[0]
    if mode == 'full':
        L = N + K - 1
    elif mode == 'valid':
        L = N - K + 1
    elif mode == 'same':
        L = N
    else:
        pass
    start = (N + K - 1 - L) // 2
    end = start + L

    def _matmat(x):
        # x is always 2d
        batch_size = x.shape[1]
        if mode == 'full':
            y = np.zeros((L, batch_size),
                         dtype=binary_dtype(x.dtype, in2.dtype))
            y[:N, :] = in2[0] * x[:N, :]
            y[1:(N + 1), :] += in2[1] * x[:N, :]
            y[2:(N + 2), :] += in2[2] * x[:N, :]
        elif mode == 'valid':
            y = np.zeros((L, batch_size),
                         dtype=binary_dtype(x.dtype, in2.dtype))
            y[:L, :] = in2[2] * x[:L, :]
            y[:L, :] += in2[1] * x[1:(1 + L), :]
            y[:L, :] += in2[0] * x[2:(2 + L), :]
        elif mode == 'same':
            y = in2[1] * x[:N, :]
            y[1:N] += in2[2] * x[:(N - 1), :]
            y[:(N - 1)] += in2[0] * x[1:N, :]
        return y

    def _rmatmat(x):
        # x is always 2d
        batch_size = x.shape[1]
        if mode == 'full':
            y = np.zeros((N, batch_size),
                         dtype=binary_dtype(x.dtype, in2.dtype))
            y[:N, :] = in2[0] * x[:N, :]
            y[:N, :] += in2[1] * x[1:min(L + 1, N + 1), :]
            y[:N, :] += in2[2] * x[2:min(L + 2, N + 2), :]
        elif mode == 'valid':
            y = np.zeros((N, batch_size),
                         dtype=binary_dtype(x.dtype, in2.dtype))
            y[:L, :] = in2[2] * x[:L, :]
            y[1:(1 + L), :] += in2[1] * x[:L, :]
            y[2:(2 + L), :] += in2[0] * x[:L, :]
        elif mode == 'same':
            y = in2[1] * x[:N, :]
            y[:(N - 1), :] += in2[2] * x[1:N, :]
            y[1:N, :] += in2[0] * x[:(N - 1), :]
        return y

    return LazyLinOp(
        shape=(L, N),
        matmat=lambda x: _matmat(x),
        rmatmat=lambda x: _rmatmat(x)
    )


def _oaconvolve(in1: int, in2: np.ndarray,
                mode: str = 'full', fft_backend: str = 'scipy'):
    """This function implements overlap-add method for convolution.
    Creates Lazy Linear Operator that corresponds to the convolution
    of a signal of length in1 with the kernel in2.
    The function only considers the first dimension of the kernel.
    Do not call _oaconvolve function outside of convolve function.

    Args:
        in1: int
        Length of the input.
        in2: np.ndarray
        Kernel to use for the convolution.
        mode: str, optional

            - 'full' computes convolution (input + padding).
            - 'valid' computes 'full' mode and extract centered
              output that does not depend on the padding.
            - 'same' computes 'full' mode and extract centered
              output that has the same shape that the input.
        fft_backend: str, optional
            See :py:func:`fft` for more details.

    Returns:
        LazyLinOp

    Raises:
        Exception
        kernel number of dimensions < 1.
        ValueError
        mode is either 'full' (default), 'valid' or 'same'
        ValueError
        Length of the input are expected (int).
        ValueError
        size of the kernel is greater than the size of the signal.
    """
    # Do not need to check mode because convolve already did it.
    # Indeed convolve calls _oaconvolve.
    # if not mode in ['full', 'valid', 'same']:
    #     raise ValueError("mode is either 'full' (default)," +
    #                      " 'valid' or 'same'")
    # Do not need to check in1 because convolve already did it.
    # Indeed convolve calls _oaconvolve.
    # if not type(in1) is int:
    #     raise ValueError("Length of the input are expected (int).")

    # size of the kernel
    K = in2.shape[0]
    # if K > in1:
    #     raise ValueError("size of the kernel is greater" +
    #                      " than the size of the signal.")
    # size of the output (full mode)
    Y = in1 + K - 1

    # block size B, number of blocks X = in1 / B
    B = K
    while B < min(in1, K) or not is_power_of_two(B):
        B += 1

    # number of blocks
    step = B
    B *= 2
    R = in1 % step
    X = in1 // step + 1 if R > 0 else in1 // step

    # Create linear operator C that will be applied to all the blocks.
    # C = ifft(np.diag(fft(kernel)) @ fft(signal))
    # use Kronecker product between identity matrix
    # and C to apply to all the blocks.
    # We can also use block_diag operator.
    # Use mpad to pad each block.
    if in1 > (2 * K):
        # If the signal size is greater than twice
        # the size of the kernel use overlap-based convolution
        D = diag(fft(B, backend=fft_backend) @ eye(B, n=K, k=0) @ in2, k=0)
        F = fft(B,
                backend=fft_backend,
                norm='forward').H @ D @ fft(B, backend=fft_backend)
        # block_diag(*[F] * X) is equivalent to kron(eye, F)
        # C = oa(B, X, overlap=B - step) @ kron(eye(X, n=X, k=0), F) \
        #     @ mpad2(step, X, n=B - step)
        C = oa(B, X, overlap=B - step) @ block_diag(*[F] * X) \
            @ mpad2(step, X, n=B - step)
        if (X * step) > in1:
            C = C @ eye(X * step, n=in1, k=0)
    else:
        # if the signal size is not greater than twice
        # the size of the kernel use FFT-based convolution
        F = fft(Y, backend=fft_backend)
        D = diag(F @ eye(Y, n=K, k=0) @ in2, k=0)
        C = fft(Y,
                backend=fft_backend,
                norm='forward').H @ D @ F @ eye(Y, n=in1, k=0)

    # convolution mode
    if mode == 'valid':
        # compute full mode, valid mode returns
        # elements that do not depend on the padding
        extract = in1 - K + 1
        start = (Y - extract) // 2
    elif mode == 'same':
        # keep the middle of full mode (centered)
        # and returns the same size that the signal size
        extract = in1
        start = (Y - extract) // 2
    else:
        # compute full mode
        extract = Y
        start = 0
    indices = np.arange(start, start + extract, 1)
    # use eye operator to extract
    C = eye(extract, n=C.shape[0], k=start) @ C

    iscomplex = 'complex' in str(in2.dtype)

    def _batch(op, x):
        # x is always 2d
        batch_size = x.shape[1]
        y = np.empty((op.shape[0], batch_size),
                     dtype=binary_dtype(op.dtype, x.dtype))
        # print(op.dtype, x.dtype, y.dtype)
        # use Dask ?
        for b in range(batch_size):
            y[:, b] = op @ x[:, b]
        return y

    return LazyLinOp(
        shape=(C.shape[0], in1),
        matmat=lambda x: _batch(C, x) if (
            iscomplex or 'complex' in str(x.dtype)
        )
        else np.real(_batch(C, x)),
        rmatmat=lambda x: _batch(C.H, x) if (
            iscomplex or 'complex' in str(x.dtype)
        )
        else np.real(_batch(C.H, x))
    )


def _circconvolve(in1: int, in2: np.ndarray,
                  method: str = 'auto', disable_jit: int = 0):
    """Creates a lazy linear operator that corresponds to circular convolution.
    Length of the signal and length of the kernel K must be the same.
    If not, pad the signal (resp. the kernel) if in1 > K (resp. K < in1).
    Do not call _circconvolve function outside of convolve function.

    Args:
        in1: int
            Length of the input.
        in2: np.ndarray
            Kernel to use for the convolution.
        method: str, optional

            - 'auto' use best implementation.
            - 'direct' direct computation using
              nested for loops (Numba implementation).
              Larger the signal is better the performances are.
            - 'scipy fft' use Scipy implementation of the FFT.
            - 'pyfaust circ' use pyfaust implementation of circulant matrix.
            - 'pyfaust dft' use pyfaust implementation
              of DFT (allows only power of two).
        disable_jit: int, optional
            If 0 (default) disable Numba jit.

    Returns:
        LazyLinOp

    Raises:
        ValueError
            Expects shape of the input.
        Exception
            Kernel size must be <= signal size.
        Exception
            Length of the signal is not a power of two.
        ValueError
            method is not in ['auto', 'direct', 'scipy fft',
            'pyfaust circ', 'pyfaust dft'].
    """
    # Do not need to check in1 because convolve already did it.
    # Indeed convolve calls _circconvolve.
    # if not type(in1) is int:
    #     raise ValueError("Expects shape of the int.")

    # size of the kernel
    K = in2.shape[0]
    if K > in1:
        raise Exception("Kernel size must be <= signal size.")

    if method == 'pyfaust dft' and not is_power_of_two(in1):
        raise Exception("Length of the signal is not a power of two.")

    pin2 = np.pad(in2, (0, in1 - K), mode='constant', constant_values=0.0)

    new_method = method
    try:
        import numba as nb
        from numba import njit, prange, set_num_threads, threading_layer
        _T = nb.config.NUMBA_NUM_THREADS
        nb.config.THREADING_LAYER = 'omp'
        nb.config.DISABLE_JIT = disable_jit
    except ImportError:
        if new_method == 'direct':
            warn("Did not find Numba, switch to scipy fft.")
            new_method = 'scipy fft'

    if new_method == 'direct':

        @njit(parallel=True, cache=True)
        def _matvec(kernel, signal):
            K = kernel.shape[0]
            output = np.full(in1, 0.0)
            # y[n] = sum(h[k] * s[n - k mod N], k, 0, K - 1)
            perT = int(np.ceil(in1 / _T))
            for t in prange(_T):
                for i in range(t * perT, min(in1, (t + 1) * perT), 1):
                    for j in range(K):
                        output[i] += kernel[j] * signal[np.mod(i - j, in1)]
            return output

        @njit(parallel=True, cache=True)
        def _matmat(kernel, signal):
            K = kernel.shape[0]
            B = signal.shape[1]
            output = np.full((in1, B), 0.0)
            # y[n] = sum(h[k] * s[n - k mod N], k, 0, K - 1)
            perT = int(np.ceil(in1 / _T))
            for t in prange(_T):
                for i in range(t * perT, min(in1, (t + 1) * perT), 1):
                    for j in range(K):
                        # NumPy uses row-major format
                        for b in range(B):
                            output[i, b] += (
                                kernel[j] * signal[np.mod(i - j, in1), b]
                            )
            return output

        @njit(parallel=True, cache=True)
        def _rmatvec(kernel, signal):
            K = kernel.shape[0]
            output = np.full(in1, 0.0)
            # y[n] = sum(h[k] * s[k + n mod N], k, 0, K - 1)
            perT = int(np.ceil(in1 / _T))
            for t in prange(_T):
                for i in range(t * perT, min(in1, (t + 1) * perT), 1):
                    for j in range(K):
                        output[i] += kernel[j] * signal[np.mod(i + j, in1)]
            return output

        @njit(parallel=True, cache=True)
        def _rmatmat(kernel, signal):
            K = kernel.shape[0]
            B = signal.shape[1]
            output = np.full((in1, B), 0.0)
            # y[n] = sum(h[k] * s[k + n mod N], k, 0, K - 1)
            perT = int(np.ceil(in1 / _T))
            for t in prange(_T):
                for i in range(t * perT, min(in1, (t + 1) * perT), 1):
                    for j in range(K):
                        # NumPy uses row-major format
                        for b in range(B):
                            output[i, b] += (
                                kernel[j] * signal[np.mod(i + j, in1), b]
                            )
            return output

        C = LazyLinOp(
            shape=(in1, in1),
            matmat=lambda x: _matvec(pin2,
                                     x) if x.ndim == 1 else _matmat(pin2, x),
            rmatmat=lambda x: _rmatvec(pin2,
                                       x) if x.ndim == 1 else _rmatmat(pin2, x)
        )
    elif new_method == 'scipy fft' or new_method == 'auto':
        # Op = FFT^-1 @ diag(FFT(kernel)) @ FFT
        D = diag(fft(in1, backend='scipy') @ pin2, k=0)
        F = fft(in1,
                backend='scipy',
                norm='forward').H @ D @ fft(in1, backend='scipy')
        C = LazyLinOp(
            shape=(in1, in1),
            matvec=lambda x: (
                F @ x if 'complex' in [str(pin2.dtype), str(x.dtype)]
                else np.real(F @ x)
            ),
            rmatvec=lambda x: (
                F.H @ x if 'complex' in [str(pin2.dtype), str(x.dtype)]
                else np.real(F.H @ x)
            )
        )
    elif new_method == 'pyfaust circ':
        from pyfaust import circ
        C = LazyLinOp(
            shape=(in1, in1),
            matvec=lambda x: (
                circ(pin2) @ x if 'complex' in (
                    [str(pin2.dtype), str(x.dtype)]
                )
                else np.real(circ(pin2) @ x)
            ),
            rmatvec=lambda x: (
                circ(pin2).H @ x if 'complex' in (
                    [str(pin2.dtype), str(x.dtype)]
                )
                else np.real(circ(pin2).H @ x)
            )
        )
    elif new_method == 'pyfaust dft':
        from pyfaust import dft
        F = aslazylinop(dft(in1, normed=False))
        fft_kernel = F @ pin2
        A = F.H @ diag(fft_kernel, k=0) @ F
        AH = F.H @ diag(fft_kernel.conj(), k=0) @ F
        C = LazyLinOp(
            shape=(in1, in1),
            matvec=lambda x: (
                np.multiply(1.0 / in1, A @ x) if 'complex' in (
                    [str(pin2.dtype), str(x.dtype)]
                )
                else np.multiply(1.0 / in1, np.real(A @ x))
            ),
            rmatvec=lambda x: (
                np.multiply(1.0 / in1, AH @ x) if 'complex' in (
                    [str(pin2.dtype), str(x.dtype)]
                )
                else np.multiply(1.0 / in1, np.real(AH @ x))
            )
        )
    # else:
    #     # Do not need to check method because convolve already did it.
    #     # Indeed convolve calls _circconvolve.
    #     raise ValueError("method is not in ['auto', 'direct'," +
    #                      " 'scipy fft', 'pyfaust circ', 'pyfaust dft']")

    # return lazy linear operator
    return C


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

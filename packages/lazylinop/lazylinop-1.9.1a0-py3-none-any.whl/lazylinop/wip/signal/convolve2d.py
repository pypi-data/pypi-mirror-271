import numpy as np
import scipy as sp
from lazylinop import LazyLinOp
from lazylinop.basicops import add, diag, eye, kron
import sys
from lazylinop.basicops.pad import kron_pad
from lazylinop.wip.signal import bc2d, convolve
import warnings
from warnings import warn
warnings.simplefilter(action='always')
sys.setrecursionlimit(100000)


def convolve2d(in1: tuple, in2: np.ndarray,
               mode: str = 'full', boundary: str = 'fill',
               method: str = 'auto', **kwargs):
    r"""Constructs a 2d convolution lazy linear operator C.
    C @ X.flatten() is the result of the convolution.
    Of note, 2d-array X has been flattened.
    The output is also flattened and you have to reshape it
    according to the convolution mode.
    Toeplitz based method use the fact that convolution of a
    kernel with an image can be written as a sum of Kronecker
    product between eye and Toeplitz matrices.

    Args:
        in1: tuple,
        Shape (X, Y) of the signal to convolve with kernel.
        in2: np.ndarray
        Kernel to use for the convolution, shape is (K, L)
        mode: str, optional
        'full' computes convolution (input + padding)
        'valid' computes 'full' mode and extract centered output
        that does not depend on the padding.
        'same' computes 'full' mode and extract centered output
        that has the same shape that the input.
        See also Scipy documentation of scipy.signal.convolve
        function for more details
        boundary: str, optional
        'fill' pads input array with zeros (default)
        'wrap' periodic boundary conditions
        'symm' symmetrical boundary conditions
        method: str, optional
        'auto' to use the best method according to the kernel and
        input array dimensions.
        'scipy encapsulation' use scipy.signal.convolve2d as a
        lazy linear operator
        'scipy toeplitz' to use lazy encapsulation of Scipy
        implementation of Toeplitz matrix.
        'pyfaust toeplitz' to use FAuST implementation of Toeplitz matrix.
        'scipy fft' to use Fast-Fourier-Transform to compute convolution.

    Returns:
        LazyLinOp or np.ndarray

    Raises:
        ValueError
            mode is either 'full' (default), 'valid' or 'same'.
        ValueError
            boundary is either 'fill' (default), 'wrap' or 'symm'
        Exception
            Size of the kernel is greater than the size of
            signal (mode is valid).
        ValueError
            Unknown method.
        Exception
            in1 expects tuple as (X, Y).
        Exception
            in1 expects array with shape (X, Y).
        ValueError
            Negative dimension value is not allowed.

    Examples:
        >>> from lazylinop.wip.signal import convolve2d
        >>> import scipy as sp
        >>> X = np.random.randn(6, 6)
        >>> kernel = np.random.randn(3, 3)
        >>> c1 = convolve2d(X.shape, kernel, mode='same') @ X.flatten()
        >>> c2 = sp.signal.convolve2d(X, kernel, mode='same').flatten()
        >>> np.allclose(c1, c2)
        True

    .. seealso::
        `<https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve2d.html>`_
    """
    if boundary not in ['fill', 'wrap', 'symm']:
        raise ValueError("boundary is either 'fill' (default) " +
                         ", 'wrap' or 'symm'")

    if type(in1) is tuple:
        if len(in1) != 2:
            raise Exception("in1 expects tuple (X, Y).")
        X, Y = in1[0], in1[1]
    else:
        raise Exception("in1 expects tuple (X, Y).")

    if X <= 0 or Y <= 0:
        raise ValueError("zero or negative dimension is not allowed.")
    K, L = in2.shape
    if (K > X or L > Y) and mode == 'valid':
        raise Exception("Size of the kernel is greater than the size" +
                        " of the image (mode is valid).")
    if K <= 0 or L <= 0:
        raise ValueError("Negative dimension value is not allowed.")

    if method == 'auto':
        compute = 'scipy fft' if max(K, L) >= 32 else 'kronecker'
    else:
        compute = method

    if compute == 'scipy encapsulation' and (boundary == 'wrap'
                                             or boundary == 'symm'):
        raise Exception("scipy encapsulation method has no" +
                        " implementation of wrap and symm boundaries.")

    # boundary conditions
    if boundary == 'fill' or compute == 'scipy encapsulation':
        # SciPy encapsulation uses boundary argument of SciPy function
        B = 1
    else:
        if K > X or L > Y:
            B = 1 + 2 * 2 * max(max(0, int(np.ceil((K - X) / X))),
                                int(np.ceil((L - Y) / Y)))
        else:
            # add one input on both side of each axis
            B = 3

    # shape of the output image (full mode)
    # it takes into account the boundary conditions
    P, Q = B * X + K - 1, B * Y + L - 1

    # length of the output as a function of convolution mode
    xdim = {}
    xdim['full'] = B * X + K - 1
    xdim['valid'] = B * X - K + 1
    xdim['same'] = B * X
    ydim = {}
    ydim['full'] = B * Y + L - 1
    ydim['valid'] = B * Y - L + 1
    ydim['same'] = B * Y

    imode = (
        0 * int(mode == 'full') + 1 * int(mode == 'valid') +
        2 * int(mode == 'same') + 3 * int(mode == 'circ')
    )
    rmode = {}
    rmode['full'] = 'valid'
    rmode['valid'] = 'full'
    rmode['same'] = 'same'
    xy = {}
    xy['full'] = (X + K - 1) * (Y + L - 1)
    xy['valid'] = (X - K + 1) * (Y - L + 1)
    xy['same'] = X * Y

    if mode == 'full':
        i1 = (P - (X + K - 1)) // 2
        s1 = i1 + X + K - 1
        i2 = (Q - (Y + L - 1)) // 2
        s2 = i2 + Y + L - 1
    elif mode == 'valid':
        # compute full mode and extract what we need
        # number of rows to extract is X - K + 1 (centered)
        # number of columns to extract is Y - L + 1 (centered)
        # if boundary conditions extract image from the center
        i1 = (P - (X - K + 1)) // 2
        s1 = i1 + X - K + 1
        i2 = (Q - (Y - L + 1)) // 2
        s2 = i2 + Y - L + 1
    elif mode == 'same':
        # keep middle of the full mode
        # number of rows to extract is M (centered)
        # number of columns to extract is N (centered)
        # if boundary conditions extract image from the center
        i1 = (P - X) // 2
        s1 = i1 + X
        i2 = (Q - Y) // 2
        s2 = i2 + Y
    else:
        raise ValueError("mode is either 'full' (default), 'valid' or 'same'.")

    if compute == 'scipy encapsulation':
        # correlate2d is the adjoint operator of convolve2d
        def _matmat(x):
            # x is always 2d
            batch_size = x.shape[1]
            # use Dask ?
            y = np.empty((xdim[mode] * ydim[mode], batch_size),
                         dtype=(x[0, 0] * in2[0, 0]).dtype)
            for b in range(batch_size):
                y[:, b] = sp.signal.convolve2d(
                    x[:, b].reshape(xdim['same'], ydim['same']),
                    in2, mode=mode, boundary=boundary).ravel()
            return y

        def _rmatmat(x):
            # x is always 2d
            batch_size = x.shape[1]
            # use Dask ?
            y = np.empty((xdim['same'] * ydim['same'], batch_size),
                         dtype=(x[0, 0] * in2[0, 0]).dtype)
            for b in range(batch_size):
                y[:, b] = sp.signal.correlate2d(
                    x[:, b].reshape(xdim[mode], ydim[mode]),
                    in2, mode=rmode[mode], boundary=boundary).ravel()
            return y
        C = LazyLinOp(
            shape=(xdim[mode] * ydim[mode], xdim['same'] * ydim['same']),
            matmat=lambda x: _matmat(x),
            rmatmat=lambda x: _rmatmat(x)
        )
    elif compute == 'scipy fft' or compute == 'auto':
        from lazylinop.wip.signal import fft2
        F = fft2((P, Q), backend='scipy', norm='ortho')

        # Operator to pad both flattened kernel and input
        # according to convolution mode.
        # scipy.signal.convolve2d adds 0 only on one side along both axis
        # input
        x1 = 0
        x2 = xdim['full'] - xdim['same'] - x1
        y1 = 0
        y2 = ydim['full'] - ydim['same'] - y1
        P1 = kron_pad((xdim['same'], ydim['same']), ((x1, x2), (y1, y2)))
        # kernel
        x1 = 0
        x2 = xdim['full'] - K - x1
        y1 = 0
        y2 = ydim['full'] - L - y1
        P2 = kron_pad((K, L), ((x1, x2), (y1, y2)))

        Fin2 = np.multiply(np.sqrt(P * Q), F @ P2 @ in2.flatten())
        C = F.H @ (diag(Fin2, k=0) @ F) @ P1
        if boundary == 'wrap' or boundary == 'symm':
            C = C @ bc2d((X, Y), x=(B - 1) // 2, y=(B - 1) // 2,
                         boundary=boundary)
        # extract center of the output
        indices = ((np.arange(P * Q).reshape(P, Q))[i1:s1, i2:s2]).ravel()
        C = C[indices, :]
    elif compute == 'kronecker':
        # Write 2d convolution as a sum of Kronecker products:
        # input * kernel = sum(kron(E_i, convolve_i), i, 1, M)
        # E_i is an eye matrix eye(P, n=X, k=-i).
        Ops = [None] * K
        for i in range(K):
            Ops[i] = kron(
                eye(xdim['full'], n=xdim['same'], k=-i),
                convolve(B * Y, in2[i, :], method='direct', mode='full')
            )
        C = add(*Ops)
        # Add boundary conditions
        if boundary == 'wrap' or boundary == 'symm':
            C = C @ bc2d((X, Y), x=(B - 1) // 2, y=(B - 1) // 2,
                         boundary=boundary)
        # Extract center of the output
        C = C[
            (
                (
                    np.arange(
                        xdim['full'] * ydim['full']
                    ).reshape(xdim['full'], ydim['full'])
                )[i1:s1, i2:s2]
            ).ravel(), :]
    elif compute == 'pyfaust toeplitz' or compute == 'scipy toeplitz':
        # write 2d convolution as a sum of Kronecker products:
        # input * kernel = sum(kron(E_i, T_i), i, 1, M)
        # E_i is an eye matrix eye(P, n=X, k=-i).
        # T_i is a Toeplitz matrix build from the kernel.
        # first column is the i-th row of the kernel.
        # first row is 0
        if compute == 'pyfaust toeplitz':
            from pyfaust import toeplitz
        Ops = [None] * K
        for i in range(K):
            if method == 'pyfaust toeplitz':
                Ops[i] = kron(
                    eye(xdim['full'], n=xdim['full'], k=-i),
                    toeplitz(np.pad(in2[i, :], (0, ydim['same'] - 1)),
                             np.pad([in2[i, 0]], (0, ydim['full'] - 1)),
                             diag_opt=True)
                )
            else:
                # Default
                Ops[i] = kron(
                    eye(xdim['full'], n=xdim['full'], k=-i),
                    sp.linalg.toeplitz(np.pad(in2[i, :],
                                              (0, ydim['same'] - 1)),
                                       np.full(ydim['full'], 0.0))
                )
        # Operator to pad the flattened image
        # scipy.signal.convolve2d adds 0 only on one side along both axis
        C = add(*Ops) @ kron_pad((xdim['same'], ydim['same']),
                                 ((0, xdim['full'] - xdim['same']),
                                  (0, ydim['full'] - ydim['same'])))
        # Add boundary conditions
        if boundary == 'wrap' or boundary == 'symm':
            C = C @ bc2d((X, Y),
                         x=(B - 1) // 2, y=(B - 1) // 2, boundary=boundary)
        # Extract center of the output
        C = C[
            (
                (
                    np.arange(xdim['full'] * ydim['full']).reshape(
                        xdim['full'], ydim['full'])
                )[i1:s1, i2:s2]
            ).ravel(), :]
    else:
        raise ValueError('Unknown method.')

    # return lazy linear operator
    # pyfaust toeplitz returns 'complex' even if argument is 'real'
    ckernel = 'complex' in str(in2.dtype)
    return LazyLinOp(
        shape=C.shape,
        matmat=lambda x: (
            C @ x if ckernel or 'complex' in str(x.dtype)
            else np.real(C @ x)
        ),
        rmatmat=lambda x: (
            C.H @ x if ckernel or 'complex' in str(x.dtype)
            else np.real(C.H @ x)
        )
    )


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

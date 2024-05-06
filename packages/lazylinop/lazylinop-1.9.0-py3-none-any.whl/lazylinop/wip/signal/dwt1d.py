import numpy as np
from lazylinop import LazyLinOp
import pywt
import sys
from lazylinop.basicops import block_diag, eye, vstack
from lazylinop.wip.signal import bc, convolve, ds_mconv, slices

sys.setrecursionlimit(100000)


def dwt1d(N: int,
          wavelet: pywt.Wavelet = pywt.Wavelet("haar"),
          mode: str = 'zero', level: int = None,
          backend: str = 'pywavelets', **kwargs):
    """Constructs a Discrete Wavelet Transform (DWT) lazy linear operator.
    For the first level of decomposition Op @ x returns the array [cA, cD]
    while for the nth level of decomposition Op @ x returns the
    array [cAn, cDn, cDn-1, ..., cD2, cD1]. The 1d array of coefficients
    corresponds to the concatenation of the list of arrays Pywavelets returns.
    Of note, the function follows the format returned by Pywavelets module.

    Args:
        N: int
            Size of the input array.
        wavelet: pywt.Wavelet
            Wavelet from Pywavelets module.
        mode: str, optional

            - 'periodic', signal is treated as periodic signal.
            - 'symmetric', use mirroring to pad the signal.
            - 'zero', signal is padded with zeros (default).
        level: int, optional
            Decomposition level, by default (None) return all.
        kwargs:
            lfilter: np.ndarray
                Quadrature mirror low-pass filter.
            hfilter: np.ndarray
                Quadrature mirror high-pass filter.
                If lfilter and hfilter, ignore wavelet argument.
        backend: str, optional
            'pywavelets' (default) or 'pyfaust' for the underlying
            computation of the DWT.

    Returns:
        The DWT LazyLinOp.

    Raises:
        ValueError
            Decomposition level must be >= 0.
        ValueError
            mode is either 'periodic', 'symmetric' or 'zero'.
        ValueError
            level is greater than the maximum decomposition level.
        ValueError
            backend must be either 'pywavelets' or 'lazylinop'.
        ValueError
            backend 'pywavelets' works only for mode='zero'.
            We are currently implementing adjoint for others modes.

    Examples:
        >>> from lazylinop.wip.signal import dwt1d
        >>> import numpy as np
        >>> import pywt
        >>> N = 8
        >>> x = np.arange(1, N + 1, 1)
        >>> Op = dwt1d(N, mode='periodic', level=1, backend='lazylinop')
        >>> y = Op @ x
        >>> z = pywt.wavedec(x, wavelet='haar', mode='periodic', level=1)
        >>> np.allclose(y, np.concatenate(z))
        True

    .. seealso::
        `Pywavelets module <https://pywavelets.readthedocs.io/en/
        latest/index.html>`_,
        `Wavelets <https://pywavelets.readthedocs.io/en/latest/
        regression/wavelet.html>`_,
        `Extension modes <https://pywavelets.readthedocs.io/en/
        latest/ref/signal-extension-modes.html>`_
    """

    if level is not None and level < 0:
        raise ValueError("Decomposition level must be >= 0.")
    if mode not in ['zero', 'symmetric', 'periodic']:
        raise ValueError("mode is either 'periodic', 'symmetric' or 'zero'.")
    if level is not None and level == 0:
        # Nothing to decompose, return identity matrix
        return eye(N, n=N, k=0)

    if backend == 'pywavelets':
        if mode != 'zero':
            str1 = "backend 'pywavelets' works only for mode='zero'."
            str2 = "We are currently implementing adjoint for others modes."
            raise ValueError(str1 + '\n' + str2)

        # Name of the wavelet to use with rmatmat
        if 'rbio' in wavelet.name:
            rwavelet = 'bior' + wavelet.name[-3:]
        elif 'bior' in wavelet.name:
            rwavelet = 'rbio' + wavelet.name[-3:]
        else:
            rwavelet = wavelet.name
        # Wavelet length
        W = wavelet.dec_len

        # Compute length of the output (number of coefficients)
        tmp = N
        ncoeffs = 0
        for i in range(pywt.dwt_max_level(N, W) if level is None else level):
            # Number of details coefficients
            tmp = pywt.dwt_coeff_len(tmp, W, mode=mode)
            ncoeffs += tmp
        # Number of approximation coefficients
        ncoeffs += tmp

        def _matmat(x):
            # Decomposition (return array from coefficients)
            # x is always 2d
            y = pywt.coeffs_to_array(
                pywt.wavedecn(
                    x, wavelet=wavelet.name,
                    level=level, mode=mode, axes=(0, )
                ), axes=(0, ))[0]
            return y

        def _rmatmat(x):
            # Reconstruction
            # x is always 2d
            # Get slices for further reconstruction
            tmp = np.full((N, x.shape[1]), 1.0)
            slices = pywt.coeffs_to_array(
                pywt.wavedecn(
                    tmp, wavelet=wavelet.name,
                    level=level, mode=mode, axes=(0, )
                ), axes=(0, ))[1]
            x = pywt.array_to_coeffs(x, slices, output_format='wavedecn')
            y = pywt.waverecn(x, wavelet=rwavelet, mode=mode, axes=(0, ))
            return y[:N, :]

        return LazyLinOp(
            shape=(ncoeffs, N),
            matmat=lambda x: _matmat(x),
            rmatmat=lambda x: _rmatmat(x)
        )
    elif backend == 'lazylinop':

        # "Home-made" low and high-pass filters
        if 'lfilter' in kwargs.keys() and 'hfilter' in kwargs.keys():
            lfilter = kwargs['lfilter']
            hfilter = kwargs['hfilter']
            wavelet_name = 'unknown'
        else:
            lfilter = np.asarray(wavelet.dec_lo)
            hfilter = np.asarray(wavelet.dec_hi)
            wavelet_name = wavelet.name
        W = hfilter.shape[0]
        if W > N:
            # Nothing to decompose, return identity matrix
            return eye(N, n=N, k=0)

        boffset = bool(wavelet_name == 'bior3.1' or
                       wavelet_name == 'bior3.3' or
                       wavelet_name == 'bior3.5' or
                       wavelet_name == 'bior3.7' or
                       wavelet_name == 'bior3.9' or
                       wavelet_name == 'bior5.5' or
                       wavelet_name == 'coif2' or
                       wavelet_name == 'coif4' or
                       wavelet_name == 'coif6' or
                       wavelet_name == 'coif8' or
                       wavelet_name == 'coif10' or
                       wavelet_name == 'coif12' or
                       wavelet_name == 'coif14' or
                       wavelet_name == 'coif16' or
                       wavelet_name == 'db2' or
                       wavelet_name == 'db4' or
                       wavelet_name == 'db6' or
                       wavelet_name == 'db8' or
                       wavelet_name == 'db10' or
                       wavelet_name == 'db12' or
                       wavelet_name == 'db14' or
                       wavelet_name == 'db16' or
                       wavelet_name == 'db18' or
                       wavelet_name == 'db20' or
                       wavelet_name == 'db22' or
                       wavelet_name == 'db24' or
                       wavelet_name == 'db26' or
                       wavelet_name == 'db28' or
                       wavelet_name == 'db30' or
                       wavelet_name == 'db32' or
                       wavelet_name == 'db34' or
                       wavelet_name == 'db36' or
                       wavelet_name == 'db38' or
                       wavelet_name == 'rbio3.1' or
                       wavelet_name == 'rbio3.3' or
                       wavelet_name == 'rbio3.5' or
                       wavelet_name == 'rbio3.7' or
                       wavelet_name == 'rbio3.9' or
                       wavelet_name == 'rbio5.5' or
                       wavelet_name == 'sym2' or
                       wavelet_name == 'sym4' or
                       wavelet_name == 'sym6' or
                       wavelet_name == 'sym8' or
                       wavelet_name == 'sym10' or
                       wavelet_name == 'sym12' or
                       wavelet_name == 'sym14' or
                       wavelet_name == 'sym16' or
                       wavelet_name == 'sym18' or
                       wavelet_name == 'sym20')

        # Maximum decomposition level: stop decomposition when
        # the signal becomes shorter than the filter length
        K = int(np.log2(N / (W - 1)))
        if level is not None and level > K:
            raise ValueError("level is greater than the" +
                             " maximum decomposition level.")
        D = K if level is None else level

        if D == 0:
            # Nothing to decompose, return identity matrix
            return eye(N, n=N, k=0)

        # Loop over the decomposition level
        for i in range(D):
            # Low and high-pass filters + decimation
            npd = W - 2
            if i == 0:
                # Boundary conditions
                NN = N + 2 * npd
                if mode == 'zero':
                    NN += NN % 2
                    B = eye(NN, n=N, k=-npd)
                else:
                    mx = NN % 2
                    bn = npd
                    an = npd + mx
                    NN += mx
                    B = bc(N, n=0, bn=bn, an=an, boundary=mode)
            else:
                # Boundary conditions
                NN = cx + 2 * npd
                if mode == 'zero':
                    NN += NN % 2
                    B = eye(NN, n=cx, k=-npd)
                else:
                    mx = NN % 2
                    bn = npd
                    an = npd + mx
                    NN += mx
                    B = bc(cx, n=0, bn=bn, an=an, boundary=mode)
            offset_d = int(
                (npd % 2) == 0) if mode == 'zero' else int((bn % 2) == 0)
            if boffset:
                offset_d = 0
            if 0:
                # Convolution low and high-pass filters + down-sampling
                GH = ds_mconv(NN, lfilter, hfilter,
                              mode='same', offset=offset_d, every=2) @ B
            else:
                # Convolution
                G = convolve(NN, lfilter, mode='same',
                             method='scipy encapsulation')
                H = convolve(NN, hfilter, mode='same',
                             method='scipy encapsulation')
                # Down-sampling
                DG = slices(G.shape[0], [], [], 1, 2, (offset_d, None))
                DH = slices(H.shape[0], [], [], 1, 2, (offset_d, None))
                # Vertical stack
                GH = vstack((DG @ G, DH @ H)) @ B
            # Extract approximation and details coefficients cA, cD
            cx = ((N if i == 0 else cx) + W - 1) // 2
            offset = (NN // 2 - cx) // 2
            if boffset:
                offset += 1
            # Slices to extract cA and cD
            V = slices(GH.shape[0], [offset, offset + NN // 2],
                       [offset + cx - 1, offset + NN // 2 + cx - 1])
            if i == 0:
                # First level of decomposition
                Op = V @ GH
            else:
                # Apply low and high-pass filters + decimation only to cA
                # Because of lazy linear operator V, cA always comes first
                Op = block_diag(*[V @ GH,
                                  eye(Op.shape[0] - GH.shape[1],
                                      n=Op.shape[0] - GH.shape[1], k=0)]) @ Op
        return Op
    else:
        raise ValueError("backend must be either 'pywavelets' or 'lazylinop'.")


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

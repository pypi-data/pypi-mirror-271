import numpy as np
import scipy as sp
from lazylinop import LazyLinOp
from lazylinop.basicops import block_diag, eye, kron, vstack
from lazylinop.wip.signal import bc, convolve, slices
from lazylinop.wip.signal import ds_mconv
import pywt
import sys
sys.setrecursionlimit(100000)


def dwt2d(shape: tuple, wavelet: pywt.Wavelet = pywt.Wavelet("haar"),
          mode: str = 'zero', level: int = None,
          backend: str = 'pywavelets', **kwargs):
    """Constructs a multiple levels 2d DWT lazy linear operator.
    If the lazy linear operator is applied to a 1d array it returns
    the array [cA, cH, cV, cD] for the first decomposition level.
    For the nth level of decomposition it returns
    the array [cAn, cHn, cVn, cDn, ..., cH1, cV1, cD1].
    cAn matrix has been flattened as-well-as the cHs, cVs and cDs.
    The 1d array of coefficients corresponds
    to the concatenation of the list of arrays Pywavelets returns.
    Of note, you must apply DWT LazyLinOp to a flattened 2d array.

    Args:
        shape: tuple
            Shape of the 2d input array (M, N).
        wavelet: pywt.Wavelet
            Wavelet from Pywavelets module.
        mode: str, optional

            - 'periodic', image is treated as periodic image
            - 'symmetric', use mirroring to pad the signal
            - 'zero', signal is padded with zeros (default)
        level: int, optional
            If level is None compute full decomposition (default).
        backend: str, optional
            'pywavelets' (default) or 'pyfaust' for the underlying
            computation of the DWT.
        kwargs:
            lfilter: np.ndarray
            Quadrature mirror low-pass filter.
            hfilter: np.ndarray
            Quadrature mirror high-pass filter.
            If lfilter and hfilter and backend='lazylinop',
            ignore wavelet argument.

    Returns:
        LazyLinOp

    Raises:
        Exception
            Shape expects tuple (M, N).
        ValueError
            Decomposition level must be >= 0.
        Exception
            Decomposition level is greater than the maximum
            decomposition level.
        ValueError
            mode is either 'zero', 'periodic' or 'symmetric'.
        ValueError
            backend must be either 'pywavelets' or 'lazylinop'.
        ValueError
            backend 'pywavelets' works only for mode='zero'.
            We are currently implementing adjoint for others modes.
        Exception
            Length of the wavelet must be > 1.

    Examples:
        >>> from lazylinop.wip.signal import dwt2d
        >>> import numpy as np
        >>> import pywt
        >>> X = np.array([[1., 2.], [3., 4.]])
        >>> Op = dwt2d(X.shape, wavelet=pywt.Wavelet('haar'), level=1)
        >>> y = Op @ X.flatten()
        >>> cA, (cH, cV, cD) = pywt.wavedec2(X, wavelet='haar', level=1)
        >>> z = np.concatenate([cA, cH, cV, cD], axis=1)
        >>> np.allclose(y, z)
        True

    .. seealso::
        `Pywavelets module <https://pywavelets.readthedocs.io/en/
        latest/ref/2d-dwt-and-idwt.html#ref-dwt2>`_,
        `Wavelets <https://pywavelets.readthedocs.io/en/latest/
        regression/wavelet.html>`_,
        `Extension modes <https://pywavelets.readthedocs.io/en/
        latest/ref/signal-extension-modes.html>`_
    """
    if type(shape) is not tuple:
        raise Exception("Shape expects tuple (M, N).")
    if len(shape) != 2:
        raise Exception("Shape expects tuple (M, N).")
    if level is not None and level < 0:
        raise ValueError("Decomposition level must be >= 0.")
    if level is not None and level == 0:
        return eye(shape[0] * shape[1], n=shape[0] * shape[1], k=0)

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

        M, N = shape
        MN = shape[0] * shape[1]

        # Compute length of the output (number of coefficients)
        tmp = min(M, N)
        ncoeffs = 0
        for i in range(min(
                pywt.dwt_max_level(M, W),
                pywt.dwt_max_level(N, W)) if level is None else level):
            # Number of H, V and D coefficients
            tmp = pywt.dwt_coeff_len(tmp, W, mode=mode)
            ncoeffs += 3 * tmp ** 2
        # Number of approximation coefficients
        ncoeffs += tmp ** 2

        # Compute length of the output (number of coefficients)
        tmpM, tmpN = M, N
        ncoeffs = 0
        for i in range(min(
                pywt.dwt_max_level(M, W),
                pywt.dwt_max_level(N, W)) if level is None else level):
            # Number of H, V and D coefficients
            tmpM = pywt.dwt_coeff_len(tmpM, W, mode=mode)
            tmpN = pywt.dwt_coeff_len(tmpN, W, mode=mode)
            ncoeffs += 3 * tmpM * tmpN
        # Number of approximation coefficients
        ncoeffs += tmpM * tmpN

        def _matmat(x):
            # Decomposition (return 1d array from coefficients)
            # cAn matrix will be flattened as-well-as the cHs, cVs and cDs.
            # x is always 2d
            batch_size = x.shape[1]

            y = np.empty((ncoeffs, batch_size), dtype=x.dtype)

            # Loop over a batch of flattened 2d array
            for b in range(batch_size):
                tmp = pywt.wavedec2(x[:, b].reshape(M, N),
                                    wavelet=wavelet.name,
                                    level=level, mode=mode, axes=(-2, -1))
                # Store coefficients in 1d array
                tmp_ravel = []
                for i in range(len(tmp)):
                    if type(tmp[i]) is tuple:
                        for j in range(len(tmp[i])):
                            tmp_ravel = np.append(tmp_ravel,
                                                  tmp[i][j].flatten())
                    else:
                        tmp_ravel = np.append(tmp_ravel, tmp[i].flatten())
                y[:, b] = np.array(tmp_ravel)
            return y

        def _rmatmat(x):
            # Reconstruction
            # x is always 2d
            batch_size = x.shape[1]

            y = np.empty((MN, batch_size), dtype=x.dtype)

            # Loop over a batch of flattened 2d array
            for b in range(batch_size):
                # Compute length of the output of _matmat(x)
                tmpM, tmpN = M, N
                coeffs = []
                offset = x.shape[0]
                for i in range(min(
                        pywt.dwt_max_level(M, W),
                        pywt.dwt_max_level(N, W)) if level is None else level):
                    # Number of H, V and D coefficients
                    tmpM = pywt.dwt_coeff_len(tmpM, W, mode=mode)
                    tmpN = pywt.dwt_coeff_len(tmpN, W, mode=mode)
                    # Reconstruct the output of pywt.wavedec2
                    D = x[(offset - tmpM * tmpN):offset, b].reshape(tmpM, tmpN)
                    V = x[
                        (offset - 2 * tmpM * tmpN):
                        (offset - tmpM * tmpN), b].reshape(tmpM, tmpN)
                    H = x[
                        (offset - 3 * tmpM * tmpN):
                        (offset - 2 * tmpM * tmpN), b].reshape(tmpM, tmpN)
                    coeffs.insert(0, (H, V, D))
                    offset = offset - 3 * tmpM * tmpN
                # Approximation coefficients
                A = x[:offset, b].reshape(tmpM, tmpN)
                coeffs.insert(0, A)

                y[:, b] = pywt.waverec2(coeffs,
                                        wavelet=rwavelet,
                                        mode=mode,
                                        axes=(-2, -1))[:M, :N].ravel()
            return y

        return LazyLinOp(
            shape=(ncoeffs, MN),
            matmat=lambda x: _matmat(x),
            rmatmat=lambda x: _rmatmat(x)
        )
    elif backend == 'lazylinop':

        # Image has been flattened (with img.flatten(order='C'))
        # The result is vec = (row1, row2, ..., rowR) with size = M * N
        M, N = shape[0], shape[1]

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
        if W <= 1:
            raise Exception("Length of the wavelet must be > 1.")

        if W > M or W > N:
            # Nothing to decompose, return identity matrix
            return eye(M * N, n=M * N, k=0)

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

        # Stop decomposition when the signal becomes
        # shorter than the filter length
        K = min(int(np.log2(M / (W - 1))), int(np.log2(N / (W - 1))))
        if level is not None and level > K:
            raise Exception("Decomposition level is greater than" +
                            " the maximum decomposition level.")
        D = K if level is None else min(K, level)
        if D == 0:
            # Nothing to decompose, return identity matrix
            return eye(M * N, n=M * N, k=0)

        # Slice index as a function of decomposition level
        offset = np.empty(D + 1, dtype=np.int_)
        offset[0] = 0
        for i in range(D):
            cx = ((M if i == 0 else cx) + W - 1) // 2
            offset[i + 1] = offset[i] + 4 * cx
        start = np.empty(np.sum(np.diff(offset)), dtype=np.int_)
        end = np.empty(np.sum(np.diff(offset)), dtype=np.int_)

        # Loop over the decomposition level
        for i in range(D):
            # Low and high-pass filters + decimation
            # Boundary conditions
            npd = W - 2
            tmp_x = M if i == 0 else cx
            tmp_y = N if i == 0 else cy
            Fx = tmp_x + 2 * npd
            Fy = tmp_y + 2 * npd
            if mode == 'zero':
                Fx += Fx % 2
                Fy += Fy % 2
                Ax = eye(Fx, n=tmp_x, k=-npd)
                Ay = eye(Fy, n=tmp_y, k=-npd)
            else:
                mx = Fx % 2
                bx = npd
                ax = npd + mx
                Fx += mx
                my = Fy % 2
                by = npd
                ay = npd + my
                Fy += my
                Ax = bc(tmp_x, n=0, bn=bx, an=ax, boundary=mode)
                Ay = bc(tmp_y, n=0, bn=by, an=ay, boundary=mode)
            # First work on the row ...
            # ... and then work on the column (use Kronecker product vec trick)
            offset_x = int(
                (npd % 2) == 0) if mode == 'zero' else int((bx % 2) == 0)
            offset_y = int(
                (npd % 2) == 0) if mode == 'zero' else int((by % 2) == 0)
            if boffset:
                offset_x, offset_y = 0, 0
            if Fx > 1024 and Fy > 1024:
                # Convolution, down-sampling and vertical stack
                VM = ds_mconv(Fx, lfilter, hfilter,
                              mode='same', offset=offset_x) @ Ax
                VN = ds_mconv(Fy, lfilter, hfilter,
                              mode='same', offset=offset_y) @ Ay
            else:
                # Convolution
                method = 'scipy encapsulation'
                GM = convolve(Fx, lfilter, mode='same', method=method)
                GN = convolve(Fy, lfilter, mode='same', method=method)
                HM = convolve(Fx, hfilter, mode='same', method=method)
                HN = convolve(Fy, hfilter, mode='same', method=method)
                # Down-sampling
                DM = slices(GM.shape[0], [], [], 1, 2, (offset_x, None))
                DN = slices(GN.shape[0], [], [], 1, 2, (offset_y, None))
                # Vertical stack
                VM = vstack((DM @ GM, DM @ HM)) @ Ax
                VN = vstack((DN @ GN, DN @ HN)) @ Ay
            # Because we work on the rows and then on the columns,
            # we can write a Kronecker product that will be applied
            # to the flatten image
            KGH = kron(VM, VN)
            # Extract four sub-images (use slices operator)
            # ---------------------
            # | LL (cA) | LH (cH) |
            # ---------------------
            # | HL (cV) | HH (cD) |
            # ---------------------
            cx = ((M if i == 0 else cx) + W - 1) // 2
            cy = ((N if i == 0 else cy) + W - 1) // 2
            # Slices to extract detail, vertical and horizontal
            # coefficients and fill the following list of
            # coefficients [cAn, cHn, cVn, cDn, ..., cH1, cV1, cD1]
            Hx, Hy = Fx // 2, Fy // 2
            offset_x = (Hx - cx) // 2
            offset_y = (Hy - cy) // 2
            if boffset:
                offset_x += 1
                offset_y += 1
            # Slices to extract sub-image LL
            np.add(
                np.arange(offset_x, offset_x + cx) * Fy,
                offset_y,
                out=start[offset[i]:(offset[i] + cx)]
            )
            np.add(
                start[offset[i]:(offset[i] + cx)],
                cy - 1,
                out=end[offset[i]:(offset[i] + cx)]
            )
            # Slices to extract sub-image LH
            np.add(
                start[offset[i]:(offset[i] + cx)],
                Hy,
                out=start[(offset[i] + 2 * cx):(offset[i] + 3 * cx)]
            )
            np.add(
                end[offset[i]:(offset[i] + cx)],
                Hy,
                out=end[(offset[i] + 2 * cx):(offset[i] + 3 * cx)]
            )
            # Slices to extract sub-image HL
            np.add(
                np.arange(Hx + offset_x, Hx + offset_x + cx, 1) * Fy,
                offset_y,
                out=start[(offset[i] + cx):(offset[i] + 2 * cx)]
            )
            np.add(
                start[(offset[i] + cx):(offset[i] + 2 * cx)],
                cy - 1,
                out=end[(offset[i] + cx):(offset[i] + 2 * cx)]
            )
            # Slices to extract sub-image HH
            np.add(
                start[(offset[i] + cx):(offset[i] + 2 * cx)],
                Hy,
                out=start[(offset[i] + 3 * cx):(offset[i] + 4 * cx)]
            )
            np.add(
                end[(offset[i] + cx):(offset[i] + 2 * cx)],
                Hy,
                out=end[(offset[i] + 3 * cx):(offset[i] + 4 * cx)]
            )
            # Vertical stack where LL is the first lazy linear operator
            # ----
            # |LL|
            # ----
            # |LH|
            # ----
            # |HL|
            # ----
            # |HH|
            # ----
            V = slices(KGH.shape[0],
                       start[offset[i]:(offset[i] + 4 * cx)],
                       end[offset[i]:(offset[i] + 4 * cx)])
            if i == 0:
                # First level of decomposition
                A = V @ KGH
            else:
                # Apply low and high-pass filters + decimation only to LL
                # Because of lazy linear operator V, LL always comes first
                A = block_diag(*[V @ KGH,
                                 eye(A.shape[0] - KGH.shape[1],
                                     n=A.shape[0] - KGH.shape[1], k=0)]) @ A
        return A
    else:
        raise ValueError("backend must be either 'pywavelets' or 'lazylinop'.")


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

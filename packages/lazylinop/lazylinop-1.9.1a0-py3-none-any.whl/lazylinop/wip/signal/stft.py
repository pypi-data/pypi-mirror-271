import numpy as np
import scipy as sp
from lazylinop import LazyLinOp
from lazylinop.basicops import diag, eye, kron
from lazylinop.wip.signal import slices
import sys
sys.setrecursionlimit(100000)


def stft(N: int, fs: float = 1.0, window: str = 'hann',
         nperseg: int = 256, noverlap: int = None,
         boundary: str = 'zeros', padded: bool = True,
         scaling: str = 'spectrum'):
    """Constructs a Short-Time-Fourier-Transform lazy linear operator.
    :octicon:`info;1em;sd-text-success` The function uses basic
    operators to build STFT operator.

    Args:
        N: int
            Length of the input array.
        fs: int, optional
            Sampling frequency (1 is default).
        window: str, optional
            Window name to use to avoid discontinuity if the
            segment was looped indefinitly ('hann' is default).
            See `scipy.signal.get_window <https://docs.scipy.org/
            doc/scipy/reference/generated/scipy.signal.get_window.html>`_
            for a list of available windows.
        nperseg: int, optional
            Number of samples in a frame (256 is default).
        noverlap: int, optional
            Number of samples to overlap between two consecutive
            segments (None is default correspoding to nperseg // 2).
        boundary: str or None, optional
            How to extend signal at both ends ('zeros' is default).
            Only option is 'zeros', others are WiP.
        padded: bool, optional
            Zero-pad the signal such that new length fits exactly
            into an integer number of window segments (True is default).
        scaling: str, optional
            Scaling mode ('spectrum' is default) follows scipy.signal.stft
            function, other possible choice is 'psd'.

    Returns:
        LazyLinOp

    Raises:
        ValueError
            window argument expects 'hann'.
        ValueError
            scaling argument expects 'spectrum' or 'psd'.
        ValueError
            noverlap expects value less than nperseg.
        ValueError
            nperseg expects value greater than 0.

    Examples:

    .. seealso::
        `scipy.signal.stft <https://docs.scipy.org/doc/scipy/
        reference/generated/scipy.signal.stft.html>`_,
        `scipy.signal.get_window <https://docs.scipy.org/doc/
        scipy/reference/generated/scipy.signal.get_window.html>`_.
    """
    if nperseg < 1:
        raise ValueError("nperseg expects value greater than 0.")

    if noverlap is None:
        noverlap = nperseg // 2
    if noverlap >= nperseg:
        raise ValueError("noverlap expects value less than nperseg.")

    warray = sp.signal.windows.get_window(window, nperseg, fftbins=True)

    # number of zeros to add to both ends (boundary)
    bzeros = 1

    # number of samples between two frames > 0
    nhop = nperseg - noverlap
    # number of segments
    nseg = N // nperseg if nhop == 0 else 1 + (N - nperseg) // nhop

    def _rfft(N: int):
        nfreq = N // 2 + 1 if (N % 2) == 0 else (N + 1) // 2
        F = LazyLinOp(
            shape=(N, N),
            matvec=lambda x: sp.fft.fft(x),
            rmatvec=lambda x: np.multiply(N, sp.fft.ifft(x)),
            dtype='complex128'
        )
        return F[:nfreq, :]

    # keep only positive-frequency terms
    nfreq = nperseg // 2 + 1 if (nperseg % 2) == 0 else (nperseg + 1) // 2
    # lazy linear operator for the FFT
    F = _rfft(nperseg)
    # lazy linear operator "scatter and gather the windows"
    G = slices(N, [], [], nperseg, nhop)
    # lazy linear operator "one operation" per segment
    E = eye(nseg, n=nseg, k=0, dtype='complex128')
    # lazy linear operator to apply window
    W = kron(E, diag(warray, k=0))
    # lazy linear operator to apply STFT per segment
    S = kron(E, F)
    # lazy linear operator to scale the output
    if scaling == 'psd':
        sqscale = 1.0 / (fs * np.sum(np.square(warray)))
    elif scaling == 'spectrum':
        sqscale = 1.0 / np.sum(warray) ** 2
    else:
        raise ValueError("scaling argument expects 'spectrum' or 'psd'.")
    D = diag(np.full(nseg * nfreq, np.sqrt(sqscale)), k=0)
    # return complete operator
    return D @ S @ W @ G


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

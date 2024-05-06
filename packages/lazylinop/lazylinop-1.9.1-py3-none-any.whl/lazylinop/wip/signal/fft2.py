import numpy as np
import scipy as sp
from lazylinop import aslazylinop, kron, LazyLinOp
from lazylinop.wip.signal import is_power_of_two
import sys
import warnings
from warnings import warn

sys.setrecursionlimit(100000)
warnings.simplefilter(action='always')


def fft2(shape, backend='scipy', **kwargs):
    """Returns a LazyLinOp for the 2D DFT of size n.

    Args:
        shape: tuple
            The signal shape to apply the fft2 to.
        backend: str, optional
            'scipy' (default) or 'pyfaust' for the underlying computation
            of the 2D DFT. pyfaust allows power of two only.
        kwargs:
            Any key-value pair arguments to pass to the
            scipy or pyfaust dft backend.

    Returns:
        LazyLinOp

    Raises:
        ValueError
            backend must be either scipy or pyfaust.

    Example:
        >>> from lazylinop.wip.signal import fft2
        >>> import numpy as np
        >>> F_scipy = fft2((32, 32), norm='ortho')
        >>> F_pyfaust = fft2((32, 32), backend='pyfaust')
        >>> x = np.random.rand(32, 32)
        >>> np.allclose(F_scipy @ x.ravel(), F_pyfaust @ x.ravel())
        True
        >>> y = F_scipy @ x.ravel()
        >>> np.allclose(F_scipy.H @ y, x.ravel())
        True
        >>> np.allclose(F_pyfaust.H @ y, x.ravel())
        True

    .. seealso::
        `SciPy fft2 <https://docs.scipy.org/doc/scipy/reference/
        generated/scipy.fft.fft2.html>`_,
        `pyfaust dft <https://faustgrp.gitlabpages.inria.fr/faust/
        last-doc/html/namespacepyfaust.html#a2695e35f9c270e8cb6b28b9b40458600>`_
    """
    s = shape[0] * shape[1]
    if backend == 'scipy':
        from scipy.fft import fft2, ifft2
        return LazyLinOp(
            shape=(s, s),
            matvec=lambda x: fft2(x.reshape(shape), **kwargs).ravel(),
            rmatvec=lambda x: ifft2(x.reshape(shape), **kwargs).ravel()
        )
    elif backend == 'pyfaust':
        from pyfaust import dft
        # pyfaust allows power of two only
        if not is_power_of_two(shape[0]) or not is_power_of_two(shape[1]):
            # fallback to scipy backend
            warn("pyfaust allows power of two only," +
                 " fallback to scipy backend.")
            kwargs.pop('normed', None)
            from scipy.fft import fft2, ifft2
            return LazyLinOp(
                shape=(s, s),
                matvec=lambda x: fft2(x.reshape(shape), **kwargs).ravel(),
                rmatvec=lambda x: ifft2(x.reshape(shape), **kwargs).ravel()
            )
        else:
            return kron(dft(shape[0], **kwargs), dft(shape[1], **kwargs).T)
    else:
        raise ValueError('backend must be either scipy or pyfaust.')

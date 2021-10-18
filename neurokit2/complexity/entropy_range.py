import numpy as np
import pandas as pd

from .utils import _get_r, _phi, _phi_divide


def entropy_range(signal, dimension=3, delay=1, r="default", method="mSampEn", **kwargs):
    """Range Entropy (RangeEn)

    Introduced by `Omidvarnia et al. (2018) <https://www.mdpi.com/1099-4300/20/12/962/htm>`_.
    Both ApEn and SampEn compute the logarithmic likelihood that runs of patterns that are close
    remain close on the next incremental comparisons, of which this closeness is estimated by the
    Chebyshev distance. Range Entropy adapts the quantification of this closeness by using instead a
    normlized distance, resulting in modified forms of ApEn and SampEn, 'mApEn' and 'mSampEn' respectively.

    Parameters
    ----------
    signal : Union[list, np.array, pd.Series]
        The signal (i.e., a time series) in the form of a vector of values.
    delay : int
        Time delay (often denoted 'Tau', sometimes referred to as 'lag'). In practice, it is common
        to have a fixed time lag (corresponding for instance to the sampling rate; Gautama, 2003), or
        to find a suitable value using some algorithmic heuristics (see ``delay_optimal()``).
    dimension : int
        Embedding dimension (often denoted 'm' or 'd', sometimes referred to as 'order'). Typically
        2 or 3. It corresponds to the number of compared runs of lagged data. If 2, the embedding returns
        an array with two columns corresponding to the original signal and its delayed (by Tau) version.
    r : float
        Tolerance (similarity threshold). It corresponds to the filtering level - max absolute difference
        between segments. If 'default', will be set to 0.2 times the standard deviation of the signal
        (for dimension = 2).
    method : str
        The entropy measure to use, 'mSampEn' (sample entropy, default) or 'mApEn' (approximate entropy).
    **kwargs
        Other arguments.

    See Also
    --------
    entropy_approximate, entropy_sample

    Returns
    -------
    RangeEn : float
        Range Entropy
    info : dict
        A dictionary containing additional information regarding the parameters used.

    References
    ----------
    - Omidvarnia, A., Mesbah, M., Pedersen, M., & Jackson, G. (2018). Range entropy: A bridge between
    signal complexity and self-similarity. Entropy, 20(12), 962.


    Examples
    ----------
    >>> import neurokit2 as nk
    >>>
    >>> signal = nk.signal_simulate(duration=2, sampling_rate=100, frequency=[5, 6], noise=0.5)
    >>>
    >>> # Range Entropy
    >>> rangeen, info = nk.entropy_range(signal, dimension=3, delay=1, method="mSampEn")
    >>> rangeen  #doctest: +SKIP

    """
    # Sanity checks
    if isinstance(signal, (np.ndarray, pd.DataFrame)) and signal.ndim > 1:
        raise ValueError(
            "Multidimensional inputs (e.g., matrices or multichannel data) are not supported yet."
        )

    # Prepare parameters
    info = {"Dimension": dimension, "Delay": delay, "Method": method}

    info["Tolerance"] = _get_r(signal, r=r, dimension=dimension)
    out = _entropy_range(
        signal,
        r=info["Tolerance"],
        delay=delay,
        dimension=dimension,
        method=method,
        **kwargs
    )

    return out, info


def _entropy_range(signal, r, delay=1, dimension=2, method="mSampEn", **kwargs):

    if method == "mApEn":
        phi = _phi(signal, delay=delay, dimension=dimension, r=r, approximate=True,
                   distance="range", **kwargs)
        rangeen = np.abs(np.subtract(phi[0], phi[1]))

    elif method == "mSampEn":
        phi = _phi(signal, delay=delay, dimension=dimension, r=r, approximate=False,
                   distance="range", **kwargs)
        rangeen = _phi_divide(phi)

    return rangeen

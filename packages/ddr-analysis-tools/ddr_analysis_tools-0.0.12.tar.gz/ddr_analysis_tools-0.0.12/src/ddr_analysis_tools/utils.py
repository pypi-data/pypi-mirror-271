
import numpy as np

import scipy




def filter_data_butter(data: np.ndarray, N: int = 20, Wn: list | float = 1, btype: str = 'highpass', sampling_frequency: int = 1000) -> np.ndarray:
    """filteres the data using butterworth filter from scipy

    Parameters
    ----------
    data : np.ndarray
        input time series data
    N : int, optional
        order of the filter. More details can be found in scipy.signal.butter, by default 20
    Wn : list|float, optional
        cutoff freq. If btype = 'bandpass' or 'bandstop' then Wn should have 2 values in list or array type, by default 1
    btype : str, optional
        {‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}, by default 'highpass'
    fs : int, optional
        sampling frequency, by default 1000

    Returns
    -------
    array_like
        filtered data
    """
    sos = scipy.signal.butter(
        N, Wn=Wn, btype=btype, analog=False, fs=sampling_frequency, output='sos')
    return scipy.signal.sosfilt(sos, data)
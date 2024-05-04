

import scipy
import numpy as np
import matplotlib.pyplot as plt


from .utils import *



class PSD_welch:

    def __init__(self, data: np.ndarray, sampling_rate: int = None, total_time: float = None, **kwargs) -> None:
        """calculates PSD using welch's method.

        Mean of data is calculated and subtracted from the data. If mean is already subtracted then, calculating mean will result in zero and no changes in the data.

        Parameters
        ----------
        data : 1-D or single column numpy-array 
            data for which PSD is to be performed.
        sampling_rate : int, optional
            Sampling rate at which the data is acquired. Either of sampling_rate of total_time needs to be given. The other is calculated from the given value, by default None
        total_time : float, optional
            Total time duration for which the data was acquired. Either of sampling_rate of total_time needs to be given. The other is calculated from the given value, by default None
        **kwargs :
            keyword arguments related to scipy.signal.welch method. Look documentation for further help.
        """

        self.data = data
        self.n_samples = data.shape[0]
        self.data_mean = self.data.mean()
        self.data = self.data - self.data_mean

        if sampling_rate is not None:
            self.sampling_rate = sampling_rate
            self.total_time = self.n_samples / self.sampling_rate
        elif total_time is not None:
            self.total_time = total_time
            self.sampling_rate = self.n_samples / self.total_time

        self.welch_PSD_params = kwargs
        self.omega, self.data_PSD = scipy.signal.welch(
            x=self.data, fs=self.sampling_rate, **kwargs)

    def plot_PSD(self, xlabel: str = 'HZ', ylabel: str = 'Amplitude', ax: plt.Axes = None, label: str = None, scale: str = 'loglog', **kwargs) -> plt.Axes:
        if ax is None:
            ax = plt.gca()

        xdata, ydata = self.omega, self.data_PSD
        if scale == "loglog":
            ax.loglog(xdata, ydata, label=label, **kwargs)
        else:
            ax.plot(xdata, ydata, label=label, **kwargs)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        return ax

    def filtered_PSD(self, N: int = 20, Wn: list | float = 1, btype: str = 'highpass') -> tuple[np.ndarray, np.ndarray]:
        """_summary_

        Parameters
        ----------
        N : int, optional
        order of the filter. More details can be found in scipy.signal.butter, by default 20
        Wn : list|float, optional
            cutoff freq. If btype = 'bandpass' or 'bandstop' then Wn should have 2 values in list or array type, by default 1
        btype : str, optional
            {'lowpass', 'highpass', 'bandpass', 'bandstop'}, by default 'highpass'

        Returns
        -------
        tuple[np.ndarray,np.ndarray]
            freq and PSD as returned from scipy.signal.welch
        """

        data1 = filter_data_butter(data=self.data, N=N, Wn=Wn,
                            btype=btype, sampling_frequency=self.sampling_rate)
        return scipy.signal.welch(x=data1, fs=self.sampling_rate, **self.welch_PSD_params)

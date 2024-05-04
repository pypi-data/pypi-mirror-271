import numpy as np
import matplotlib.pyplot as plt


class fft_analysis:
    """
    Performs fft on the given data. fft is performed using numpy algorithm.
    This class is used to easily get the X-axis and y-axis for the fft plots.
    """

    def __init__(self, data, sampling_rate=None, total_time=None):
        """

        Parameters
        ----------
        data : 1-D or single column numpy-array
            data for which fft is to be performed.
        sampling_rate : float, optional
            Sampling rate at which the data is acquired. Either of sampling_rate of total_time needs to be given.
            The other is calculated from the given value.
            The default is None.
        total_time : float, optional
            Total time duration for which the data was acquired. Either of sampling_rate of total_time needs to be given.
            The other is calculated from the given value.
            The default is None.

        Returns
        -------
        fft_analysis class

        """

        self.data = data
        self.n_samples = data.shape[0]
        self.data_mean = self.data.mean()

        if sampling_rate is not None:
            self.sampling_rate = sampling_rate
            self.total_time = self.n_samples / self.sampling_rate
        elif total_time is not None:
            self.total_time = total_time
            self.sampling_rate = self.n_samples / self.total_time

        self.data_fft = np.fft.fft(self.data - self.data_mean)
        self.omega = np.fft.fftfreq(n=self.n_samples, d=1 / self.sampling_rate)

    @property
    def plotting_data(self) -> tuple[np.ndarray, np.ndarray]:
        return self.omega[: self.n_samples // 2], np.abs(
            self.data_fft[: self.n_samples // 2]
        )

    @property
    def peak_frequency(self) -> float:
        return freq[self.peak_freqidx]

    @property
    def peak_freqidx(self) -> int:
        freq, amp = self.plotting_data
        return amp.argmax()

    @property
    def half_data(self) -> tuple[np.ndarray, np.ndarray]:
        """returns the data cropped till half length. i.e. it returns only positive values of the frequency and respective complex fft values."""
        return self.omega[: self.n_samples // 2], self.data_fft[: self.n_samples // 2]

    def phase_data(self, threshold: float = 10**-7) -> tuple[np.ndarray, np.ndarray]:
        """Returns the frequency and corresponding phase angle in degrees.

        Parameters
        ----------
        threshold : float, optional
            values smaller than threshold in absolute sence, will be made 0.0 for both real and imag part, by default 10**-7

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            frequency and phase cropped till half
        """

        omega, ydata = self.half_data

        yreal = ydata.real
        f1 = np.abs(yreal) < threshold
        yreal[f1] = 0.0

        yimag = ydata.imag
        f1 = np.abs(yimag) < threshold
        yimag[f1] = 0.0

        return omega, np.arctan2(yimag, yreal) * 180 / np.pi

    def plot_fft(
        self,
        xlabel: str = "HZ",
        ylabel: str = "Amplitude",
        ax: plt.Axes = None,
        label: str = None,
        scale: str = "loglog",
        **kwargs
    ) -> plt.Axes:
        if ax is None:
            ax = plt.gca()

        xdata, ydata = self.plotting_data
        if scale == "loglog":
            ax.loglog(xdata, ydata, label=label, **kwargs)
        else:
            ax.plot(xdata, ydata, label=label, **kwargs)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid()

        return ax

    def plot_phase(
        self,
        xlabel: str = "HZ",
        ylabel: str = "Angle $^\circ$",
        ax: plt.Axes = None,
        label: str = None,
        threshold: float = 10**-7,
        **kwargs
    ) -> plt.Axes:
        if ax is None:
            ax = plt.gca()

        xdata, ydata = self.phase_data(threshold=threshold)
        ax.plot(xdata, ydata, label=label, **kwargs)

        # ax.set_xscale('log')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(visible=True)

        return ax

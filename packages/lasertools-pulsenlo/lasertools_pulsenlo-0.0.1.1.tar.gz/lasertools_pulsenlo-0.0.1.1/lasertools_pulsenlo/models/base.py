"""Define an NLO model template"""
import scipy as sp
import numpy as np
from lasertools_rffthelper import Axes


class _NLOBase:
    """Base class for a pulse NLO model template"""

    def __init__(self):
        self.bandpass_sos = None

    def define_bandpass(
        self,
        axes: Axes,
        bandpass_limit_lower: float,
        bandpass_limit_upper: float,
    ):
        """Defined a bandpass filter

        Keyword arguments:
        - axes -- Object defining signal and frequency axes
        - bandpass_limit_lower -- Lower edge of filter (Hz)
        - bandpass_limit_upper -- Upper edge of filter (Hz)"""

        self.bandpass_sos = sp.signal.butter(
            1,
            [
                bandpass_limit_lower,
                bandpass_limit_upper,
            ],
            "bandpass",
            fs=1 / axes.axes_parameters.signal_step,
            output="sos",
        )

    def apply_bandpass(self, waveform: np.ndarray):
        """Returns filtered waveform

        Keyword arguments:
        - waveform -- waveform to be filtered"""

        return sp.signal.sosfilt(self.bandpass_sos, waveform, axis=0)

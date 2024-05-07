"""Define an amplitude model"""
import sys
import numpy as np
from .base import _NLOBase
from lasertools_pulse import Pulse


class SHGFast(_NLOBase):
    """An arbitrary index of refraction defined by an equation"""

    def check_id(self, id_string):
        """Check if model name matches this pulse class"""

        return id_string == "SHG fast"

    def apply_process(
        self,
        waveform: np.ndarray,
    ):
        """Apply SHG to a waveform

        Keyword arguments:
        - waveform -- Waveform to be modified"""

        return waveform**2

    def apply_process_pulse(self, pulse: Pulse):
        """Apply SHG to a pulse object

        Keyword arguments:
        - pulse -- Pulse object to be modified"""

        if self.bandpass_sos is None:
            spectrum_intensity = pulse.spectrum()[0] ** 2
            spectrum_intensity /= np.max(spectrum_intensity)

            tenth_points = np.where(
                np.diff(np.sign(spectrum_intensity - 0.0001))
            )[0]

            try:
                self.define_bandpass(
                    pulse.axes,
                    2 * pulse.axes.frequency_axis[tenth_points[0]],
                    2 * pulse.axes.frequency_axis[tenth_points[-1]],
                )
            except ValueError:
                sys.exit("Frequency axis too narrow for the SHG fast process.")

        waveform_output = self.apply_process(pulse.waveform())
        pulse.define_waveform(self.apply_bandpass(waveform_output))

        return pulse

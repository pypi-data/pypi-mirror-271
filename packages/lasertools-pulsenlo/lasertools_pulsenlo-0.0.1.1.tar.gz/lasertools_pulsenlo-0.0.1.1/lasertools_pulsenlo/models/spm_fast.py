"""Define an amplitude model"""

import sys
import numpy as np
import lasertools_rffthelper as rfft
from .base import _NLOBase
from lasertools_pulse import Pulse


class SPMFast(_NLOBase):
    """An arbitrary index of refraction defined by an equation"""

    def check_id(self, id_string):
        """Check if model name matches this pulse class"""

        return id_string == "SPM fast"

    def apply_process(
        self,
        waveform: np.ndarray,
        spm_factor: float,
    ):
        """Apply SPM to a waveform

        Keyword arguments:
        - waveform -- Waveform to be modified
        - spm_factor -- B integral of nonlinear phase (rad)"""

        envelope, _, _, envelope_complex = rfft.envelope_frequency(waveform)

        return np.real(
            envelope_complex
            * np.exp(-1j * spm_factor / np.max(envelope**2) * envelope**2)
        )

    def apply_process_pulse(self, pulse: Pulse, spm_factor: float):
        """Apply SHG to a pulse object

        Keyword arguments:
        - pulse -- Pulse object to be modified
        - b_integral -- B integral of nonlinear phase (rad)"""

        waveform_output = self.apply_process(pulse.waveform(), spm_factor)
        pulse.define_waveform(waveform_output)

        return pulse

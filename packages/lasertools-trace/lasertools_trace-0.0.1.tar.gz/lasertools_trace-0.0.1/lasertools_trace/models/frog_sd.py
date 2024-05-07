"""A trace model for a dispersion scan"""
import numpy as np
import lasertools_pulsenlo
import lasertools_rffthelper as rfft
from lasertools_pulse import Pulse
from .base import _TraceBase


class TraceFROGSD(_TraceBase):
    """A material dispersion scan trace"""

    def check_id(self):
        """Check if model name matches this pulse class"""

        return self.model_information.model_name == "FROG-SD"

    def initialize(self):
        """Initialize the model"""
        self.define_computations()

    def define_computations(self):
        """Define masks in frequency and time"""

        # Calculate the phase map to shift the pulse at each delay
        delay_list = self.model_information.model_arguments["delay_list"]
        phase_map = rfft.calculate_phase_shift(delay_list, self.axes)
        self.computations.mask_phase = np.exp(-1j * phase_map)

        # Calculate the time-domain mask to prevent pulse wrapping
        self.computations.mask_time = rfft.calculate_amplitude_mask(
            delay_list, self.axes
        )

        # Define a bandpass filter for the SFG signal
        self.computations.model_nlo = lasertools_pulsenlo.find_model("SHG fast")
        self.computations.model_nlo.define_bandpass(
            self.axes,
            self.model_information.frequency_range_trace[0],
            self.model_information.frequency_range_trace[1],
        )

    def time(self, pulse: Pulse):
        """Returns the trace in the time domain

        Keyword arguments:
        - pulse -- Reference pulse of trace"""

        # Create 2d array of fundamental spectrum with mask for delay
        delayed_complex_spectrum = (
            self.computations.mask_phase * pulse.spectrum_complex[..., None]
        )

        # Obtain 2d array of delayed pulse without wrapping
        delayed_field = rfft.signal_from_complex_spectrum(
            delayed_complex_spectrum, self.axes
        )
        delayed_field_masked = self.computations.mask_time * delayed_field

        # Find analytical signals
        amplitude, _, phase, _ = rfft.envelope_frequency(pulse.waveform())
        amplitude_delayed, _, phase_delayed, _ = rfft.envelope_frequency(
            delayed_field_masked
        )

        # Calculate the SD field
        sd_field = (
            (amplitude_delayed**2)
            * amplitude[..., None]
            * np.cos(2 * phase_delayed - phase[..., None])
        )

        # Filter the SD frequency pulse
        sd_field_filtered = self.computations.model_nlo.apply_bandpass(
            sd_field
        )
        return sd_field_filtered

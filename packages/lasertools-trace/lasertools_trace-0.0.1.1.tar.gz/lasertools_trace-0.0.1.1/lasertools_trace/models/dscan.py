"""A trace model for a dispersion scan"""
import numpy as np
import lasertools_pulsedispersion
import lasertools_pulsenlo
import lasertools_rffthelper as rfft
from lasertools_pulse import Pulse
from .base import _TraceBase


class TraceDSCAN(_TraceBase):
    """A material dispersion scan trace"""

    def check_id(self):
        """Check if model name matches this pulse class"""

        return self.model_information.model_name == "DSCAN"

    def initialize(self):
        """Initialize the model"""
        self.define_computations()

    def define_computations(self):
        """Define masks in frequency and time"""

        # Initialize the phase map
        phase_map = np.zeros_like(
            np.outer(
                self.axes.frequency_axis,
                self.parameter_information.parameter_axis_dimensionless,
            ),
        )

        # Calculate the phase for each element in the dispersion list
        dispersion_list = self.model_information.model_arguments[
            "dispersion_list"
        ]
        for k, dispersion_elements in enumerate(dispersion_list):
            for dispersion_element in dispersion_elements:
                (
                    element_model,
                    element_model_parameters,
                ) = lasertools_pulsedispersion.find_model(dispersion_element["name"])
                phase = element_model.define_phase(
                    element_model_parameters,
                    self.axes.frequency_axis,
                    **dispersion_element["args"]
                )
                phase_map[:, k] += phase

        # Set the phase at offset value to zero
        phase_map_offset = np.zeros_like(self.axes.frequency_axis)
        for k, _ in enumerate(self.axes.frequency_axis):
            phase_map_offset[k] = np.interp(
                self.parameter_information.parameter_axis_offset_dimensionless,
                self.parameter_information.parameter_axis_dimensionless,
                phase_map[k, :],
            )
        phase_map -= phase_map_offset[..., None]

        # Define the phase mask
        self.computations.mask_phase = np.exp(-1j * phase_map)

        # Define the NLO model
        self.computations.model_nlo = lasertools_pulsenlo.find_model(
            self.model_information.model_arguments["nlo_process"]
        )
        self.computations.model_nlo.define_bandpass(
            self.axes,
            self.model_information.frequency_range_trace[0],
            self.model_information.frequency_range_trace[1],
        )

    def time(self, pulse: Pulse):
        """Returns the trace in the time domain

        Keyword arguments:
        - pulse -- Reference pulse of trace"""

        # Create 2d array of fundamental spectrum with mask for dispersion
        dispersed_complex_spectrum = (
            self.computations.mask_phase * pulse.spectrum_complex[..., None]
        )

        # Find the time domain signal
        dispersed_field = rfft.signal_from_complex_spectrum(
            dispersed_complex_spectrum, self.axes
        )

        # Calculate and filter the NLO signal
        dispersed_field_nlo = self.computations.model_nlo.apply_process(
            dispersed_field
        )
        dispersed_field_nlo = self.computations.model_nlo.apply_bandpass(
            dispersed_field_nlo
        )
        return dispersed_field_nlo

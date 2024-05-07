"""Define an trace model template"""
import dataclasses
import numpy as np
import lasertools_pulsenlo as nlo
import lasertools_rffthelper as rfft


@dataclasses.dataclass
class ParameterScales:
    """Class to store trace model parameter scales

    Keyword arguments:
    - parameter_label_unitless -- Name of parameter scanned in trace
    - parameter_unit -- Unit of parameter
    - parameter_factor -- Scale of units relative to SI"""

    parameter_label_unitless: str = "Parameter"
    parameter_unit: str = "arb. u."
    parameter_factor: float = 1

    def parameter_label(self) -> str:
        """Returns the label for the model parameters with units"""

        return self.parameter_label_unitless + " (" + self.parameter_unit + ")"


@dataclasses.dataclass
class FourierScales:
    """Class to store trace model time and frequency scales

    Keyword arguments:
    - frequency_unit -- Unit of frequency
    - frequency_factor -- Scale factor of frequency unit relative to Hertz
    - time_unit -- Unit of time
    - time_factor -- Scale of time unit relative to seconds
    - wavelength_unit -- Unit of wavelength
    - wavelength_factor -- Scale of wavelength unit relative to meters"""

    frequency_unit: str = "PHz"
    frequency_factor: float = 1e-15

    time_unit: str = "fs"
    time_factor: float = 1e15

    wavelength_unit: str = "nm"
    wavelength_factor: float = 1e9


@dataclasses.dataclass
class Labels:
    """Class to store all labels associated with a trace model

    Keyword arguments:
    - fourier_scales -- Object describing the model time and frequency scales
    - parameter_scales -- Object describing the model parameter scales"""

    fourier_scales: FourierScales
    parameter_scales: ParameterScales


@dataclasses.dataclass
class Computations:
    """Class to store masks and models used in trace computation

    Keyword arguments:
    - mask_time -- Mask(s) to apply in the time domain
    - mask_amplitude -- Mask(s) to apply to the spectrum amplitude
    - mask_phase -- Mask(s) to apply to the spectral phase
    - model_nlo -- Object representing model of NLO process"""

    mask_time: np.ndarray = None
    mask_amplitude: np.ndarray = None
    mask_phase: np.ndarray = None
    model_nlo: object = None


@dataclasses.dataclass
class ModelInformation:
    """Class to store trace parameters

    Keyword arguments:
    - model_name -- Name of trace model
    - model_arguments -- Keyword arguments used to initialize the trace model
    - frequency_range_fundamental -- Frequency edges of fundamental spectrum
    - frequency_range_trace -- Frequency edges of trace spectrum"""

    model_name: str
    model_arguments: {}
    frequency_range_fundamental: list[float]
    frequency_range_trace: list[float]

    index_range_fundamental = None
    index_range_trace = None

    def find_frequency_indices(self, axes: rfft.Axes):
        """Find indices at edge of frequency ranges

        Keyword arguments:
        - axes -- Object describing the Fourier axes"""

        self.index_range_fundamental = [
            np.argmin(
                np.abs(
                    axes.frequency_axis - self.frequency_range_fundamental[0]
                )
            ),
            np.argmin(
                np.abs(
                    axes.frequency_axis - self.frequency_range_fundamental[1]
                )
            ),
        ]
        self.index_range_trace = [
            np.argmin(
                np.abs(axes.frequency_axis - self.frequency_range_trace[0])
            ),
            np.argmin(
                np.abs(axes.frequency_axis - self.frequency_range_trace[1])
            ),
        ]


class ParameterInformation:
    """Class to calculate and store computational parameter axis information"""

    def __init__(
        self,
        parameter_axis_samples: int,
        parameter_axis_offset_dimensionless: float = 0,
        parameter_axis_dimensional_factor: float = 1,
    ):
        """Initialize parameter information

        Keyword arguments:
        - parameter_axis_samples -- Number of points in parameter axis
        - parameter_axis_offset_dimensionless -- Normalized parameter offset
        - parameter_axis_dimensional_factor -- Scale of parameter axis units"""

        self.parameter_axis_samples = parameter_axis_samples
        self.parameter_axis_dimensionless = np.arange(
            self.parameter_axis_samples
        )
        self.parameter_axis_offset_dimensionless = (
            parameter_axis_offset_dimensionless
        )
        self.parameter_axis_dimensional_factor = (
            parameter_axis_dimensional_factor
        )

    def raw_axis(self):
        """Returns dimensional parameter axis without offset"""

        return (
            self.parameter_axis_dimensionless
            * self.parameter_axis_dimensional_factor
        )

    def axis(self):
        """Returns dimensional parameter axis with offset"""

        return self.raw_axis() - self.offset()

    def offset(self):
        """Returns the dimensional parameter offset"""

        return (
            self.parameter_axis_offset_dimensionless
            * self.parameter_axis_dimensional_factor
        )


class _TraceBase:
    """Base class for a trace template"""

    def __init__(
        self,
        axes: rfft.Axes,
        labels: Labels,
        parameter_information: ParameterInformation,
        model_information: ModelInformation,
    ):
        self.axes = axes
        self.computations = Computations()
        self.labels = labels
        self.parameter_information = parameter_information
        model_information.find_frequency_indices(self.axes)
        self.model_information = model_information

    def spectrum_complex(self, trace_time):
        """Return the spectral domain trace

        Keyword arguments:
        - trace_time -- Time domain trace"""

        return rfft.complex_spectrum_from_signal(trace_time, self.axes)

    def update_spectrum_complex(self, trace_spectrum_complex):
        """Returns the time domain trace

        Keyword arguments:
        - trace_spectrum_complex -- Spectral domain trace (complex)"""

        return rfft.signal_from_complex_spectrum(
            trace_spectrum_complex, self.axes
        )

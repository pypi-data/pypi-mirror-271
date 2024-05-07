"""Process a trace"""

import sys
import dataclasses
import numpy as np
from lasertools_traceprocess import utilities


@dataclasses.dataclass
class BackgroundSettings:
    """Class to store background processing settings

    Keyword arguments:
    - background_pixels (Optional) -- Pixels at corners to use for subtraction
    - background_fraction (Optional) -- Signal level below which to set at zero
    """

    background_pixels: int = None
    background_fraction: float = None
    background_edges: int = None


@dataclasses.dataclass
class ProcessingSettings:
    """Class to store trace processing settings

    Keyword arguments:
    - background_pixels (Optional) -- Object storing background settings
    - blurring_sigma (Optional) -- Standard deviations of Gaussian blur
    - frequency_axis (Optional) -- Computational frequency axis (Hz)
    - frequency_axis_limits (Optional) -- Frequency boundaries of data (Hz)
    - parameter_axis (Optional) -- Computational parameter axis
    - normalize (Optional) -- Boolean setting for applying normalization"""

    background_settings: BackgroundSettings = BackgroundSettings()
    blurring_sigma: float = None
    frequency_axis: np.ndarray = None
    frequency_axis_limits: list[float] = None
    parameter_axis: np.ndarray = None
    normalizer: utilities.normalize.Normalizer = None


@dataclasses.dataclass
class TraceData:
    """Class to store signal and frequency axis parameters

    Keyword arguments:
    - trace -- Measured trace
    - frequency_axis (Optional) -- Measurement frequency axis (Hz)
    - wavelength_axis (Optional) -- Measurement wavelength axis (m)
    - parameter_axis (Optional) -- Measurement parameter axis"""

    trace: np.ndarray
    frequency_axis: np.ndarray = None
    wavelength_axis: np.ndarray = None
    parameter_axis: np.ndarray = None


def _process_interpolation(
    trace: TraceData, settings: ProcessingSettings, trace_processed=np.ndarray
):
    """Returns data interpolated to computational grid

    Keyword arguments:
    - trace -- Object representing measured trace
    - settings -- Object representing processing settings
    - trace_processed -- Processed trace to interpolate"""

    # Interpolate data to computation grid
    interpolate_frequency = False
    if (trace.wavelength_axis is not None) and (
        trace.frequency_axis is not None
    ):
        sys.exit("Only wavelength or frequency axis should be provided")
    elif trace.wavelength_axis is not None:
        interpolate_frequency = True
        trace.frequency_axis = np.flip(299792458 / trace.wavelength_axis)
        trace_processed = np.flip(trace_processed, axis=0)
        if settings.frequency_axis is None:
            sys.exit("Computational frequency axis must be provided")

    if (settings.frequency_axis is not None) and (
        trace.frequency_axis is not None
    ):
        interpolate_frequency = True

    interpolate_parameter = False
    if trace.parameter_axis is not None:
        if settings.parameter_axis is not None:
            interpolate_parameter = True
        elif interpolate_frequency:
            settings.parameter_axis = trace.parameter_axis
    elif interpolate_frequency:
        trace.parameter_axis = np.arange(len(trace_processed[0, :]))
        settings.parameter_axis = np.arange(len(trace_processed[0, :]))

    if interpolate_parameter & (not interpolate_frequency):
        settings.frequency_axis = trace.frequency_axis

    if interpolate_parameter or interpolate_frequency:
        trace_processed_interpolated = utilities.interpolate.interpolate2d(
            trace.parameter_axis,
            trace.frequency_axis,
            trace_processed,
            settings.parameter_axis,
            np.abs(settings.frequency_axis),
        )

        if settings.frequency_axis_limits is not None:
            frequency_axis_limit_index_lower = (
                np.abs(
                    settings.frequency_axis - settings.frequency_axis_limits[0]
                )
            ).argmin()
            frequency_axis_limit_index_upper = (
                np.abs(
                    settings.frequency_axis - settings.frequency_axis_limits[1]
                )
            ).argmin()
            trace_processed_interpolated[
                :frequency_axis_limit_index_lower, :
            ] = 0
            trace_processed_interpolated[
                frequency_axis_limit_index_upper:, :
            ] = 0
    else:
        settings.frequency_axis = trace.frequency_axis
        settings.parameter_axis = trace.parameter_axis
        trace_processed_interpolated = trace_processed

    return trace, settings, trace_processed_interpolated


def process(trace: TraceData, settings: ProcessingSettings):
    """Function to process raw traces

    Keyword arguments:
    - trace -- Object representing measured trace
    - settings -- Object representing processing settings"""

    if trace.frequency_axis is not None:
        if len(trace.frequency_axis) != len(trace.trace[:, 0]):
            sys.exit("First dimension must be frequency axis")

    if trace.wavelength_axis is not None:
        if len(trace.wavelength_axis) != len(trace.trace[:, 0]):
            sys.exit("First dimension must be wavelength axis")

    trace_processed = trace.trace

    # Subtract background based on average of corner values
    if settings.background_settings.background_pixels is not None:
        trace_processed = utilities.background.corners2d(
            trace_processed, settings.background_settings.background_pixels
        )

    # Subtract background based on average of edge values
    if settings.background_settings.background_edges is not None:
        trace_processed = utilities.background.extrema(
            trace_processed, settings.background_settings.background_edges
        )

    # Set all data below threshold to zero
    if settings.background_settings.background_fraction is not None:
        trace_processed = utilities.threshold.fraction(
            trace_processed, settings.background_settings.background_fraction
        )

    # Blur data using a Gaussian filter
    if settings.blurring_sigma is not None:
        trace_processed = utilities.smooth.gaussianblur(
            trace_processed, settings.blurring_sigma
        )

    # Interpolate the data to the computational grid
    trace, settings, trace_processed_interpolated = _process_interpolation(
        trace, settings, trace_processed
    )

    # Find the average parameter weighted by the signal
    if (settings.parameter_axis is not None) & (
        settings.frequency_axis is not None
    ):
        (
            weighted_average_parameter,
            weighted_average_frequency,
        ) = utilities.maxima.weighted2d(
            settings.parameter_axis,
            settings.frequency_axis,
            trace_processed_interpolated,
        )
    else:
        weighted_average_frequency = None
        weighted_average_parameter = None

    # Normalize data
    if settings.normalizer:
        trace_processed_interpolated /= settings.normalizer.norm(
            trace_processed_interpolated
        )

    return (
        settings.frequency_axis,
        settings.parameter_axis,
        trace_processed_interpolated,
        weighted_average_frequency,
        weighted_average_parameter,
    )

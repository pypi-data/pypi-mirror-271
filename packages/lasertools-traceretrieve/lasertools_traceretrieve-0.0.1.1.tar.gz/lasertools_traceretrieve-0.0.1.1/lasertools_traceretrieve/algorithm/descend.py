"""A brute force gradient descent for phase retrieval"""

import copy
import dataclasses
import numpy as np
import numba as nb
from lasertools_pulse import Pulse
from lasertools_traceprocess import Normalizer
from lasertools_trace.models.base import _TraceBase


@nb.njit(parallel=False)
def variance_nb(am, ddof=0):
    """Calculate the variance of an array

    Keyword arguments:
    - am -- Array
    - ddof (Optional) -- Degrees of freedom"""

    a = am.flatten()
    n = len(a)
    s = a.sum()
    m = s / (n - ddof)
    v = 0
    for i in nb.prange(n):
        v += abs(a[i] - m) ** 2
    return v / (n - ddof)


@nb.njit(parallel=False)
def residual_nb(am, bm):
    """Calculate the residual sum of squares of two arrays

    Keyword arguments:
    - am -- Array 1
    - bm -- Array 2"""

    a = (am - bm) ** 2
    b = a.flatten()
    s = b.sum()
    return s


def determination(am, bm):
    """Calculate R^2 between two arrays

    Keyword arguments:
    - am -- Test array
    - bm -- Reference array"""

    return 1 - residual_nb(am, bm) / (variance_nb(bm) * np.size(bm))


def residual(
    trace_time_unconstrained: np.ndarray,
    trace_object: _TraceBase,
    pulse_object: Pulse,
    normalizer_time: Normalizer,
):
    """Calculate the residual sum of squares of the time domain traces

    Keyword arguments:
    - trace_time_unconstrained -- Numerical time domain trace for reference
    - trace_object -- Object representing a trace model
    - pulse_object -- Object representing a test pulse"""

    trace_time_constrained = normalizer_time.normalize(
        trace_object.time(pulse_object)
    )
    return residual_nb(trace_time_constrained, trace_time_unconstrained)


def gradient_calculation(
    trace_time_unconstrained: np.ndarray,
    trace_object: _TraceBase,
    pulse_object: Pulse,
    test_increment: float,
    normalizer_time: Normalizer,
):
    """Calculate the gradient for a pulse using the time domain trace

    Keyword arguments:
    - trace_time_unconstrained -- Numerical time domain trace for reference
    - trace_object -- Object representing a trace model
    - pulse_object -- Object representing a test pulse
    - test_increment -- Test increment for calculating gradient"""

    # Calculate reference residual sum of squares
    residual_reference = residual(
        trace_time_unconstrained, trace_object, pulse_object, normalizer_time
    )
    variance_reference = variance_nb(trace_time_unconstrained) * np.size(
        trace_time_unconstrained
    )

    # Create matrix of real numbers from complex vector for optimization
    input_variables = np.column_stack(
        (
            pulse_object.spectrum_complex.real,
            pulse_object.spectrum_complex.imag,
        )
    )

    # Store indices to optimize over
    optimization_indices = [
        (idx1, idx2)
        for idx1 in range(
            trace_object.model_information.index_range_fundamental[0],
            trace_object.model_information.index_range_fundamental[1] + 1,
            1,
        )
        for idx2 in [0, 1]
    ]

    # Copy input pulse instance
    pulse_object_test = copy.deepcopy(pulse_object)

    # Initialize residual array
    residuals = residual_reference * np.ones_like(input_variables)

    # Iterate over every point within spectral range for real and imaginary
    for indices in optimization_indices:
        # Copy test pulse variables
        test_variables = input_variables.copy()

        # Increment test pulse variables
        test_variables[indices[0], indices[1]] += test_increment

        # Reassemble test pulse spectra
        test_spectrum_complex = (
            test_variables[:, 0] + 1j * test_variables[:, 1]
        )

        # Update test pulse
        pulse_object_test.define_spectrum_complex(test_spectrum_complex)

        # Check test pulse
        residuals[indices[0], indices[1]] = residual(
            trace_time_unconstrained,
            trace_object,
            pulse_object_test,
            normalizer_time,
        )

    # Find rate of change of residual sum of squares
    r2_rate = (residual_reference - residuals) / (
        variance_reference * test_increment
    )

    # Return rate as a complex vector
    return r2_rate[:, 0] + 1j * r2_rate[:, 1]


@dataclasses.dataclass
class SettingsDescent:
    """Settings used for optimization

    Keyword arguments:
    - learning_rate_factor -- Maximum fraction of R^2 gap to increment
    - acceptable_loss -- Fraction of spectral R^2 that can be lost per step
    - steps -- Number of gradient descent steps
    - increment_relative -- Fractional increment for gradient calculation"""

    learning_rate_factor: float = 0.2
    acceptable_loss: float = 0.01
    steps: int = 1
    increment_relative: int = 1e-4
    normalizer: Normalizer = None
    normalizer_time: Normalizer = None


@dataclasses.dataclass
class DataDescent:
    """Data used and updated

    Keyword arguments:
    - trace_time_unconstrained -- Array of unconstrained time domain trace
    - trace_intensity_data -- Array of measured trace intensities
    - trace_object -- Object representing a measurement process
    - pulse_object -- Object representing a test pulse
    - r2_time_descent -- List of time domain R^2 during the descent
    - r2_spectrum_descent -- List of spectrum R^2 during the descent"""

    trace_time_unconstrained: np.ndarray
    trace_intensity_data: np.ndarray
    trace_object: _TraceBase
    pulse_object: Pulse
    r2_time_descent: list[float]
    r2_spectrum_descent: list[float]


def descend(
    spectrum_intensity_data: np.ndarray,
    trace_object: _TraceBase,
    pulse_object: Pulse,
    settings: SettingsDescent,
    normalizer: Normalizer,
):
    """Perform gradient descent

    Keyword arguments:
    - spectrum_intensity_data -- Array of measured intensities
    - trace_object -- Object representing a measurement process
    - pulse_object -- Object representing a test pulse
    - settings -- Object containing the gradient descent settings"""

    normalizer_time = normalizer

    # Calculate and normalize constrained time domain trace
    trace_time_constrained = normalizer_time.normalize(
        trace_object.time(pulse_object)
    )

    # Calculate and normalize contrained spectral domain trace
    trace_spectrum_constrained = normalizer.normalize(
        np.abs(trace_object.spectrum_complex(trace_time_constrained)) ** 2
    )

    # Calculate and normalize time domain trace based on measured intensities
    trace_time_unconstrained = normalizer_time.normalize(
        trace_object.update_spectrum_complex(
            np.sqrt(spectrum_intensity_data)
            * np.exp(
                1j
                * np.angle(
                    trace_object.spectrum_complex(trace_time_constrained)
                )
            )
        )
    )

    # Calculate determinations in time and spectrum before descent
    r2_time_descent = [
        determination(trace_time_constrained, trace_time_unconstrained)
    ]

    # Calculate determination in spectrum trace before descent
    r2_spectrum_descent = [
        determination(trace_spectrum_constrained, spectrum_intensity_data)
    ]

    data_descent = DataDescent(
        trace_time_unconstrained=trace_time_unconstrained,
        trace_intensity_data=spectrum_intensity_data,
        trace_object=trace_object,
        pulse_object=pulse_object,
        r2_spectrum_descent=r2_spectrum_descent,
        r2_time_descent=r2_time_descent,
    )

    settings.normalizer = normalizer
    settings.normalizer_time = normalizer_time

    return step(settings, data_descent)


def step(
    settings: SettingsDescent,
    data: DataDescent,
):
    """Make the gradient descent steps

    Keyword arguments:
    - settings -- Object containing the gradient descent settings
    - data -- Object containing the data used and updated"""

    for _ in range(settings.steps):

        # Store unmodified spectrum
        spectrum_complex_initial = data.pulse_object.spectrum_complex

        # Set spectrum increment based on amplitude
        increment = settings.increment_relative * np.min(
            [
                np.mean(data.pulse_object.spectrum_complex.real),
                np.mean(data.pulse_object.spectrum_complex.imag),
            ]
        )

        # Calculate the gradient
        r2_rate = gradient_calculation(
            data.trace_time_unconstrained,
            data.trace_object,
            data.pulse_object,
            increment,
            settings.normalizer_time,
        )
        r2_rate /= np.linalg.norm(r2_rate)

        # Test a small learning rate
        data.pulse_object.define_spectrum_complex(
            spectrum_complex_initial + settings.increment_relative * r2_rate
        )

        # Calculate and normalize new time and frequency domain traces
        trace_time_constrained = settings.normalizer_time.normalize(
            data.trace_object.time(data.pulse_object)
        )
        trace_intensity_constrained = settings.normalizer.normalize(
            np.abs(data.trace_object.spectrum_complex(trace_time_constrained))
            ** 2
        )

        # Find new determination and rates
        r2_time_new = determination(
            trace_time_constrained, data.trace_time_unconstrained
        )
        r2_spectrum_new = determination(
            trace_intensity_constrained, data.trace_intensity_data
        )

        r2_time_rate = (
            r2_time_new - data.r2_time_descent[-1]
        ) / settings.increment_relative
        r2_spectrum_rate = (
            r2_spectrum_new - data.r2_spectrum_descent[-1]
        ) / settings.increment_relative

        # Define learning rates
        learning_rate_time = (
            (1 - data.r2_time_descent[-1])
            * settings.learning_rate_factor
            / (r2_time_rate)
        )
        learning_rate_spectrum = (
            (1 - data.r2_spectrum_descent[-1])
            * settings.learning_rate_factor
            / (r2_spectrum_rate)
        )
        learning_rate_spectrum = max(learning_rate_spectrum, 0)
        learning_rate = (learning_rate_time + learning_rate_spectrum) / 2

        # Initialize new determination
        r2_time_new = data.r2_time_descent[-1] - 1
        r2_spectrum_new = data.r2_spectrum_descent[-1] - 1

        improving = 0
        while improving < 0.95:
            # Update spectrum
            data.pulse_object.define_spectrum_complex(
                spectrum_complex_initial + (learning_rate * r2_rate)
            )

            # Calculate and normalize new time and frequency domain traces
            trace_time_constrained = settings.normalizer_time.normalize(
                data.trace_object.time(data.pulse_object)
            )
            trace_intensity_constrained = settings.normalizer.normalize(
                (
                    np.abs(
                        data.trace_object.spectrum_complex(
                            trace_time_constrained
                        )
                    )
                    ** 2
                )
            )

            # Find new determination and rates
            r2_time_new = determination(
                trace_time_constrained, data.trace_time_unconstrained
            )
            r2_spectrum_new = determination(
                trace_intensity_constrained, data.trace_intensity_data
            )

            improving = 0
            if r2_time_new > data.r2_time_descent[-1]:
                improving += 0.5
            else:
                learning_rate /= 10
                improving += 0.4
                print(
                    "Temporal R^2 decreased, learning rate reduced to: "
                    + str(learning_rate)
                )

            if (
                r2_spectrum_new
                > data.r2_spectrum_descent[-1]
                * (
                    1
                    - np.sign(data.r2_spectrum_descent[-1])
                    * settings.acceptable_loss
                )
            ) & (improving > 0.45):
                improving += 0.5
            elif improving > 0.45:
                learning_rate /= 10
                print(
                    "Spectral R^2 below threshold, learning rate reduced to: "
                    + str(learning_rate)
                )
            if learning_rate < 1e-20:
                improving = 2
                print("Minimum learning rate threshold reached")

        # Update spectrum
        data.pulse_object.define_spectrum_complex(
            data.pulse_object.spectrum_complex + learning_rate * r2_rate
        )

        # Store determinations
        data.r2_time_descent.append(r2_time_new)
        data.r2_spectrum_descent.append(r2_spectrum_new)

        return (
            data.pulse_object,
            data.r2_time_descent,
            data.r2_spectrum_descent,
            trace_intensity_constrained,
            improving > 1.95,
        )

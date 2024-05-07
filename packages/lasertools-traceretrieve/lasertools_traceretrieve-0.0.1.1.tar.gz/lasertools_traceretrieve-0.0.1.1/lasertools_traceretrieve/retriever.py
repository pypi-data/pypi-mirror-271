"""Retrieve pulse using the method of general projections"""

import time
import dataclasses
import copy
import numpy as np
from lasertools_pulse import Pulse
from lasertools_traceprocess import Normalizer
from lasertools_trace.models.base import _TraceBase
from lasertools_traceretrieve.algorithm.descend import SettingsDescent, descend
from lasertools_traceretrieve import resources


class Times:
    """Class to store, caculate, and report retrieval time durations"""

    def __init__(self):
        """Initialization"""

        self.start_global: float = time.time()
        self.start_iteration: float = None
        self.end_iteration: float = None
        self.end_global: float = None
        self.iteration_list: list[float] = []

    def iteration_start(self):
        """Store iteration start time"""
        self.start_iteration = time.time()

    def iteration_end(self):
        """Store iteration end time and duration"""
        self.end_iteration = time.time()
        self.iteration_list.append(self.end_iteration - self.start_iteration)

    def iteration_report(
        self,
        iteration_number: int,
        iteration_threshold: int,
        r2_time: float,
        r2_spectrum: float,
    ):
        """Output iteration report:

        Keyword arguments:
        - iteration_number -- Current iteration number
        - iteration_threshold -- Maximum iteration number
        - r2_time -- Current time-domain R^2
        - r2_spectrum -- Current spectral-domain R^2"""

        print(
            "Iteration "
            + str(iteration_number + 1)
            + " of "
            + str(iteration_threshold)
            + " took "
            + str(
                np.round(
                    1000 * (self.iteration_list[-1]),
                    1,
                )
            )
            + " milliseconds; R^2 time = "
            + str(np.round(r2_time, 5))
            + "; R^2 spectrum = "
            + str(np.round(r2_spectrum, 5))
        )

    def report(self):
        """Output final report"""

        self.end_global = time.time()
        print(
            "Total runtime was "
            + str(np.round((self.end_global - self.start_global) / 60, 1))
            + " minutes; Average iteration took "
            + str(
                np.round(
                    1000 * (np.mean(self.iteration_list)),
                    1,
                )
            )
            + " milliseconds"
        )


@dataclasses.dataclass
class SettingsThreshold:
    """Thresholds for stopping retrieval

    Keyword arguments:
    - iterations -- Maximum number of iterations
    - seconds -- Maximum number of seconds
    - r2 -- Minimum R^2
    - r2_change -- Minimum R^2 change"""

    iterations: int = 1000
    seconds: float = None
    r2: float = 1
    r2_change: float = 1e-6
    r2_last = [0, 0]
    threshold = False

    def check(
        self,
        iteration: int,
        time_object: Times,
        r2_time: float,
        r2_spectrum: float,
    ):
        """Check threshold criteria

        Keyword arguments:
        - iteration -- Current iteration number
        - time_object -- Object to store and report retrieval time durations
        - r2_time -- Current R^2 in time domain
        - r2_spectrum -- Current R%2 in frequency domain"""

        if iteration >= (self.iterations - 1):
            self.threshold = True
        if (r2_time > self.r2) & (r2_spectrum > self.r2):
            print("R^2 threshold reached")
            self.threshold = True
        if self.seconds is not None:
            if (
                time_object.end_iteration - time_object.start_global
            ) > self.seconds:
                print("Runtime threshold reached")
                self.threshold = True
        if ((r2_time - self.r2_last[0]) < self.r2_change) & (
            (r2_spectrum - self.r2_last[1]) < self.r2_change
        ):
            print("R^2 improvement threshold reached")
            self.threshold = True


@dataclasses.dataclass
class SettingsRetrieve:
    """Class to store retrieving parameters

    Keyword arguments:
    - descend -- Object containing gradient descent settings
    - thresholds (Optional) -- Object containing threshold settings
    - update_period (Optional) -- Number of iterations per figure update
    - output_directory (Optional) -- Path to directory for output
    - normalization (Optional) -- continuous (2d) or discontinuous (1d)"""

    descend: SettingsDescent = SettingsDescent()
    thresholds: SettingsThreshold = SettingsThreshold()
    update_period: int = 25
    output_directory: str = None
    normalizer: Normalizer = None


def retrieve(
    settings: SettingsRetrieve,
    trace_object: _TraceBase,
    pulse_object: Pulse,
    trace_intensity_measured: np.ndarray,
):
    """Run a phase retrieval

    Keyword arguments:
    - settings -- Object containing retrieval settings
    - trace_object -- Object representing a trace model
    - pulse_object -- Object representing a test pulse
    - trace_processed -- Array of processed measured trace
    - output_directory (Optional) -- Directory for retrieval output"""

    # Log start time
    time_object = Times()

    # Initialize normalizer
    if settings.normalizer is None:
        settings.normalizer = Normalizer(
            "continuous",
            trace_object.model_information.index_range_trace,
        )

    # Calculate trace for initial guess
    trace_intensity_guess = settings.normalizer.normalize(
        np.abs(
            trace_object.spectrum_complex(
                trace_object.time(copy.copy(pulse_object))
            )
        )
        ** 2
    )

    # Store measured trace
    trace_intensity_measured /= settings.normalizer.norm(
        trace_intensity_measured
    )

    # Initialize determinations array
    determinations = np.zeros([1, 3])

    # Initialize figure
    plot_objects = resources.create_plots(trace_object)
    plot_objects.determination.plot(determinations)
    plot_objects.pulse.plot(pulse_object)
    plot_objects.traces.plot(trace_intensity_measured, trace_intensity_guess)
    resources.draw_really()

    iteration = 0
    while not settings.thresholds.threshold:
        # Record start time of iteration
        time_object.iteration_start()

        # Apply constraints
        (
            pulse_object,
            r2_time_descent,
            r2_spectrum_descent,
            trace_intensity_guess,
            settings.thresholds.threshold,
        ) = descend(
            trace_intensity_measured,
            trace_object,
            pulse_object,
            settings.descend,
            settings.normalizer,
        )

        # Store determinations
        for k, _ in enumerate(r2_time_descent):
            iteration_partial = iteration + k * (
                1 / (settings.descend.steps + 1)
            )
            if iteration_partial == 0:
                determinations[0, 0] = iteration_partial
                determinations[0, 1] = r2_spectrum_descent[k]
                determinations[0, 2] = r2_time_descent[k]
                settings.thresholds.r2_last = [
                    r2_time_descent[k],
                    r2_spectrum_descent[k],
                ]
            elif iteration_partial > 0:
                determinations = np.vstack(
                    (
                        determinations,
                        [
                            iteration_partial,
                            r2_spectrum_descent[k],
                            r2_time_descent[k],
                        ],
                    )
                )

        # Record end time of iteration
        time_object.iteration_end()

        # Report duration of iteration
        time_object.iteration_report(
            iteration,
            settings.thresholds.iterations,
            r2_time_descent[-1],
            r2_spectrum_descent[-1],
        )

        # Check thresholds
        settings.thresholds.check(
            iteration,
            time_object,
            r2_time_descent[-1],
            r2_spectrum_descent[-1],
        )

        # Store current R^2 and increment iteration
        if not settings.thresholds.threshold:
            iteration += 1
            settings.thresholds.r2_last = [
                r2_time_descent[-1],
                r2_spectrum_descent[-1],
            ]

        # Update figure
        if (
            np.remainder(iteration + 1, settings.update_period) == 0
        ) or settings.thresholds.threshold:
            # Update figure
            plot_objects.determination.update(determinations)
            plot_objects.pulse.update(pulse_object)
            plot_objects.traces.update(trace_intensity_guess)
            resources.draw_really()

    time_object.report()

    if settings.output_directory is not None:
        pulse_object.recenter()
        pulse_object.export(settings.output_directory)
        plot_objects.fig.export(settings.output_directory)

    # Keep figure alive
    plot_objects.fig.hang()

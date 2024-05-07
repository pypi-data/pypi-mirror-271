"""A module for the live figure during retrievals"""

import os
import copy
import dataclasses
import numpy as np
from matplotlib import pyplot as plt
from lasertools_trace import _TraceBase
from lasertools_pulse import Pulse
from lasertools_traceretrieve.resources.colormap_jetwhite import create_colormap


@dataclasses.dataclass
class DataCoordinatesLabel:
    """Class to store plot axes labels"""

    label: str = ""
    units: str = ""

    def full(self):
        """Return label with units"""
        return self.label + " (" + self.units + ")"


class RetrievalFigureDataCoordinates:
    """Class to store plot axes"""

    def __init__(
        self,
        values: np.ndarray,
        offset: float = 0,
        factor: float = 1,
        label: DataCoordinatesLabel = DataCoordinatesLabel(),
    ):
        """Class to store frequency axis information"""
        self.values = values
        self.offset = offset
        self.factor = factor
        self.label = label

        self.range_indices = [0, (len(values) - 1)]
        self.range = [
            self.values[self.range_indices[0]],
            self.values[self.range_indices[1]],
        ]

    def values_unoffset(self):
        """Return axis in range"""

        return (
            self.values[self.range_indices[0] : self.range_indices[1]]
            * self.factor
        )

    def value_offset(self):
        """Return offset"""

        return self.offset * self.factor

    def values_offset(self):
        """Return axis in range with offset"""

        return self.values_unoffset() + self.value_offset()

    def define_range(self, axis_range: list[float]):
        """Define the range to plot by a start and stop value"""

        self.range_indices = [
            np.argmin(np.abs(np.min(axis_range) - self.values)),
            np.argmin(np.abs(np.max(axis_range) - self.values)),
        ]
        self.range = [
            self.values[self.range_indices[0]],
            self.values[self.range_indices[1]],
        ]
        return copy.deepcopy(self)


def draw_really():
    """A function to actually update the axes"""

    plt.draw()
    plt.pause(0.001)
    plt.pause(0.001)


@dataclasses.dataclass
class RetrievalFigureFormatValues:
    """Class to store figure layout values"""

    figure_pad: float = 5
    axis_position_left: float = 0.07
    axis_position_spacing_horizontal: float = 0.0625
    axis_width: float = 0.2175
    axis_position_bottom: float = 0.125
    axis_position_spacing_vertical: float = 0.12
    axis_height: float = 0.29


class RetrievalFigureWindow:
    """Live and final plot of retrieval"""

    def __init__(
        self,
        figure_size=(11, 8.5),
        figure_number=547,
        figure_format_values=None,
    ):
        self.figure_size = figure_size
        self.figure_number = figure_number
        self.figure_format_values = figure_format_values

        if not self.figure_format_values:
            self.figure_format_values = RetrievalFigureFormatValues()

        self.fig, self.fig_axs = self.make_axes()
        draw_really()

        input(
            "Position live figure window before continuing. Press enter/return to continue."
        )

    def make_axes(self):
        """Initialize and format figure and axes"""

        # Create figure and primary figure axes
        fig, _axs = plt.subplots(
            2, 3, num=self.figure_number, figsize=self.figure_size
        )
        fig.tight_layout(pad=self.figure_format_values.figure_pad)

        # Create twinned axes
        _axs_twin = _axs_cbar = []
        _axs_twin.append(_axs[0, 0].twiny())
        _axs_twin.append(_axs[1, 1].twinx())
        _axs_twin.append(_axs[1, 2].twinx())

        axs = []
        axs.append(_axs[0, 0])
        axs[0].set_position(
            [
                self.figure_format_values.axis_position_left,
                self.figure_format_values.axis_position_bottom
                + self.figure_format_values.axis_height
                + self.figure_format_values.axis_position_spacing_vertical,
                self.figure_format_values.axis_width,
                self.figure_format_values.axis_height,
            ]
        )
        _ax_position = axs[0].get_position()

        axs.append(_axs_twin[0])

        axs.append(_axs[0, 1])
        axs[2].set_position(
            [
                _ax_position.x0
                + _ax_position.width
                + self.figure_format_values.axis_position_spacing_horizontal,
                _ax_position.y0,
                _ax_position.width,
                _ax_position.height,
            ]
        )
        _ax_position = axs[2].get_position()

        _ax_cbar = plt.axes(
            [
                _ax_position.x0 + _ax_position.width + 0.005,
                _ax_position.y0,
                0.01,
                _ax_position.height,
            ]
        )
        axs.append(_ax_cbar)

        axs.append(_axs[0, 2])
        axs[4].set_position(
            [
                _ax_position.x0
                + _ax_position.width
                + 2
                * self.figure_format_values.axis_position_spacing_horizontal,
                _ax_position.y0,
                _ax_position.width,
                _ax_position.height,
            ]
        )
        _ax_position = axs[4].get_position()

        _ax_cbar = plt.axes(
            [
                _ax_position.x0 + _ax_position.width + 0.005,
                _ax_position.y0,
                0.01,
                _ax_position.height,
            ]
        )
        axs.append(_ax_cbar)

        axs.append(_axs[1, 0])
        axs[6].set_position(
            [
                self.figure_format_values.axis_position_left,
                self.figure_format_values.axis_position_bottom,
                _ax_position.width,
                _ax_position.height,
            ]
        )
        _ax_position = axs[6].get_position()

        axs.append(_axs[1, 1])
        axs[7].set_position(
            [
                _ax_position.x0
                + _ax_position.width
                + self.figure_format_values.axis_position_spacing_horizontal,
                _ax_position.y0,
                _ax_position.width,
                _ax_position.height,
            ]
        )
        _ax_position = axs[7].get_position()

        axs.append(_axs_twin[1])

        axs.append(_axs[1, 2])
        axs[9].set_position(
            [
                _ax_position.x0
                + _ax_position.width
                + 2
                * self.figure_format_values.axis_position_spacing_horizontal,
                _ax_position.y0,
                _ax_position.width,
                _ax_position.height,
            ]
        )
        _ax_position = axs[9].get_position()

        axs.append(_axs_twin[2])

        return fig, axs

    def export(self, path, filename="retrieval"):
        """Save figure"""

        self.fig.savefig(os.path.join(path, filename + ".png"))

    def hang(self):
        """Keep window alive"""

        plt.show()


class RetrievalFigurePlotsTrace:
    """Trace color plots"""

    def __init__(
        self,
        fig,
        axs,
        coordinates_frequency,
        coordinates_parameter,
    ):
        self.coordinates_parameter = coordinates_parameter
        self.coordinates_frequency = coordinates_frequency
        self.fig = fig
        self.axs = axs
        self.handles = [None] * len(axs)
        self.trace_measured_max = 0
        self.data_trace_processed_trimmed = None

    def trim_trace(self, trace):
        """Trim trace to coordinate ranges"""

        return np.array(
            trace[
                self.coordinates_frequency.range_indices[
                    0
                ] : self.coordinates_frequency.range_indices[1],
                self.coordinates_parameter.range_indices[
                    0
                ] : self.coordinates_parameter.range_indices[1],
            ]
        )

    def plot(self, data_trace_processed, trace_simulated):
        """Method to plot the traces

        Keyword arguments:
        - data_trace_processed -- Measured trace
        - trace_simulated -- Reconstructed trace"""

        self.data_trace_processed_trimmed = self.trim_trace(
            data_trace_processed
        )

        self.trace_measured_max = np.max(self.data_trace_processed_trimmed)

        trace_simulated_trimmed = self.trim_trace(trace_simulated)
        trace_simulated_max = np.max(trace_simulated_trimmed)
        trace_overall_max = np.max(
            [trace_simulated_max, self.trace_measured_max]
        )

        trace_difference = (
            trace_simulated_trimmed - self.data_trace_processed_trimmed
        )
        trace_difference_max = np.max(np.abs(trace_difference))

        axis_parameter = self.coordinates_parameter.values_unoffset()
        axis_frequency = self.coordinates_frequency.values_offset()

        _ax = self.axs[0]
        _handle = _ax.pcolormesh(
            axis_parameter,
            axis_frequency,
            self.data_trace_processed_trimmed / trace_overall_max,
            cmap=create_colormap(),
            clim=(0, 1),
        )
        _ax.set_xlabel(self.coordinates_parameter.label.full())
        _ax.set_ylabel(self.coordinates_frequency.label.full())
        _ax.set_xlim(
            axis_parameter[0],
            axis_parameter[-1],
        )
        _ax.set_ylim(
            axis_frequency[0],
            axis_frequency[-1],
        )
        _ax.set_title("Measured Trace")
        self.handles[0] = _handle

        _ax = self.axs[1]
        _ax.tick_params(direction="in", pad=-22)
        _ax.set_xlim(
            axis_parameter[0],
            axis_parameter[-1],
        )
        _ax.set_xticks([self.coordinates_parameter.value_offset()])
        _ax.set_xticklabels(["Center"])

        _ax = self.axs[2]
        _handle = _ax.pcolormesh(
            axis_parameter,
            axis_frequency,
            trace_simulated_trimmed / trace_overall_max,
            cmap=create_colormap(),
            clim=(0, 1),
        )
        _ax.set_xlabel(self.coordinates_parameter.label.full())
        _ax.set_ylabel(self.coordinates_frequency.label.full())
        _ax.set_xlim(
            axis_parameter[0],
            axis_parameter[-1],
        )
        _ax.set_ylim(
            axis_frequency[0],
            axis_frequency[-1],
        )
        _ax.set_title("Retrieved Trace")
        self.handles[2] = _handle

        _ax = self.axs[3]
        _ax.cbar = self.fig.colorbar(
            self.handles[2],
            cax=_ax,
            orientation="vertical",
        )
        _ax.cbar.set_label("Intensity (arb. u.)")

        _ax = self.axs[4]
        _handle = _ax.pcolormesh(
            axis_parameter,
            axis_frequency,
            100 * trace_difference / self.trace_measured_max,
            cmap="bwr",
            clim=(
                -100 * trace_difference_max / self.trace_measured_max,
                100 * trace_difference_max / self.trace_measured_max,
            ),
        )
        _ax.set_xlabel(self.coordinates_parameter.label.full())
        _ax.set_ylabel(self.coordinates_frequency.label.full())
        _ax.set_xlim(
            axis_parameter[0],
            axis_parameter[-1],
        )
        _ax.set_ylim(
            axis_frequency[0],
            axis_frequency[-1],
        )
        _ax.set_title("Difference")
        self.handles[4] = _handle

        _ax = self.axs[5]
        _ax.cbar = self.fig.colorbar(
            self.handles[4],
            cax=_ax,
            orientation="vertical",
        )
        _ax.cbar.set_label("Residual (%)")

    def update(self, trace_simulated):
        """Method to update the trace plots

        Keyword arguments:
        - data_trace_processed -- Measured trace
        - trace_simulated -- Reconstructed trace"""

        trace_simulated_trimmed = self.trim_trace(trace_simulated)
        trace_simulated_max = np.max(trace_simulated_trimmed)
        trace_overall_max = np.max(
            [trace_simulated_max, self.trace_measured_max]
        )

        trace_difference = (
            trace_simulated_trimmed - self.data_trace_processed_trimmed
        )
        trace_difference_max = np.max(np.abs(trace_difference))

        self.handles[0].set_array(
            self.data_trace_processed_trimmed / trace_overall_max
        )
        self.handles[2].set_array(trace_simulated_trimmed / trace_overall_max)
        self.handles[4].set_array(
            100 * trace_difference / self.trace_measured_max
        )
        self.handles[4].set_clim(
            -100 * trace_difference_max / self.trace_measured_max,
            100 * trace_difference_max / self.trace_measured_max,
        )
        self.handles[5]


class RetrievalFigurePlotsPulse:
    """Line plots decribing pulse in frequency and time"""

    def __init__(
        self,
        fig,
        axs,
        coordinates_frequency,
        coordinates_time,
    ):
        self.coordinates_time = coordinates_time
        self.coordinates_frequency = coordinates_frequency
        self.fig = fig
        self.axs = axs
        self.handles = [None] * len(axs)

    def plot(self, pulse_raw: Pulse):
        """Method to plot the pulse

        Keyword arguments:
        - pulse -- Object representing a pulse"""

        pulse = copy.copy(pulse_raw)
        pulse.recenter()

        pulse_fwhm = np.round(
            pulse.fwhm(envelope_order=2) * self.coordinates_time.factor, 1
        )
        pulse_fwhm_ftl = np.round(
            pulse.fwhm_ftl(envelope_order=2) * self.coordinates_time.factor, 1
        )

        axis_time = self.coordinates_time.values_offset()
        axis_frequency = self.coordinates_frequency.values_offset()

        spectrum_intensity = pulse.spectrum()[0] ** 2
        spectrum_intensity /= np.max(spectrum_intensity)

        (
            envelope_intensity,
            frequency,
        ) = pulse.envelope(envelope_order=2)
        envelope_intensity /= np.max(envelope_intensity)

        _ax = self.axs[7]
        (_handle,) = _ax.plot(
            axis_frequency,
            spectrum_intensity[
                self.coordinates_frequency.range_indices[
                    0
                ] : self.coordinates_frequency.range_indices[1]
            ],
            "k",
        )
        _ax.set_xlabel(self.coordinates_frequency.label.full())
        _ax.set_ylabel("Intensity (arb. u.)")
        _ax.set_xlim(
            axis_frequency[0],
            axis_frequency[-1],
        )
        _ax.set_ylim(-0.05, 1.05)
        _ax.set_title(
            "Spectrum: "
            + str(pulse_fwhm_ftl)
            + " "
            + self.coordinates_time.label.units
            + " FTL"
        )
        self.handles[7] = _handle

        _ax = self.axs[8]
        (_handle,) = _ax.plot(
            axis_frequency,
            pulse.spectrum()[1][
                self.coordinates_frequency.range_indices[
                    0
                ] : self.coordinates_frequency.range_indices[1]
            ],
            "-b.",
            alpha=0.5,
        )
        _ax.set_xlim(
            axis_frequency[0],
            axis_frequency[-1],
        )
        _ax.set_ylabel("Phase (rad)")
        _ax.yaxis.label.set_color("blue")
        _ax.tick_params(axis="y", colors="blue")
        _ax.spines["right"].set_color("blue")
        _ax.set_ylim(-1.025 * np.pi, 1.025 * np.pi)
        _ax.yaxis.set_label_position("right")
        self.handles[8] = _handle

        _ax = self.axs[9]
        (_handle,) = _ax.plot(
            axis_time,
            envelope_intensity[
                self.coordinates_time.range_indices[
                    0
                ] : self.coordinates_time.range_indices[1]
            ],
            "k",
        )
        _ax.set_xlim(
            np.max([axis_time[0], -5 * pulse_fwhm]),
            np.min([axis_time[-1], 5 * pulse_fwhm]),
        )
        _ax.set_xlabel(self.coordinates_time.label.full())
        _ax.set_ylabel("Intensity (arb. u.)")
        _ax.set_ylim(-0.05, 1.05)
        _ax.set_title(
            "Waveform: "
            + str(pulse_fwhm)
            + " "
            + self.coordinates_time.label.units
        )
        self.handles[9] = _handle

        _ax = self.axs[10]
        (_handle,) = _ax.plot(
            axis_time,
            frequency[
                self.coordinates_time.range_indices[
                    0
                ] : self.coordinates_time.range_indices[1]
            ]
            * self.coordinates_frequency.factor,
            "-b",
            alpha=0.5,
        )
        _ax.set_ylabel(self.coordinates_frequency.label.full())
        _ax.yaxis.label.set_color("blue")
        _ax.tick_params(axis="y", colors="blue")
        _ax.spines["right"].set_color("blue")
        _ax.set_xlim(
            np.max([axis_time[0], -5 * pulse_fwhm]),
            np.min([axis_time[-1], 5 * pulse_fwhm]),
        )
        _ax.set_ylim(
            axis_frequency[0],
            axis_frequency[-1],
        )
        self.handles[10] = _handle

    def update(self, pulse_raw: Pulse):
        """Method to update the pulse plot

        Keyword arguments:
        - pulse -- Object representing a pulse"""

        pulse = copy.copy(pulse_raw)
        pulse.recenter()

        pulse_fwhm = np.round(
            pulse.fwhm(envelope_order=2) * self.coordinates_time.factor, 1
        )
        pulse_fwhm_ftl = np.round(
            pulse.fwhm_ftl(envelope_order=2) * self.coordinates_time.factor, 1
        )

        spectrum_intensity = pulse.spectrum()[0] ** 2
        spectrum_intensity /= np.max(spectrum_intensity)

        (
            envelope_intensity,
            frequency,
        ) = pulse.envelope(envelope_order=2)
        envelope_intensity /= np.max(envelope_intensity)

        self.handles[7].set_ydata(
            spectrum_intensity[
                self.coordinates_frequency.range_indices[
                    0
                ] : self.coordinates_frequency.range_indices[1]
            ]
        )
        self.axs[7].set_title(
            "Spectrum: "
            + str(pulse_fwhm_ftl)
            + " "
            + self.coordinates_time.label.units
            + " FTL"
        )
        self.handles[8].set_ydata(
            pulse.spectrum()[1][
                self.coordinates_frequency.range_indices[
                    0
                ] : self.coordinates_frequency.range_indices[1]
            ]
        )
        self.handles[9].set_ydata(
            envelope_intensity[
                self.coordinates_time.range_indices[
                    0
                ] : self.coordinates_time.range_indices[1]
            ]
        )
        self.axs[9].set_title(
            "Waveform: "
            + str(pulse_fwhm)
            + " "
            + self.coordinates_time.label.units
        )
        self.handles[10].set_ydata(
            frequency[
                self.coordinates_time.range_indices[
                    0
                ] : self.coordinates_time.range_indices[1]
            ]
            * self.coordinates_frequency.factor
        )
        self.axs[10].set_xlim(
            np.max(
                [self.coordinates_time.values_offset()[0], -5 * pulse_fwhm]
            ),
            np.min(
                [self.coordinates_time.values_offset()[-1], 5 * pulse_fwhm]
            ),
        )


class RetrievalFigurePlotDetermination:
    """Line plots decribing determination in frequency and time"""

    def __init__(
        self,
        fig,
        axs,
    ):
        self.fig = fig
        self.axs = axs
        self.handles = [None] * len(axs)

    def plot(self, determinations: np.ndarray):
        """Method to plot the r-squared values

        Keyword arguments:
        - determinations -- R^2 values"""

        _ax = self.axs[6]
        (_handle1,) = _ax.plot(
            determinations[:, 0],
            determinations[:, 1],
            "b",
        )
        (_handle2,) = _ax.plot(
            determinations[:, 0],
            determinations[:, 2],
            "r",
        )
        _ax.legend(
            [_handle1, _handle2],
            ["Frequency domain", "Time domain"],
            loc="lower right",
            frameon=False,
        )
        _ax.set_xlabel("Iteration")
        _ax.set_ylabel("R$^2$")
        _ax.set_title("Determination")
        if len(determinations[:, 0]) > 1:
            _ax.set_xlim(determinations[:, 0], determinations[:, -1])
        self.handles[6] = [_handle1, _handle2]

    def update(self, determinations: np.ndarray):
        """Method to update the determination plots

        Keyword arguments:
        - determinations -- R^2 values"""

        self.handles[6][0].set_xdata(determinations[:, 0])
        self.handles[6][0].set_ydata(determinations[:, 1])
        self.handles[6][1].set_xdata(determinations[:, 0])
        self.handles[6][1].set_ydata(determinations[:, 2])
        if len(determinations[:, 0]) > 1:
            self.axs[6].set_xlim(determinations[0, 0], determinations[-1, 0])
            ymin = np.min(determinations[:, 1:3])
            ymax = np.min([np.max(determinations[:, 1:3]), 1])
            if (ymin < 0) & (ymax > 0):
                ymin = 0
            self.axs[6].set_ylim(
                ymin - 0.04,
                ymax + 0.04,
            )


@dataclasses.dataclass
class PlotObjects:
    """Object to store all plot objects"""

    traces: RetrievalFigurePlotsTrace = None
    pulse: RetrievalFigurePlotsPulse = None
    determination: RetrievalFigurePlotDetermination = None
    fig: RetrievalFigureWindow = None
    format: RetrievalFigureFormatValues = None


def create_plots(trace_model=_TraceBase):
    """Function to generate axes and coordinates

    Keyword arguments:
    - trace_model -- Object representing a trace model"""

    plot_objects = PlotObjects()
    plot_objects.fig = RetrievalFigureWindow()

    param_coords = RetrievalFigureDataCoordinates(
        values=trace_model.parameter_information.raw_axis(),
        label=DataCoordinatesLabel(
            trace_model.labels.parameter_scales.parameter_label_unitless,
            trace_model.labels.parameter_scales.parameter_unit,
        ),
        factor=trace_model.labels.parameter_scales.parameter_factor,
        offset=trace_model.parameter_information.offset(),
    )
    freq_coords = RetrievalFigureDataCoordinates(
        values=trace_model.axes.frequency_axis,
        label=DataCoordinatesLabel(
            "Frequency", trace_model.labels.fourier_scales.frequency_unit
        ),
        factor=trace_model.labels.fourier_scales.frequency_factor,
    )
    freq_coords_trace = freq_coords.define_range(
        trace_model.model_information.frequency_range_trace
    )
    freq_coords_fund = freq_coords.define_range(
        trace_model.model_information.frequency_range_fundamental
    )

    time_coords = RetrievalFigureDataCoordinates(
        values=trace_model.axes.signal_axis,
        label=DataCoordinatesLabel(
            "Time", trace_model.labels.fourier_scales.time_unit
        ),
        factor=trace_model.labels.fourier_scales.time_factor,
        offset=-np.mean(trace_model.axes.signal_axis),
    )

    plot_objects.traces = RetrievalFigurePlotsTrace(
        plot_objects.fig.fig,
        plot_objects.fig.fig_axs,
        freq_coords_trace,
        param_coords,
    )
    plot_objects.pulse = RetrievalFigurePlotsPulse(
        plot_objects.fig.fig,
        plot_objects.fig.fig_axs,
        freq_coords_fund,
        time_coords,
    )
    plot_objects.determination = RetrievalFigurePlotDetermination(
        plot_objects.fig.fig, plot_objects.fig.fig_axs
    )

    return plot_objects

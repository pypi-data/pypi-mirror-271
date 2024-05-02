"""
-----------------------------------------------------------------------------------------
graph module
-----------------------------------------------------------------------------------------
Provides functionality to easily visualise signals. 
"""

from typing import Tuple, List, Any

import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.palettes import Colorblind
from bokeh.models import HoverTool


def plot_signal(
    n: np.ndarray,
    s: np.ndarray,
    is_discrete: bool = True,
    fig_size: Tuple[int, int] = (10, 5),
    fig_title: str = None,
    x_lim: Tuple[int, int] = None,
    x_tick: List[int] = None,
    x_tick_labels: List[Any] = None,
    x_ticks_steps: int = 5,
    x_label: str = None,
    y_lim: Tuple[int, int] = None,
    y_tick: List[int] = None,
    y_tick_labels: List[Any] = None,
    y_label: str = "Amplitude",
    grid_on: bool = True,
    save_figure: bool = False,
    save_name: str = "Figure.png",
    save_format: str = "png",
) -> None:
    """Visualize discrete (secuences) and continuous time signals.

    Args:
        n (np.ndarray): Independent variable (i.e. time vector).

        s (np.ndarray): Dependent variable (i.e. the signal).

        is_discrete (bool, optional): Whether the signal is discrete or continuous.
        Defaults to True.

        fig_size (Tuple[int, int], optional): Set up the size of the output figure (in
        inches).
        Defaults to (10, 5).

        fig_title (str, optional): Figure title.
        Defaults to None: no title.

        x_lim (Tuple[int, int], optional): Minimum and maximum value of the x-axis.
        Defaults to None: ruled by x_ticks_steps.

        x_tick (List[int], optional): Values where the y-axis ticks are.
        Defaults to None: MatPlotLib's default.

        x_tick_labels (List[Any], optional): Labels that are going to be displayed in the
        x-axis ticks.
        Defaults to None: MatPlotLib's default.

        x_ticks_steps (int, optional): Steps to show x-axis ticks.
        Defaults to 5.

        x_label (str, optional): Label for x-axis.
        Defaults to None: Ruled by is_sequence so "n (samples)" for discrete sequences
        and "t (seconds)" for continuous signals.

        y_lim (Tuple[int, int], optional): Minimum and maximum value of the y-axis.
        Defaults to None: ruled by y_ticks_steps.

        y_tick (List[int], optional): Values where the y-axis ticks are.
        Defaults to None: MatPlotLib's default.

        y_tick_labels (List[Any], optional):  Labels that are going to be displayed in the
        y-axis ticks.
        Defaults to None: MatPlotLib's default.

        y_label (str, optional): Label for y-axis.
        Defaults to "Amplitude".

        grid_on (bool, optional): Wheter to display the grid.
        Defaults to True.

        save_figure (bool, optional): Wheter to save the figure.
        Defaults to False.

        save_name (str, optional): Name of the file name when saveFigure = True.
        Defaults to "Figure.png".

        save_format (str, optional): Format for the file name when saveFigure = True.
        Defaults to "png".
    """

    ## FIGURE SETUP
    fig = plt.figure(figsize=fig_size)  # Create the figure
    ax = fig.gca()  # Get the axis object of the figure

    if is_discrete:  # Draw discrete signals
        try:
            # Legacy code, new version of MatPlotLib does not support the use_line_collection argument
            ax.stem(n, s, use_line_collection=True, basefmt="k-")
        except TypeError:
            ax.stem(n, s, basefmt="k-")
    else:
        ax.plot(n, s)  # line Plot

    ## WORK ON X-AXIS
    if x_tick is None:  # Set the x-axis ticks
        if is_discrete:
            x_tick = n[n % x_ticks_steps == 0]
            ax.set_xticks(x_tick)

            x_tick_labels = list(map(str, x_tick))
            ax.set_xticklabels(x_tick_labels)
    else:
        ax.set_xticks(x_tick)
        if not isinstance(x_tick_labels, type(None)):
            ax.set_xticklabels(x_tick_labels)

    if x_lim is None:
        if is_discrete:
            ax.set_xlim(
                left=min(n) - 1, right=max(n) + 1  # Setup the limits of the x-axis
            )
    else:
        ax.set_xlim(x_lim)

    if x_label is None:
        if is_discrete:
            ax.set_xlabel("n (samples)", fontsize="xx-large")  # Label for the x-axis
        else:
            ax.set_xlabel("t (seconds)", fontsize="xx-large")  # Label for the x-axis
    else:
        ax.set_xlabel(x_label, fontsize="xx-large")  # Label for the x-axis

    ## WORK ON Y-AXIS
    if y_tick is not None:  # MatPlotLib's default insted
        ax.set_yticks(y_tick)

    if y_tick_labels is not None:  # MatPlotLib's default insted
        ax.set_yticklabels(y_tick_labels)

    if y_lim is not None:
        ax.set_ylim(y_lim)

    ax.set_ylabel(y_label, fontsize="xx-large")  # Label for the y-axis

    ## GENERAL TICK PARAMETERS
    ax.tick_params(axis="both", labelsize="x-large")  # Increase size of tick labels

    ## WORK ON TITLE
    if fig_title is not None:  # Figure title if indicated
        ax.set_title(fig_title, fontsize="xx-large")

    ## GRIDS
    if grid_on:
        ax.grid(alpha=0.4)

    ## EXPORT OPTION
    if save_figure:  # Saves the figure
        fig.savefig(save_name, dpi=300, format=save_format, bbox_inches="tight")

    plt.show()  # Shows the figure


def iplot_signal(
    t: np.ndarray,
    x: np.ndarray,
    x_lim: tuple = None,
    y_lim: tuple = None,
    fig_title: str = "",
    xlabel: str = "Time (s)",
    ylabel: str = "Amplitude (a.u.)",
    legend: str = None,
    plot_width: int = 700,
    plot_height: int = 450,
    line_width: float = 1.5,
    to_notebook: bool = True,
) -> None:
    """Signal interactive plot.

    Args:
        t (np.ndarray): Independent variable (i.e. time vector).

        x (np.ndarray): Dependent variable (i.e. the signal).

        x_lim (tuple, optional): Horizontal axis span limitation.
        Defaults to None.

        y_lim (tuple, optional): Vertical axis span limitation.
        Defaults to None.

        fig_title (str, optional): Title of the figure.
        Defaults to "".

        xlabel (str, optional): Label for the horizontal axis.
        Defaults to "Time (s)".

        ylabel (str, optional): Label for the vertical axis.
        Defaults to "Amplitude (a.u.)".

        legend (str, optional): Legend to be displayed if multple signals are plotted.
        Defaults to None (no legend).

        plot_width (int, optional): Width of the plot.
        Defaults to 700.

        plot_height (int, optional): Height of the plot.
        Defaults to 450.

        line_width (float, optional): Width of the signal line.
        Defaults to 1.5.

        to_notebook (bool, optional): Wheter to output the plot in a notebook.
        Defaults to True.
    """

    if to_notebook:
        output_notebook(hide_banner=True)

    if x_lim is None:
        x_lim = (min(t), max(t))
    else:
        x_lim

    if y_lim is None:
        y_lim = (x.min() * 1.05, x.max() * 1.05)
    else:
        y_lim

    plot = figure(
        title=fig_title,
        x_axis_label=xlabel,
        y_axis_label=ylabel,
        x_range=x_lim,
        y_range=y_lim,
        width=plot_width,
        height=plot_height,
        toolbar_location="below",
    )

    try:
        if x.ndim < 2:  # makes a 1D vector column-wise
            x = x.reshape((len(x), 1))

        if legend is None:
            for i in range(x.shape[1]):
                plot.line(t, x[:, i], line_width=line_width, color=Colorblind[8][i % 8])
        else:
            for i in range(x.shape[1]):
                plot.line(
                    t,
                    x[:, i],
                    line_width=line_width,
                    color=Colorblind[8][i % 8],
                    legend_label=legend[i],
                )

            plot.legend.click_policy = "hide"

            plot.add_layout(plot.legend[0], "right")

        plot.add_tools(
            HoverTool(
                line_policy="nearest",
                point_policy="snap_to_data",
                tooltips=[(ylabel, "$y{0.00}"), (xlabel, "$x{0.00}")],
            )
        )

        show(plot, notebook_handle=to_notebook)

    except Exception as error:
        print("Error:" + str(error))

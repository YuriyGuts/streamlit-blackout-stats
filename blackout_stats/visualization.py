import july
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


@st.cache_data(ttl=600)
def generate_daily_plot(df_daily_downtime):
    """Given a dataframe of daily blackout durations, generate a calendar plot."""

    date_range = july.utils.date_range(
        df_daily_downtime["date"].min(),
        df_daily_downtime["date"].max(),
    )

    fig, _ = calendar_plot(
        dates=date_range,
        data=df_daily_downtime["daily_downtime"],
        title=None,
        value_label=True,
        fontfamily="DejaVu Sans",
        cmap="Oranges",
        ncols=3,
        figsize=(15, 12),
        dpi=96,
    )

    return fig


# Copy-pasted from `july` source code because it needed minor API adjustments
# to be compatible with streamlit.
def calendar_plot(
    dates,
    data,
    cmap="july",
    value_label=False,
    date_label=False,
    weeknum_label=True,
    month_label=True,
    value_format="int",
    ncols=4,
    figsize=None,
    title=None,  # pylint: disable=unused-argument
    **kwargs,
):
    """Create a calendar-shaped heatmap of all months in input dates and data.
    Args:
        dates: List like data structure with dates.
        data: List like data structure with numeric data.
        cmap: Colormap. Any matplotlib colormap works.
        value_label: Whether to add value label inside grid.
        date_label: Whether to add date label inside grid.
        weeknum_label: Whether to label the short axis with week numbers.
        month_label: Whether to add month label(s) along the long axis.
        value_format: Format of value_label: 'int' or 'decimal'. Only relevant if
            `value_label` is True.
        ncols: Number of columns in the calendar plot.
        ax: Matplotlib Axes object.
        figsize: Figure size. Defaults to sensible values determined from 'ncols'.
        kwargs: Parameters passed to `update_rcparams`. Figure aesthetics. Named
            keyword arguments as defined in `update_rcparams` or a dict with any
            rcParam as key(s).
    Returns:
        Matplotlib Axes object.
    """
    # pylint: disable=too-many-arguments,too-many-locals
    july.rcmod.update_rcparams(**kwargs)
    dates_clean, data_clean = july.utils.preprocess_inputs(dates, data)
    # Get unique months (YYYY-MM) in input dates.
    year_months = sorted({day.strftime("%Y-%m") for day in dates_clean})

    nrows = int(np.ceil(len(year_months) / ncols))
    if not figsize:
        if ncols == 6:
            figsize = (12, 0.5 + nrows * 2)
        elif ncols == 5:
            figsize = (12, 1 + nrows * 2)
        elif ncols == 4:
            figsize = (14, 2 + nrows * 2)
        elif ncols == 3:
            figsize = (12, 2 + nrows * 2)

    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)

    for i, year_month in enumerate(year_months):
        month = [day for day in dates_clean if day.strftime("%Y-%m") == year_month]
        vals = [
            val
            for day, val in zip(dates_clean, data_clean)
            if day.strftime("%Y-%m") == year_month
        ]
        july.month_plot(
            month,  # type: ignore
            vals,
            cmap=cmap,
            cmin=data.min(),
            cmax=data.max(),
            date_label=date_label,
            weeknum_label=weeknum_label,
            month_label=month_label,
            value_label=value_label,
            value_format=value_format,
            ax=axes.reshape(-1)[i],
            cal_mode=True,
        )

    for ax in axes.reshape(-1)[len(year_months) :]:
        ax.set_visible(False)

    plt.subplots_adjust(wspace=0.75, hspace=0.5)
    return fig, axes


def release_plot(fig):
    fig.clear()
    plt.close(fig)

import calendar
from datetime import datetime
from typing import Any
from typing import Iterable

import numpy as np
import pandas as pd
from bokeh.layouts import gridplot
from bokeh.models import CategoricalAxis
from bokeh.models import CategoricalScale
from bokeh.models import ColumnDataSource
from bokeh.models import FactorRange
from bokeh.models import HoverTool
from bokeh.models import Plot
from bokeh.models import Rect
from bokeh.models import Text
from bokeh.palettes import Oranges


def generate_year_calendar_heatmap_plot(df_daily_downtime: pd.DataFrame) -> Plot:
    """Given a dataframe of daily blackout durations, generate a calendar heatmap plot."""
    # Calendar rows x calendar columns.
    calendar_layout = (3, 4)
    year = np.max(df_daily_downtime["date"].dt.year)

    # Plot individual months.
    monthly_calendar_plots = [
        [
            generate_single_month_calendar_plot(
                df_daily_downtime=df_daily_downtime,
                year=year,
                month=3 * calendar_row + calendar_col + 1,
            )
            for calendar_col in range(calendar_layout[0])
        ]
        for calendar_row in range(calendar_layout[1])
    ]

    # Arrange months in a grid.
    grid_plot = gridplot(toolbar_location=None, children=monthly_calendar_plots)
    return grid_plot


def align_data_to_calendar_grid(
    data: Iterable[Any],
    calendar_obj: calendar.Calendar,
    year: int,
    month: int,
) -> list[Any]:
    """Pad the specified data with None values to match the day grid layout of a specific month."""
    iterator = iter(data)
    result = [
        None if not day else next(iterator)
        for day in calendar_obj.itermonthdays(year, month)
    ]
    return result


def generate_single_month_calendar_plot(
    df_daily_downtime: pd.DataFrame,
    year: int,
    month: int,
    min_day_value: float = 0.0,
    max_day_value: float = 24.0,
) -> Plot:
    """Generate a calendar heatmap plot for a single month."""
    calendar_obj = calendar.Calendar(firstweekday=0)

    tzinfo = df_daily_downtime["date"].dt.tz
    month_start_date = datetime(year, month, 1, tzinfo=tzinfo)
    month_end_date = datetime(year, month, calendar.monthrange(year, month)[1], tzinfo=tzinfo)

    datetime_labels = [
        f"{year:04d}-{month:02d}-{day:02d}"
        for day in range(month_start_date.day, month_end_date.day + 1)
    ]
    datetime_labels_calendar_aligned = align_data_to_calendar_grid(
        data=datetime_labels,
        calendar_obj=calendar_obj,
        year=year,
        month=month,
    )
    month_week_count = len(datetime_labels_calendar_aligned) // 7

    df_month = pd.DataFrame(df_daily_downtime[
        (df_daily_downtime["date"] >= month_start_date)
        & (df_daily_downtime["date"] <= month_end_date)
    ])

    # Allocate zeros for each day, then replace each day with actual data from the dataframe.
    daily_downtime_values = np.zeros(month_end_date.day, dtype=float)
    for _, row in df_month.iterrows():
        daily_downtime_values[row["date"].day - 1] = row["daily_downtime"]

    daily_downtime_values_calendar_aligned = align_data_to_calendar_grid(
        data=daily_downtime_values,
        calendar_obj=calendar_obj,
        year=year,
        month=month,
    )
    daily_downtime_labels_calendar_aligned = [
        str(int(np.round(val))) if val is not None else None
        for val in daily_downtime_values_calendar_aligned
    ]

    # Rescale 0..24 to 0..255
    daily_downtime_values = (daily_downtime_values - min_day_value) / max_day_value * 255
    daily_downtime_values = daily_downtime_values.astype(int)

    day_backgrounds = [
        "white" if value <= 0 else Oranges[256][255 - value]
        for value in daily_downtime_values
    ]
    day_backgrounds_calendar_aligned = align_data_to_calendar_grid(
        data=day_backgrounds,
        calendar_obj=calendar_obj,
        year=year,
        month=month,
    )

    day_names = list(calendar.day_abbr)
    source_data = {
        "day_names": np.tile(day_names, month_week_count),
        "week_numbers": np.arange(month_week_count).reshape(1, -1).repeat(7).astype(str),
        "datetime_labels": datetime_labels_calendar_aligned,
        "daily_downtime_labels": daily_downtime_labels_calendar_aligned,
        "daily_downtime_values": daily_downtime_values_calendar_aligned,
        "day_backgrounds": day_backgrounds_calendar_aligned,
    }
    source = ColumnDataSource(data=source_data)

    x_range = FactorRange(factors=day_names)
    y_range = FactorRange(factors=np.flip(np.arange(month_week_count).astype(str)))
    x_scale = CategoricalScale()
    y_scale = CategoricalScale()

    plot = Plot(
        x_range=x_range,
        y_range=y_range,
        x_scale=x_scale,
        y_scale=y_scale,
        width=225,
        height=225,
        outline_line_color=None,
    )

    plot.title.text = calendar.month_name[month]
    plot.title.text_font_size = "16px"
    plot.title.text_color = "lightslategray"
    plot.title.offset = 0
    plot.min_border_left = 0
    plot.min_border_right = 25
    plot.min_border_top = 0
    plot.min_border_bottom = 10

    rect = Rect(
        x="day_names",
        y="week_numbers",
        width=0.9,
        height=0.9,
        fill_color="day_backgrounds",
        line_color="silver",
    )
    plot.add_glyph(source, rect)

    text = Text(
        x="day_names",
        y="week_numbers",
        text="daily_downtime_labels",
        text_font_size="12px",
        text_align="center",
        text_baseline="middle",
    )
    plot.add_glyph(source, text)

    xaxis = CategoricalAxis()
    xaxis.major_label_text_font_size = "9px"
    xaxis.major_label_standoff = 0
    xaxis.major_tick_line_color = None
    xaxis.axis_line_color = None
    plot.add_layout(xaxis, "above")

    hover_tool = HoverTool(
        tooltips=[
            ("Дата", "@datetime_labels"),
            ("Тривалість відключень (год.)", "@daily_downtime_values{0.0}"),
        ],
    )
    plot.tools.append(hover_tool)

    return plot

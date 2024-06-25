from datetime import timedelta

import pandas as pd


def format_human_readable_summary_stats_df(
    summary_stats: dict[str, float],
    include_recent_n_days_stats: bool = True,
) -> pd.DataFrame:
    """
    Given the computed summary stats, format them for display as a dataframe.

    Parameters
    ----------
    summary_stats
        The computed summary stats.
    include_recent_n_days_stats
        Whether to include the stats for the most recent N days.
        This makes sense only when displaying the current year.

    Returns
    -------
    The formatted dataframe.
    """
    records = [
        {
            "Показник": "За весь рік (годин)",
            "Значення": summary_stats["total_downtime"],
        }
    ]

    if include_recent_n_days_stats:
        records.extend([
            {
                "Показник": "За останні 7 днів, усього (годин)",
                "Значення": summary_stats["last_7_days_downtime"],
            },
            {
                "Показник": "За останні 7 днів, в середньому за день (годин)",
                "Значення": summary_stats["last_7_days_avg_downtime"],
            },
            {
                "Показник": "За останні 30 днів, усього (годин)",
                "Значення": summary_stats["last_30_days_downtime"],
            },
            {
                "Показник": "За останні 30 днів, в середньому за день (годин)",
                "Значення": summary_stats["last_30_days_avg_downtime"],
            },
        ])

    df = pd.DataFrame.from_records(records, index=["Показник"])
    return df


def format_timedelta(delta: timedelta) -> str:
    """Format a duration (timedelta) object for display."""
    total_seconds = delta.total_seconds()
    hours = int(total_seconds / 3600.0)
    minutes = int((total_seconds - hours * 3600) / 60.0)
    seconds = int(total_seconds - hours * 3600 - minutes * 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def format_last_n_blackouts_df(
    df_blackout_events: pd.DataFrame,
    year: int | None = None,
    n: int = 5
) -> pd.DataFrame:
    """
    Given a dataframe of blackout events, format the most recent N blackouts.

    Parameters
    ----------
    df_blackout_events
        The dataframe containing the blackout events.
    year
        If specified, will only consider the blackouts that occurred in this year.
    n
        The number of most recent records to leave.

    Returns
    -------
    The formatted dataframe.
    """
    # Filter by specific year (if specified).
    if year is not None:
        df_blackout_events = df_blackout_events[df_blackout_events["start_date"].dt.year == year]

    df_last_n_blackouts = pd.DataFrame(df_blackout_events.tail(n))

    # Leave only the time part in the duration.
    df_last_n_blackouts["duration"] = df_last_n_blackouts["duration"].map(format_timedelta)

    # Strip the timezone info from the dates.
    df_last_n_blackouts["start_date"] = df_last_n_blackouts["start_date"].dt.tz_localize(None)
    df_last_n_blackouts["end_date"] = df_last_n_blackouts["end_date"].dt.tz_localize(None)

    # Rename the original columns to be human-readable.
    df_last_n_blackouts.rename(
        columns={
            "id": "№",
            "start_date": "Коли зникло",
            "end_date": "Коли з’явилося",
            "duration": "Тривалість",
        },
        inplace=True,
    )
    df_last_n_blackouts.set_index("№", inplace=True)

    return df_last_n_blackouts

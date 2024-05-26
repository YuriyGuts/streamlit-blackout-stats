from datetime import datetime
from datetime import timedelta
from zoneinfo import ZoneInfo

import pandas as pd
from dateutil.relativedelta import relativedelta


def parse_datetime_column(series: pd.Series, target_tzinfo: ZoneInfo) -> pd.Series:
    return pd.to_datetime(series, format="%Y-%m-%d %H:%M:%S").dt.tz_convert(target_tzinfo)


def transform_events_to_daily_records(
    df_blackout_events: pd.DataFrame,
    target_tzinfo: ZoneInfo,
) -> pd.DataFrame:
    """Given a dataframe of blackout events, generate a daily downtime dataframe."""
    df = df_blackout_events
    df["start_date"] = parse_datetime_column(df["start_date"], target_tzinfo)
    df["end_date"] = parse_datetime_column(df["end_date"], target_tzinfo)
    df = df.sort_values(by="start_date")

    # Determine the date range for the report.
    min_date = df["start_date"].min()
    max_date = datetime.now(tz=target_tzinfo)

    min_date = datetime(min_date.year, min_date.month, min_date.day, tzinfo=target_tzinfo)
    max_date = (
        datetime(max_date.year, max_date.month, max_date.day, tzinfo=target_tzinfo)
        + relativedelta(days=1)
    )

    # Calculate the downtime for each day in the date range.
    daily_downtime_records = []
    current_date = min_date

    while current_date < max_date:
        next_date = current_date + relativedelta(days=1)
        relevant_rows = df[
            ((df["start_date"] < next_date) & (df["end_date"] > current_date))
            | pd.isnull(df["start_date"])
            | pd.isnull(df["end_date"])
        ]

        daily_downtime = timedelta(seconds=0)
        for _, row in relevant_rows.iterrows():
            blackout_start = row["start_date"]
            blackout_end = row["end_date"]

            # Case 1: the day began as DOWN, stayed DOWN till the end.
            if blackout_start < current_date and (
                pd.isnull(blackout_end) or blackout_end >= next_date
            ):
                daily_downtime = next_date - current_date
            # Case 2: the day began as UP, ended as DOWN with one blackout.
            elif current_date <= blackout_start < next_date and (
                pd.isnull(blackout_end) or blackout_end >= next_date
            ):
                daily_downtime += next_date - blackout_start
            # Case 3: the day began as DOWN, ended as UP.
            elif blackout_start < current_date <= blackout_end:
                daily_downtime += blackout_end - current_date
            # Case 4: blackout occurred during the day and recovered within that day.
            elif blackout_start >= current_date and blackout_end < next_date:
                daily_downtime += blackout_end - blackout_start

        daily_downtime_records.append(
            {
                "date": current_date,
                "daily_downtime": round(daily_downtime.total_seconds() / 3600.0, 2),
            }
        )
        current_date = next_date

    df_daily_downtime = pd.DataFrame.from_records(daily_downtime_records).sort_values(by="date")
    return df_daily_downtime


def generate_rolling_7d_data(df_daily_downtime: pd.DataFrame) -> pd.DataFrame:
    df_rolling_stats = df_daily_downtime.copy()
    df_rolling_stats["date"] = pd.to_datetime(df_rolling_stats["date"])
    df_rolling_stats.set_index("date", inplace=True)
    return df_rolling_stats.rolling("7d").mean()


def compute_summary_statistics(df_daily_downtime: pd.DataFrame) -> dict[str, float]:
    total_downtime = df_daily_downtime["daily_downtime"].sum()
    last_7_days_downtime = df_daily_downtime.tail(7)["daily_downtime"].sum()
    last_7_days_avg_downtime = last_7_days_downtime / 7.0
    last_30_days_downtime = df_daily_downtime.tail(30)["daily_downtime"].sum()
    last_30_days_avg_downtime = last_30_days_downtime / 30.0

    result = {
        "total_downtime": total_downtime,
        "last_7_days_downtime": last_7_days_downtime,
        "last_7_days_avg_downtime": last_7_days_avg_downtime,
        "last_30_days_downtime": last_30_days_downtime,
        "last_30_days_avg_downtime": last_30_days_avg_downtime,
    }

    return result

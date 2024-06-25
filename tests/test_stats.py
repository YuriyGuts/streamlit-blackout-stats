from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd

from blackout_stats import stats as sut


def test_transform_events_to_daily_records_all_cases(df_blackout_events):
    # GIVEN a dataframe of blackout events
    # WHEN transforming the events to daily records
    utc_tzinfo = ZoneInfo("UTC")
    actual_df = sut.transform_events_to_daily_records(
        df_blackout_events,
        target_tzinfo=utc_tzinfo,
        max_output_date=datetime.fromisoformat("2024-01-09T00:00:00Z"),
    )

    # THEN the daily downtime values should be calculated correctly
    expected_df = pd.DataFrame.from_records([
        {"date": datetime(2024, 1, 1, tzinfo=utc_tzinfo), "daily_downtime": 24.0},
        {"date": datetime(2024, 1, 2, tzinfo=utc_tzinfo), "daily_downtime": 1.5},
        {"date": datetime(2024, 1, 3, tzinfo=utc_tzinfo), "daily_downtime": 1.0},
        {"date": datetime(2024, 1, 4, tzinfo=utc_tzinfo), "daily_downtime": 0.0},
        {"date": datetime(2024, 1, 5, tzinfo=utc_tzinfo), "daily_downtime": 3.0},
        {"date": datetime(2024, 1, 6, tzinfo=utc_tzinfo), "daily_downtime": 0.0},
        {"date": datetime(2024, 1, 7, tzinfo=utc_tzinfo), "daily_downtime": 1.0},
        {"date": datetime(2024, 1, 8, tzinfo=utc_tzinfo), "daily_downtime": 24.0},
        {"date": datetime(2024, 1, 9, tzinfo=utc_tzinfo), "daily_downtime": 3.5},
    ])
    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_transform_events_to_daily_records_timezone_aware():
    # GIVEN a dataframe of blackout events where blackouts start and end at midnight UTC
    blackout_records = [
        {
            "id": 1,
            "start_date": datetime.fromisoformat("2024-01-01T00:00:00Z"),
            "end_date": datetime.fromisoformat("2024-01-02T00:00:00Z"),
        },
    ]
    df_blackout_events = pd.DataFrame.from_records(blackout_records)

    # WHEN transforming the events to daily records using a specific timezone
    kyiv_tzinfo = ZoneInfo("Europe/Kyiv")
    actual_df = sut.transform_events_to_daily_records(
        df_blackout_events,
        target_tzinfo=kyiv_tzinfo,
        max_output_date=datetime(2024, 1, 2, tzinfo=kyiv_tzinfo),
    )

    # THEN the daily downtime values should be correctly split across days according to the timezone
    expected_df = pd.DataFrame.from_records([
        {"date": datetime(2024, 1, 1, tzinfo=kyiv_tzinfo), "daily_downtime": 22.0},
        {"date": datetime(2024, 1, 2, tzinfo=kyiv_tzinfo), "daily_downtime": 2.0},
    ])
    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_compute_rolling_statistics():
    # GIVEN a dataframe of daily downtime durations
    tzinfo = ZoneInfo("Europe/Kyiv")
    daily_downtimes = [0.0, 3.5, 2.5, 0.5, 0.0, 4.0, 20.0, 1.0, 0.0]
    daily_downtime_records = [
        {"date": datetime(2024, 1, idx + 1, tzinfo=tzinfo), "daily_downtime": downtime}
        for idx, downtime in enumerate(daily_downtimes)
    ]
    df_daily_downtime = pd.DataFrame.from_records(daily_downtime_records)

    # WHEN computing the rolling statistics
    actual_df = sut.compute_rolling_statistics(df_daily_downtime, period="2d")

    # THEN the rolling statistics should be computed correctly for each date
    expected_df = pd.DataFrame.from_records(
        [
            {"date": datetime(2024, 1, 1, tzinfo=tzinfo), "daily_downtime": 0.0},
            {"date": datetime(2024, 1, 2, tzinfo=tzinfo), "daily_downtime": 1.75},
            {"date": datetime(2024, 1, 3, tzinfo=tzinfo), "daily_downtime": 3.0},
            {"date": datetime(2024, 1, 4, tzinfo=tzinfo), "daily_downtime": 1.5},
            {"date": datetime(2024, 1, 5, tzinfo=tzinfo), "daily_downtime": 0.25},
            {"date": datetime(2024, 1, 6, tzinfo=tzinfo), "daily_downtime": 2.0},
            {"date": datetime(2024, 1, 7, tzinfo=tzinfo), "daily_downtime": 12.0},
            {"date": datetime(2024, 1, 8, tzinfo=tzinfo), "daily_downtime": 10.5},
            {"date": datetime(2024, 1, 9, tzinfo=tzinfo), "daily_downtime": 0.5},
        ],
        index="date",
    )

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_compute_summary_statistics():
    # GIVEN a dataframe of daily downtime durations
    tzinfo = ZoneInfo("Europe/Kyiv")
    daily_downtimes = [0.0, 3.5, 2.5, 0.5, 0.0, 4.0, 20.0, 1.0, 0.0]
    daily_downtime_records = [
        {"date": datetime(2024, 1, idx + 1, tzinfo=tzinfo), "daily_downtime": downtime}
        for idx, downtime in enumerate(daily_downtimes)
    ]
    df_daily_downtime = pd.DataFrame.from_records(daily_downtime_records)

    # WHEN computing summary statistics
    summary_stats = sut.compute_summary_statistics(df_daily_downtime)

    # THEN the totals and averages should be computed correctly
    assert summary_stats == {
        "total_downtime": 31.5,
        "last_7_days_downtime": 28.0,
        "last_7_days_avg_downtime": 4.0,
        "last_30_days_downtime": 31.5,
        "last_30_days_avg_downtime": 1.05,
    }

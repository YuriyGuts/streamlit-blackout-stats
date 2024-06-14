from datetime import datetime
from datetime import timedelta

import pandas as pd
import pytest

from blackout_stats import formatting as sut


def test_format_human_readable_summary_stats_df():
    summary_stats = {
        "total_downtime": 31.5,
        "last_7_days_downtime": 28.0,
        "last_7_days_avg_downtime": 4.0,
        "last_30_days_downtime": 31.5,
        "last_30_days_avg_downtime": 1.05,
    }
    actual_df = sut.format_human_readable_summary_stats_df(summary_stats)
    expected_records = [
        {
            "Показник": "За весь час (годин)",
            "Значення": 31.5,
        },
        {
            "Показник": "За останні 7 днів, усього (годин)",
            "Значення": 28.0,
        },
        {
            "Показник": "За останні 7 днів, в середньому за день (годин)",
            "Значення": 4.0,
        },
        {
            "Показник": "За останні 30 днів, усього (годин)",
            "Значення": 31.5,
        },
        {
            "Показник": "За останні 30 днів, в середньому за день (годин)",
            "Значення": 1.05,
        },
    ]
    expected_df = pd.DataFrame.from_records(expected_records, index="Показник")
    pd.testing.assert_frame_equal(actual_df, expected_df)


@pytest.mark.parametrize(
    "delta, expected_formatted",
    [
        (timedelta(seconds=1, milliseconds=250), "00:00:01"),
        (timedelta(seconds=75), "00:01:15"),
        (timedelta(hours=12, minutes=37), "12:37:00"),
        (timedelta(days=2), "48:00:00"),
        (timedelta(days=1, hours=23, minutes=59, seconds=58), "47:59:58"),
    ]
)
def test_format_timedelta(delta, expected_formatted):
    assert sut.format_timedelta(delta) == expected_formatted


def test_format_last_n_blackouts(df_blackout_events):
    actual_df = sut.format_last_n_blackouts_df(df_blackout_events, n=2)
    expected_records = [
        {
            "№": 6,
            "Коли зникло": datetime.fromisoformat("2024-01-07T23:00:00Z"),
            "Коли з’явилося": datetime.fromisoformat("2024-01-09T02:30:00Z"),
            "Тривалість": "27:30:00",
        },
        {
            "№": 7,
            "Коли зникло": datetime.fromisoformat("2024-01-09T21:00:00Z"),
            "Коли з’явилося": datetime.fromisoformat("2024-01-09T22:00:00Z"),
            "Тривалість": "01:00:00",
        },
    ]
    expected_df = pd.DataFrame.from_records(expected_records, index="№")
    pd.testing.assert_frame_equal(actual_df, expected_df)

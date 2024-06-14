# Helper shortcut to parse ISO dates in tests.
from datetime import datetime
from datetime import timedelta

import pandas as pd
import pytest


@pytest.fixture
def df_blackout_events():
    blackout_records = [
        # Case 1: the day began as DOWN, stayed DOWN till the end.
        {
            "id": 1,
            "start_date": datetime.fromisoformat("2024-01-01T00:00:00Z"),
            "end_date": datetime.fromisoformat("2024-01-02T00:00:00Z"),
            "duration": timedelta(hours=24),
        },
        # Case 2: the day began as UP, ended as DOWN with one blackout.
        # AND
        # Case 3: the day began as DOWN, ended as UP.
        {
            "id": 2,
            "start_date": datetime.fromisoformat("2024-01-02T22:30:00Z"),
            "end_date": datetime.fromisoformat("2024-01-03T01:00:00Z"),
            "duration": timedelta(hours=2, minutes=30),
        },
        # Case 4: blackout occurred during the day and recovered within that day.
        {
            "id": 3,
            "start_date": datetime.fromisoformat("2024-01-05T01:00:00Z"),
            "end_date": datetime.fromisoformat("2024-01-05T02:00:00Z"),
            "duration": timedelta(hours=1),
        },
        {
            "id": 4,
            "start_date": datetime.fromisoformat("2024-01-05T03:00:00Z"),
            "end_date": datetime.fromisoformat("2024-01-05T04:30:00Z"),
            "duration": timedelta(hours=1, minutes=30),
        },
        {
            "id": 5,
            "start_date": datetime.fromisoformat("2024-01-05T21:00:00Z"),
            "end_date": datetime.fromisoformat("2024-01-05T21:30:00Z"),
            "duration": timedelta(minutes=30),
        },
        # Generate some more data to test
        {
            "id": 6,
            "start_date": datetime.fromisoformat("2024-01-07T23:00:00Z"),
            "end_date": datetime.fromisoformat("2024-01-09T02:30:00Z"),
            "duration": timedelta(days=1, hours=3, minutes=30),
        },
        {
            "id": 7,
            "start_date": datetime.fromisoformat("2024-01-09T21:00:00Z"),
            "end_date": datetime.fromisoformat("2024-01-09T22:00:00Z"),
            "duration": timedelta(hours=1),
        },
    ]

    df_blackout_events = pd.DataFrame.from_records(blackout_records)
    return df_blackout_events

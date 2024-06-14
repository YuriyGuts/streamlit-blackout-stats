from datetime import timedelta

import pandas as pd


def format_human_readable_summary_stats_df(summary_stats: dict[str, float]) -> pd.DataFrame:
    records = [
        {
            "Показник": "За весь час (годин)",
            "Значення": summary_stats["total_downtime"],
        },
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
    ]

    df = pd.DataFrame.from_records(records, index=["Показник"])
    return df


def format_timedelta(delta: timedelta) -> str:
    total_seconds = delta.total_seconds()
    hours = int(total_seconds / 3600.0)
    minutes = int((total_seconds - hours * 3600) / 60.0)
    seconds = int(total_seconds - hours * 3600 - minutes * 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def format_last_n_blackouts_df(df_blackout_events: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    df_last_n_blackouts = pd.DataFrame(df_blackout_events.tail(n))

    # Leave only the time part in the duration
    df_last_n_blackouts["duration"] = df_last_n_blackouts["duration"].map(format_timedelta)

    # Rename the original columns to be human-readable
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

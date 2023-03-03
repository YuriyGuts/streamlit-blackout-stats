import pandas as pd


def format_human_readable_summary_stats_df(summary_stats):
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


def format_last_n_blackouts_df(df_blackout_events, n=5):
    df_last_n_blackouts = pd.DataFrame(df_blackout_events.tail(n))

    # Leave only the time part in the duration
    df_last_n_blackouts["duration"] = (
        df_last_n_blackouts["duration"].astype(str).map(lambda s: s.split(" ")[-1])
    )

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

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

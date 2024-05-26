#!/usr/bin/env python3
"""Entry point for the Streamlit app."""

from zoneinfo import ZoneInfo

import streamlit as st

from blackout_stats.data_access import read_blackout_events_from_google_sheet
from blackout_stats.formatting import format_human_readable_summary_stats_df
from blackout_stats.formatting import format_last_n_blackouts_df
from blackout_stats.stats import compute_summary_statistics
from blackout_stats.stats import generate_rolling_7d_data
from blackout_stats.stats import transform_events_to_daily_records
from blackout_stats.visualization import generate_daily_plot


def main() -> None:
    location_name = st.secrets["location_name"]
    st.set_page_config(page_title=f"Статистика відключень: {location_name}")
    st.title(f"💡 Статистика відключень: {location_name}")
    target_tzinfo = ZoneInfo(st.secrets["target_timezone_name"])

    df_blackout_events = read_blackout_events_from_google_sheet(
        gcp_service_account_info=st.secrets["gcp_service_account"].to_dict(),
        sheet_url=st.secrets["private_gsheets_url"],
    )
    df_daily_downtime = transform_events_to_daily_records(
        df_blackout_events=df_blackout_events,
        target_tzinfo=target_tzinfo,
    )
    summary_stats = compute_summary_statistics(df_daily_downtime)

    st.header("📊 Скільки часу не було світла")
    df_summary_stats = format_human_readable_summary_stats_df(summary_stats)
    st.dataframe(df_summary_stats.style.format("{:.1f}"))

    st.header("🗓️ Календар тривалості відключень (годин за добу)")
    plot = generate_daily_plot(df_daily_downtime)

    st.header("📈 Середньотижнева тривалість відключень (годин за добу)")
    df_rolling_stats = generate_rolling_7d_data(df_daily_downtime)
    st.line_chart(df_rolling_stats)

    st.header("⏱️ Останні 5 вимкнень")
    df_last_5_blackouts = format_last_n_blackouts_df(df_blackout_events, n=5)
    st.dataframe(df_last_5_blackouts)


if __name__ == "__main__":
    main()

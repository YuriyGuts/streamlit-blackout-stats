#!/usr/bin/env python3
"""Entry point for the Streamlit app."""
import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

from blackout_stats.data_access import read_blackout_events_from_google_sheet
from blackout_stats.formatting import format_human_readable_summary_stats_df
from blackout_stats.formatting import format_last_n_blackouts_df
from blackout_stats.stats import compute_rolling_statistics
from blackout_stats.stats import compute_summary_statistics
from blackout_stats.stats import transform_events_to_daily_records
from blackout_stats.visualization import generate_year_calendar_heatmap_plot


def main() -> None:
    location_name = st.secrets["location_name"]
    target_tzinfo = ZoneInfo(st.secrets["target_timezone_name"])

    st.set_page_config(page_title=f"Статистика відключень: {location_name}")
    st.title("💡 Статистика відключень")
    st.subheader(location_name)

    # Download the power outage data.
    df_blackout_events = read_blackout_events_from_google_sheet(
        gcp_service_account_info=st.secrets["gcp_service_account"].to_dict(),
        sheet_url=st.secrets["private_gsheets_url"],
    )
    df_daily_downtime = transform_events_to_daily_records(
        df_blackout_events=df_blackout_events,
        target_tzinfo=target_tzinfo,
    )
    last_update_date = df_blackout_events["end_date"].max()

    st.write("Дані відображають фактичні відключення.")
    st.write("Дані можуть оновлюватися з затримкою та не враховувати недавні відключення.")
    st.write(f"Останнє оновлення даних: {last_update_date:%Y-%m-%d %H:%M}.")

    available_years = [2022, 2023, 2024, 2025]
    year_selector = st.selectbox(
        label="Оберіть рік",
        placeholder="Оберіть рік",
        options=available_years,
        index=len(available_years) - 1,
    )
    is_current_year_selected = (year_selector == datetime.datetime.now().year == year_selector)

    # Filter the outage data to the currently selected year.
    df_blackout_events = pd.DataFrame(
        df_blackout_events[df_blackout_events["start_date"].dt.year == year_selector]
    )
    df_daily_downtime = pd.DataFrame(
        df_daily_downtime[df_daily_downtime["date"].dt.year == year_selector]
    )

    summary_stats = compute_summary_statistics(df_daily_downtime)

    st.header("📊 Скільки часу не було світла")
    df_summary_stats = format_human_readable_summary_stats_df(
        summary_stats=summary_stats,
        include_recent_n_days_stats=is_current_year_selected,
    )
    st.dataframe(
        data=df_summary_stats,
        column_config={
            "Значення": st.column_config.NumberColumn(format="%.1f"),
        },
        hide_index=True,
    )

    st.header("🗓️ Календар тривалості відключень")
    st.caption("(годин за добу)")
    plot = generate_year_calendar_heatmap_plot(df_daily_downtime)
    st.bokeh_chart(plot)

    st.header("📈 Середньотижнева тривалість відключень")
    st.caption("(годин за добу)")
    df_rolling_stats = compute_rolling_statistics(df_daily_downtime)
    st.line_chart(df_rolling_stats)

    st.header("⏱️ Останні 5 відключень")
    df_last_5_blackouts = format_last_n_blackouts_df(df_blackout_events, year=year_selector, n=5)
    st.dataframe(df_last_5_blackouts)


if __name__ == "__main__":
    main()

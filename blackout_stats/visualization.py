import pandas as pd
import streamlit as st
from bokeh.models import Plot


@st.cache_data(ttl=600)
def generate_daily_plot(df_daily_downtime: pd.DataFrame) -> Plot:
    """Given a dataframe of daily blackout durations, generate a calendar plot."""
    return Plot()

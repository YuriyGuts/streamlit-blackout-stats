import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect


def read_blackout_events_from_local_file(filename):
    return pd.read_csv(filename)


def read_blackout_events_from_google_sheet(gcp_service_account, sheet_url):
    @st.cache_data(ttl=600)
    def query_google_sheet(query):
        rows = conn.execute(query, headers=1)
        rows = rows.fetchall()
        return pd.DataFrame(rows)

    credentials = service_account.Credentials.from_service_account_info(
        gcp_service_account, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    conn = connect(credentials=credentials)

    query = f'SELECT * from "{sheet_url}"'
    rows = query_google_sheet(query)

    return pd.DataFrame(rows)

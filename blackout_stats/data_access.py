from typing import Any

import pandas as pd
import streamlit as st
from shillelagh.backends.apsw.db import connect


def read_blackout_events_from_local_file(filename: str) -> pd.DataFrame:
    """
    Read blackout events from a local CSV file and convert the results to a dataframe.

    Parameters
    ----------
    filename
        The path to the CSV file to read.

    Returns
    -------
    Dataframe containing the blackout events.
    """
    return pd.read_csv(filename)


def read_blackout_events_from_google_sheet(
    gcp_service_account_info: dict[str, Any],
    sheet_url: str,
) -> pd.DataFrame:
    """
    Read blackout events from a Google Sheet and convert the results to a dataframe.

    Parameters
    ----------
    gcp_service_account_info
        GCP service account info to access the Google Sheet.
    sheet_url
        URL of the Google Sheet.

    Returns
    -------
    Dataframe containing the rows from the Google Sheet.
    """
    @st.cache_data(ttl=600)
    def query_google_sheet(query: str) -> pd.DataFrame:
        """Run the specified Google Sheets query and convert the results to a dataframe."""
        cursor = conn.execute(query)

        # Infer column names.
        if cursor.description:
            column_names = [desc[0] for desc in cursor.description]
        else:
            # Fall back to assumed column names. This should not happen in normal conditions.
            # If it does, it means there is something wrong with reading the Google Sheet.
            column_names = ["id", "start_date", "end_date", "duration"]

        rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=column_names)

    conn = connect(
        ":memory:",
        adapter_kwargs={"gsheetsapi": {"service_account_info": gcp_service_account_info}},
    )

    query = f'SELECT * from "{sheet_url}"'
    df = query_google_sheet(query)

    return df

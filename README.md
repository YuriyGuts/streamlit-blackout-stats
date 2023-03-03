# Streamlit App for Power Outage Statistics

This app reads power outage events from a private Google Sheet (via a GCP service account) and
displays various time-aware statistics about the durations of the outages. 

## Installation

This project requires Python 3.9 or below.
Newer Python versions are not compatible with the `gsheetsdb` package which is now deprecated.

```shell
python3.9 -m venv ~/.virtualenvs/streamlit-blackout-events
source ~/.virtualenvs/streamlit-blackout-events/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Next, create a local `.streamlit/secrets.toml` file according
to [Streamlit documentation](https://docs.streamlit.io/knowledge-base/tutorials/databases/private-gsheet).

## Run locally:

```shell
streamlit run app.py
```

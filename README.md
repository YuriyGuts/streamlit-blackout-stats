# Streamlit App for Power Outage Statistics

This app reads power outage events from a private Google Sheet (via a GCP service account) and
displays various statistics that describe the temporal dynamics of the outages (calendar heatmap,
weekly rolling averages, etc.).

## Installation

This project requires Python 3.12 (or above) and [Poetry](https://python-poetry.org/).

Install the project dependencies:

```shell
poetry install
```

Next, create a local `.streamlit/secrets.toml` file according
to [Streamlit documentation](https://docs.streamlit.io/knowledge-base/tutorials/databases/private-gsheet).

```toml
location_name = "Home"
target_timezone_name = "Europe/Kyiv"
private_gsheets_url = "https://docs.google.com/spreadsheets/d/.../edit"

[gcp_service_account]
type = "service_account"
# ... more GCP account details here ...
```

## Startup

Run the app locally:

```shell
source ./.venv/bin/activate
make run
```

## Development

Install the dev dependencies:
```
poetry install --with dev
```

Run the tests:

```shell
source ./.venv/bin/activate
make test
```

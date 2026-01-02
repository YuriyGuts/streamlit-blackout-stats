# Streamlit App for Power Outage Statistics

This app reads power outage events from a private Google Sheet (via a GCP service account) and
displays various statistics that describe the temporal dynamics of the outages (calendar heatmap,
weekly rolling averages, etc.).

<img width="187" alt="image" src="https://github.com/YuriyGuts/streamlit-blackout-stats/assets/2750531/ed145744-82e3-4810-8c50-7f05d2c546f2">

## Installation

This project requires Python 3.12 (or above) and [uv](https://docs.astral.sh/uv/).

Install the project dependencies:

```shell
uv sync
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

## Usage

Run the app locally:

```shell
make run
```

## Development

Install all dependencies (including dev):

```shell
uv sync
```

### Available Commands

Run `make help` to see all available commands:

| Command | Description |
|---------|-------------|
| `make run` | Start the Streamlit app |
| `make test` | Run tests |
| `make lint` | Run linter |
| `make lint-fix` | Run linter with auto-fix |
| `make format` | Format code |
| `make typecheck` | Run type checker |
| `make check` | Run all checks (lint, typecheck, test) |
| `make clean` | Remove cache directories |

### Running Checks

Before committing, run all checks:

```shell
make check
```

Or run individual checks:

```shell
make lint
make typecheck
make test
```

## License

[BSD-3-Clause](LICENSE).

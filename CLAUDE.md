# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup and running

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
weather 90210
```

The venv must use `urllib3<2` (already pinned) because the system Python 3.9 on this machine ships with LibreSSL, which urllib3 v2 dropped support for.

## Architecture

The Python package lives in `source/` (not `weather/`). The `weather` command is wired via `pyproject.toml` → `source.cli:main`.

Two-module split:

- **`source/client.py`** — all network I/O and data shaping. `fetch_conditions(zip_code)` returns `current_condition[0]` from the wttr.in JSON response. `format_conditions(condition, units)` is a pure function that formats that dict into the output line. All failures raise `WeatherAPIError`.
- **`source/cli.py`** — `build_parser()` returns a configured `ArgumentParser` (kept separate from `main()` so it can be tested without I/O). `main()` calls parse → fetch → format → print, with a single `except WeatherAPIError` that writes to stderr and exits 1.

## Extending

- **New flags**: add `add_argument()` calls to `build_parser()` in `source/cli.py`. A `--format` flag placeholder is already commented there.
- **New output fields**: `format_conditions()` in `source/client.py` reads from the `current_condition[0]` dict; all available fields come from `https://wttr.in/{zip}?format=j1`.
- **Version**: bump `__version__` in `source/__init__.py` and `version` in `pyproject.toml` together.

# weather

A minimal CLI tool for current weather conditions via [wttr.in](https://wttr.in). No API key required.

## Installation

```bash
git clone https://github.com/johnhines/weather.git
cd weather
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
weather <zip_code> [--units imperial|metric]
```

### Examples

```
$ weather 90210
72°F (Feels like 68°F) | Partly cloudy | Humidity: 55% | Wind: 12 mph

$ weather 10001 --units metric
22°C (Feels like 20°C) | Overcast | Humidity: 61% | Wind: 19 km/h
```

### Flags

| Flag | Description | Default |
|------|-------------|---------|
| `zip_code` | US zip code to look up | *(required)* |
| `--units` | `imperial` (°F, mph) or `metric` (°C, km/h) | `imperial` |
| `--version` | Print version and exit | |
| `--help` | Show usage | |

## Error handling

Errors are written to stderr and exit with code 1, keeping stdout clean for piping:

```
$ weather 00000
Error: API returned status 404 for zip code '00000'
$ echo $?
1
```

## Requirements

- Python 3.9+
- [requests](https://pypi.org/project/requests/)

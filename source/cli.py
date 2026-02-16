"""Command-line interface for the weather tool."""
import argparse
import sys

from source import __version__
from source.client import WeatherAPIError, fetch_conditions, format_conditions


def build_parser() -> argparse.ArgumentParser:
    """Return a configured ArgumentParser. Factored out for testability."""
    parser = argparse.ArgumentParser(
        prog="weather",
        description="Fetch current weather conditions for a US zip code.",
    )
    parser.add_argument(
        "zip_code",
        help="US zip code to look up (e.g. 90210)",
    )
    parser.add_argument(
        "--units",
        choices=["imperial", "metric"],
        default="imperial",
        help="Unit system for temperature and wind speed (default: imperial)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"weather {__version__}",
    )
    # --format json  (placeholder for future output formats)
    # parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser


def main() -> None:
    """Entry point: parse args, fetch conditions, print result."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        condition = fetch_conditions(args.zip_code)
        line = format_conditions(condition, units=args.units)
        print(line)
    except WeatherAPIError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

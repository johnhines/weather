"""Weather API client for wttr.in."""
import requests


class WeatherAPIError(Exception):
    """Raised when the weather API request fails for any reason."""


def fetch_conditions(zip_code: str) -> dict:
    """Fetch current conditions for the given US zip code from wttr.in.

    Returns the current_condition[0] dict from the JSON response.
    Raises WeatherAPIError on network errors, timeouts, bad status, or bad JSON.
    """
    url = f"https://wttr.in/{zip_code}?format=j1"
    try:
        response = requests.get(url, timeout=10)
    except requests.ConnectionError as e:
        raise WeatherAPIError(f"Network error: {e}") from e
    except requests.Timeout as e:
        raise WeatherAPIError("Request timed out") from e

    if response.status_code != 200:
        raise WeatherAPIError(
            f"API returned status {response.status_code} for zip code '{zip_code}'"
        )

    try:
        data = response.json()
        return data["current_condition"][0]
    except (requests.exceptions.JSONDecodeError, ValueError) as e:
        raise WeatherAPIError(f"Invalid JSON response: {e}") from e
    except (KeyError, IndexError) as e:
        raise WeatherAPIError(f"Unexpected response structure: {e}") from e


def format_conditions(condition: dict, units: str = "imperial") -> str:
    """Format a current_condition dict into a single output line.

    Args:
        condition: The current_condition[0] dict from wttr.in.
        units: "imperial" for °F/mph, "metric" for °C/km/h.

    Returns:
        A formatted string like:
        "72°F (Feels like 68°F) | Partly cloudy | Humidity: 55% | Wind: 12 mph"
    """
    try:
        if units == "metric":
            temp = condition["temp_C"]
            feels_like = condition["FeelsLikeC"]
            wind = condition["windspeedKmph"]
            temp_unit = "°C"
            wind_unit = "km/h"
        else:
            temp = condition["temp_F"]
            feels_like = condition["FeelsLikeF"]
            wind = condition["windspeedMiles"]
            temp_unit = "°F"
            wind_unit = "mph"

        description = condition["weatherDesc"][0]["value"]
        humidity = condition["humidity"]
    except KeyError as e:
        raise WeatherAPIError(f"Missing field in weather data: {e}") from e

    return (
        f"{temp}{temp_unit} (Feels like {feels_like}{temp_unit})"
        f" | {description}"
        f" | Humidity: {humidity}%"
        f" | Wind: {wind} {wind_unit}"
    )

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. Section 1: The Question
    Option C "Pick the day"

    A student club is planning an outdoor event somewhere in Massachusetts in the next week and needs to pick the day. The organizer wants a table of the next seven days, today included, whether each day meets the club's rules, and the best day, for whatever town they type in.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 2. Section 2: My plan before AI
    My plan is to collect the desired town in Massachusetts from the code user. Then find the towns location using the open meteo interface. Next I will retrive the weather data for multiple days that the event could be hosted, as it is an outdoor event. Next a table will present these results to the user to analyze and the code will also present a recommendation of which day is best including the score out of 10.

    My tool will need a function to find the towns location, retrieve the weather forecast, and a way to evaluate the days and calculate a score out of 10.

    These will use the open meteo addresses of Geocoding API and the weather forecasting API.

     https://open-meteo.com/en/docs/geocoding-api

     https://open-meteo.com/en/docs

    I will know I have every record by checking that seven results of dates are returned and also shown in the final table.

    For section 6, I will check that the number of dates and the number of weather records are both 7. This will confirm that I collected all the days of forecasts needed.
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    place = "Wellesley"
    state = "Massachusetts"

    lowest_high_f = 55
    highest_high_f = 80
    max_rain_chance = 30
    max_wind_mph = 15
    return (
        highest_high_f,
        lowest_high_f,
        max_rain_chance,
        max_wind_mph,
        place,
        state,
    )


@app.cell
def _():
    #finding town coordinates
    import requests

    def get_coordinates(place, state):
        url = "https://geocoding-api.open-meteo.com/v1/search"

        params = {
            "name": place,
            "count": 100,
            "countryCode": "US"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for location in data.get("results", []):
            if location.get("admin1") == state:
                return location

        return None

    return get_coordinates, requests


@app.cell
def _(get_coordinates, place, state):
    location = get_coordinates(place, state)

    if location is None:
        print("No matching town found in Massachusetts.")
    else:
        latitude = location["latitude"]
        longitude = location["longitude"]

        print("Town:", location["name"])
        print("State:", location["admin1"])
        print("Latitude:", latitude)
        print("Longitude:", longitude)
    return latitude, longitude


@app.cell
def _(requests):
    #finding 7 day weather forecast 
    def get_forecast(latitude, longitude):
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
                "wind_speed_10m_max"
            ],
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "timezone": "America/New_York",
            "forecast_days": 7
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()["daily"]

    return (get_forecast,)


@app.cell
def _(get_forecast, latitude, longitude):
    forecast = get_forecast(latitude, longitude)

    print("Forecast retrieved successfully!")
    print("Number of days:", len(forecast["time"]))

    return (forecast,)


@app.cell
def _(forecast, highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph):
    #one record per day
    days = []

    for date, high, low, rain, wind in zip(
        forecast["time"],
        forecast["temperature_2m_max"],
        forecast["temperature_2m_min"],
        forecast["precipitation_probability_max"],
        forecast["wind_speed_10m_max"]
    ):
        passes = (
            lowest_high_f <= high <= highest_high_f
            and rain <= max_rain_chance
            and wind <= max_wind_mph
        )

        broken_rules = (
            int(high < lowest_high_f or high > highest_high_f)
            + int(rain > max_rain_chance)
            + int(wind > max_wind_mph)
        )

        days.append({
            "Date": date,
            "High (F)": high,
            "Low (F)": low,
            "Rain (%)": rain,
            "Wind (mph)": wind,
            "Passes": passes,
            "Broken Rules": broken_rules
        })

    print("Days evaluated:", len(days))
    return (days,)


@app.cell
def _(days, mo):
    #displaying table 

    mo.ui.table([
        {
            "Date": record["Date"],
            "High (F)": record["High (F)"],
            "Low (F)": record["Low (F)"],
            "Rain (%)": record["Rain (%)"],
            "Wind (mph)": record["Wind (mph)"],
            "Passes": record["Passes"]
        }
        for record in days
    ])

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    5. The Answer
    """)
    return


@app.cell
def _(days):
    #best day recommendation 

    passing_days = [
        record for record in days if record["Passes"]
    ]

    if passing_days:
        best_day = min(
            passing_days,
            key=lambda record: (
                record["Rain (%)"],
                record["Wind (mph)"]
            )
        )

        print(
            f"The best day is {best_day['Date']} because "
            f"it passes all weather rules, with a "
            f"{best_day['Rain (%)']}% chance of rain "
            f"and wind of {best_day['Wind (mph)']} mph."
        )

    elif days:
        best_day = min(
            days,
            key=lambda record: record["Broken Rules"]
        )

        print(
            f"No days meet all weather requirements. "
            f"The best alternative is {best_day['Date']} "
            f"because it breaks the fewest rules "
            f"({best_day['Broken Rules']})."
        )

    else:
        print("No forecast days available.")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    6. How I know these numbers are right
    """)
    return


if __name__ == "__main__":
    app.run()

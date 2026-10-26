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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #3. Inputs
    """)
    return


@app.cell
def _():
    #Inputs
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #4. The Work
    """)
    return


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

        daily = response.json()["daily"]

        records = []

        for _date, _high, _low, _rain, _wind in zip(
            daily["time"],
            daily["temperature_2m_max"],
            daily["temperature_2m_min"],
            daily["precipitation_probability_max"],
            daily["wind_speed_10m_max"]
        ):
            records.append({
                "Date": _date,
                "High (F)": _high,
                "Low (F)": _low,
                "Rain (%)": _rain,
                "Wind (mph)": _wind
            })

        return records

    return (get_forecast,)


@app.cell
def _(get_forecast, latitude, longitude):
    forecast = get_forecast(latitude, longitude)

    print("Forecast retrieved successfully!")
    print("Number of days:", len(forecast))

    return (forecast,)


@app.cell
def _(forecast, highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph):
    #one record per day
    days = []

    for _forecast_day in forecast:
        _high = _forecast_day["High (F)"]
        _rain = _forecast_day["Rain (%)"]
        _wind = _forecast_day["Wind (mph)"]

        _passes = (
            lowest_high_f <= _high <= highest_high_f
            and _rain <= max_rain_chance
            and _wind <= max_wind_mph
        )

        _broken_rules = (
            int(_high < lowest_high_f or _high > highest_high_f)
            + int(_rain > max_rain_chance)
            + int(_wind > max_wind_mph)
        )

        days.append({
            "Date": _forecast_day["Date"],
            "High (F)": _high,
            "Low (F)": _forecast_day["Low (F)"],
            "Rain (%)": _rain,
            "Wind (mph)": _wind,
            "Passes": _passes,
            "Broken Rules": _broken_rules
        })

    print("Days evaluated:", len(days))
    return (days,)


@app.cell
def _(forecast):
    #save wellesley data to CSV file 
    import csv
    from pathlib import Path

    # Create the data folder if it does not exist
    data_folder = Path("projects/mp2/data")
    data_folder.mkdir(parents=True, exist_ok=True)

    # Name the CSV file
    file_path = data_folder / "wellesley_forecast.csv"

    # Save the forecast records
    with open(file_path, "w", newline="") as _file:
        writer = csv.DictWriter(
            _file,
            fieldnames=forecast[0].keys()
        )

        writer.writeheader()
        writer.writerows(forecast)

    print(f"Saved {len(forecast)} weather records to {file_path}")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #5. The Answer
    """)
    return


@app.cell
def _(days):
    #displaying table 
    print(f"{'Date':<15} {'High (F)':<12} {'Low (F)':<12} {'Rain (%)':<12} {'Wind (mph)':<12} {'Passes':<10}")
    print("-" * 75)

    for _record in days:
        print(
            f"{_record['Date']:<15} "
            f"{_record['High (F)']:<12} "
            f"{_record['Low (F)']:<12} "
            f"{_record['Rain (%)']:<12} "
            f"{_record['Wind (mph)']:<12} "
            f"{str(_record['Passes']):<10}"
        )

    return


@app.cell
def _(days, place, state):
    #best day recommendation 
    passing_days = []

    for _candidate in days:
        if _candidate["Passes"]:
            passing_days.append(_candidate)

    if passing_days:
        best_day = min(
            passing_days,
            key=lambda record: (
                record["Rain (%)"],
                record["Wind (mph)"]
            )
        )

        print(
            f"The best day for an outdoor event in {place}, {state} "
            f"is {best_day['Date']} because it meets all weather "
            f"requirements, with a {best_day['Rain (%)']}% chance "
            f"of rain and wind of {best_day['Wind (mph)']} mph."
        )

    elif days:
        best_day = min(
            days,
            key=lambda record: record["Broken Rules"]
        )

        print(
            f"No days meet all weather requirements in {place}, {state}. "
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
    #6. How I know these numbers are right
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    These checks are used to confirm the results. First I am comparing the number of weather records returned to the number of days listed in my final table, they should both show 7 records.

    Second, I compared the first day weather conditions to the established requirments. This checked the temperature, precipitation, and wind speed to the pass/fail results in the table. These calculations should also agree and therefore confirm that the weather requirments were correcltly applied.
    """)
    return


@app.cell
def _(days, forecast):
    forecast_count = len(forecast)
    table_count = len(days)

    print(f"Forecast records: {forecast_count}")
    print(f"Table records: {table_count}")

    if forecast_count == table_count == 7:
        print("Check passed: All 7 days are included.")
    else:
        print("Check failed: The record counts do not match.")

    return


@app.cell
def _(
    days,
    forecast,
    highest_high_f,
    lowest_high_f,
    max_rain_chance,
    max_wind_mph,
):
    check_day = forecast[0]

    check_high = (
        lowest_high_f <= check_day["High (F)"]
        <= highest_high_f
    )

    check_rain = check_day["Rain (%)"] <= max_rain_chance

    check_wind = check_day["Wind (mph)"] <= max_wind_mph

    independent_result = check_high and check_rain and check_wind

    table_result = days[0]["Passes"]

    print(f"Date checked: {check_day['Date']}")
    print(f"Independent result: {independent_result}")
    print(f"Table result: {table_result}")

    if independent_result == table_result:
        print("Check passed: Both methods agree.")
    else:
        print("Check failed: Results do not match.")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #7. Working with the Agent
    One recommendation that I did not accept as is was the use of a "mo.ui.table" command. I did not recognize this command and also professor advised us to use print statements to create the table. I recognized this suggestion did not align and made the changes to reflect the profesors requirments of f strings and for loops. The new table results from section 5 prove that the print code is working correctly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #8. Reading it back
    The first function the agent assisted me with was get_coordinates() function. This function takes both the town and state names as inputs and relates them to the open meteo websie to find the location. The function then shows the matching MA town and its coordinates.

    I needed help understanding the line data.get("results,[]) as the extra paraenthases confused me. I learned that this searches for the results in the API response and also returns an empty list in the case of no results. This helped me clarify the code and understand that the code would not error if there were no results found.

    The second function the agent helped me create was a similar get_forecast() function. This function takes the coordinates of the get_coordinates() function and uses them to get the weather forecast from the open meteo website. The forecast function returns the 7 records including dates, temperature ranges, rain possibilities, and high wind speed. I had to ask about the zip function, I recognized this and knew I had learned this before but forgotton its function. The agent helped me understand that it combines multiple lists of data into one list to be stored together in one record.

    I will be changing the tool by changing the town input. I expect the coordinates to change and therefore the 7 day forecast will change from the origional town to the new town. I will change it from Wellesley to Wayland, and it will likely change the best day, unless these two locations share similar weather.

    The results of changing the input were a recommended day in Wayland of 10/28/2026 with a weather  forecast of 0% chance of rain and wind of 4.9 mph. The recommended day is the same as Wellesley, but the weather report is slightly different with a 0% chance of rain and wind of 5.2 mph. My prediction was correct as the weather report changed to fit the new town, despite the same day recommendation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #9. Going Further
    Score the weather on a ranking of 10
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For this section I chose to go further on the origional pass fail weather evaluation and develop the score ranking. I started by creating a new function, score_weather(), this function assigns points based on the weather conditons such as rain, wind, and temperature. Four points are assigned to temperature and precipitation while two are assigned to wind speed, as I think that wind speed is less important of a deciding factor.

    Next I used this to calculate a score for each of the seven days and the results are shown in a table. This format allowed me to easily compare weather conditions, especially with the addition of the identified highest scoring day. The highest scoring day was decided using additional factors such as the precipitation and wind speed.
    """)
    return


@app.cell
def _(highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph):
    #calclulates score
    def score_weather(high, rain, wind):
        score = 0

        if lowest_high_f <= high <= highest_high_f:
            score += 4

        if rain <= max_rain_chance:
            score += 4

        if wind <= max_wind_mph:
            score += 2

        return score

    return (score_weather,)


@app.cell
def _(days, score_weather):
    scored_days = []

    for _scored_day in days:
        _score = score_weather(
            _scored_day["High (F)"],
            _scored_day["Rain (%)"],
            _scored_day["Wind (mph)"]
        )

        scored_days.append({
            "Date": _scored_day["Date"],
            "High (F)": _scored_day["High (F)"],
            "Rain (%)": _scored_day["Rain (%)"],
            "Wind (mph)": _scored_day["Wind (mph)"],
            "Score": _score
        })
    return (scored_days,)


@app.cell
def _(scored_days):

    print(f"{'Date':<15} {'High (F)':<12} {'Rain (%)':<12} {'Wind (mph)':<12} {'Score':<10}")
    print("-" * 65)

    for _scored_record in scored_days:
        print(
            f"{_scored_record['Date']:<15} "
            f"{_scored_record['High (F)']:<12} "
            f"{_scored_record['Rain (%)']:<12} "
            f"{_scored_record['Wind (mph)']:<12} "
            f"{str(_scored_record['Score']) + '/10':<10}"
        )
    return


@app.cell
def _(place, scored_days, state):
    if scored_days:
        best_scored_day = max(
            scored_days,
            key=lambda record: (
                record["Score"],
                -record["Rain (%)"],
                -record["Wind (mph)"]
            )
        )

        print(
            f"The highest-scoring day for an outdoor event in "
            f"{place}, {state} is {best_scored_day['Date']} "
            f"with a weather score of {best_scored_day['Score']}/10, "
            f"a {best_scored_day['Rain (%)']}% chance of rain, "
            f"and wind of {best_scored_day['Wind (mph)']} mph."
        )
    else:
        print("No scored forecast days available.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #10. Time Spent
    4
    """)
    return


if __name__ == "__main__":
    app.run()

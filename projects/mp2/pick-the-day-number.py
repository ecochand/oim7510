import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #section 1: question C "Pick the day" A student club is planning an outdoor event somewhere in Massachusetts in the next week and needs to pick the day. The organizer wants a table of the next seven days, today included, whether each day meets the club's rules, and the best day, for whatever town they type in.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #section 2 my plan
    My plan is to collect the desired town in Massachusetts from the code user. Then find the towns location using the open meteo interface. Next I will retrive the weather data for multiple days that the event could be hosted, as it is an outdoor event. Next a table will present these results to the user to analyze and the code will also present a recommendation of which day is best.
    """)
    return


@app.cell
def _():
    place = "Wellesley"
    state = "Massachusetts"
    lowest_high_f = 55
    highest_high_f = 80
    max_rain_chance = 30
    max_wind_mph = 15
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

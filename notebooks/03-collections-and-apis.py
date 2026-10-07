# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "requests",
# ]
# ///
"""Collections and APIs.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Collections and APIs

    This session starts in last week's notebook, `02-lists-and-records.py`, with sections 4 to 6. This notebook picks up after them with the rest of what a dictionary can do, then tuples and sets, then how to choose between them, and then data that comes from a server.

    | | |
    |---|---|
    | ✏️ | Your turn. Add cells with the **+** button |
    | 🚀 | This week's work |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Work with your agent the same way as in notebook 2.** Try it yourself first, or write the steps in words. Then ask your agent, ask it to explain any line you could not have written, and ask which concepts its answer used.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Before section 5**, install `requests` once. Leave marimo running, open a second Terminal with the **+** in VS Code's Terminal panel, and run:

    ```
    uv add requests
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. More on Dictionaries

    Last week you read one field out of a record. A dictionary can also be changed after it is made: a value replaced, a key added. Run the cell below and read what the quote holds at the end.
    """)
    return


@app.cell
def _():
    goog_quote = {"Symbol": "GOOG", "Price": 131.36}
    goog_quote["Price"] = 133.10
    goog_quote["Currency"] = "USD"
    goog_quote
    return (goog_quote,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Asking before you read

    `goog_quote["Volume"]` would stop with a `KeyError`, because there is no such key. The first way to ask: `in` answers `True` or `False`.
    """)
    return


@app.cell
def _(goog_quote):
    "Currency" in goog_quote
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The second way: `.get()` gives `None` when the key is missing, or the fallback you hand it as a second value.
    """)
    return


@app.cell
def _(goog_quote):
    goog_quote.get("Volume", 0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading every field

    `.items()` hands you each key together with its value, and the loop takes them as two names. Section 2 explains why two names on the left work.

    **The underscore in `_field` and `_value` keeps those names inside this one cell.** Without it they would belong to the whole notebook, and a cell of your own could not use `field` or `value` again.
    """)
    return


@app.cell
def _(goog_quote):
    quote_lines = []
    for _field, _value in goog_quote.items():
        quote_lines.append(f"{_field}: {_value}")
    quote_lines
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Counting with a dictionary

    A week of order statuses. The dictionary starts empty, and each status either gets its first count or adds one to the count it already has. `.get(_status, 0)` is what makes the first time work.
    """)
    return


@app.cell
def _():
    week_statuses = ["shipped", "pending", "shipped", "cancelled", "shipped", "shipped", "pending"]

    status_counts = {}
    for _status in week_statuses:
        status_counts[_status] = status_counts.get(_status, 0) + 1

    status_counts
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Your written answers

    Several questions below ask for a sentence. This cell is where they go. Click into it, write under the letter, and press `Ctrl+Enter` (Windows) or `Cmd+Enter` (macOS).

    **B ·** france, germany, usa, and brazil


    **C ·**

    **D ·**

    **G ·**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ A · Closing prices

    Four closing prices, keyed by ticker. Add a cell for each question.

    1. What was the price of `AAPL`?
    2. Ask for `TSLA` with square brackets, read the error, then ask again in a way that gives `None`.
    3. Which tickers closed above $200? Build them into a list.
    4. Which ticker closed highest? Keep the highest price seen so far in a loop, and the ticker that goes with it.

    *Check yourself: 260.81 · `KeyError: 'TSLA'`, then `None` · `['AAPL', 'MSFT', 'GOOG']` · `MSFT`.*

    **Going further.** Every price goes up 10%. Build a new dictionary with the new prices and leave `closing_prices` as it was.
    """)
    return


@app.cell
def _():
    closing_prices = {"AAPL": 260.81, "NVDA": 186.00, "MSFT": 404.88, "GOOG": 308.42}
    closing_prices
    return (closing_prices,)


@app.cell
def _(closing_prices):
    closing_prices["AAPL"]
    return


@app.cell
def _(closing_prices):
    print(closing_prices.get("TSLA"))
    return


@app.cell
def _(closing_prices):
    above_200 = []
    for ticker, price in closing_prices.items():
            if price > 200:
                    above_200.append(ticker)
    above_200
    return


@app.cell
def _(closing_prices):
    highest_price = 0
    highest_ticker = None
    for ticker_4, price_4 in closing_prices.items():
            if price_4 > highest_price: 
                highest_price = price_4
                highest_ticker = ticker_4

    highest_ticker
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ B · Orders by country

    The countries the 30 orders in notebook 2 shipped to, in the same order.

    1. **Add a cell** that counts the orders to each country, the way `status_counts` counts statuses above.
    2. **In the written answers cell**, answer: which country or countries had the most orders?

    *Check yourself: France 4, Venezuela 3, Argentina 1, and 12 countries in all.*
    """)
    return


@app.cell
def _():
    ship_countries = [
        "France", "Germany", "Brazil", "France", "Belgium", "Brazil", "Switzerland",
        "Switzerland", "Brazil", "Venezuela", "Austria", "Mexico", "Germany", "Brazil",
        "USA", "Austria", "Sweden", "France", "Finland", "Germany", "Venezuela", "USA",
        "Finland", "USA", "USA", "Germany", "France", "Austria", "Argentina", "Venezuela",
    ]
    len(ship_countries)
    return (ship_countries,)


@app.cell
def _(ship_countries):
    country_counts = {}

    for country in ship_countries: 
            if country in country_counts:
                    country_counts[country]+= 1
            else: 
                    country_counts[country] = 1
    country_counts
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. Tuples

    A tuple holds a few values in order, like a list, and **cannot be changed after it is made**. It suits one thing with several parts: a single holding is a ticker, a number of shares and a purchase price.
    """)
    return


@app.cell
def _():
    first_holding = ("GOOG", 100, 131.36)
    first_holding[0], len(first_holding)
    return (first_holding,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **A tuple refuses to change.** `first_holding[1] = 75` stops with:

    ```
    TypeError: 'tuple' object does not support item assignment
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Unpacking

    Three names on the left take the three parts in order, which reads better than `first_holding[1] * first_holding[2]`.
    """)
    return


@app.cell
def _(first_holding):
    goog_symbol, goog_shares, goog_price = first_holding
    f"{goog_symbol} cost ${goog_shares * goog_price:,.2f}"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The count has to match. Two names for three parts stops with:

    ```
    ValueError: too many values to unpack (expected 2, got 3)
    ```

    When you want only the first part, `*_` takes the rest and throws it away: `first_symbol, *_ = first_holding`.

    This is also what `for _field, _value in goog_quote.items():` did in section 1. Each item is a tuple of two, unpacked into two names.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A function can hand back a tuple

    250 units, packed 12 to a case. `divmod` gives the full cases and what is left over, as one tuple.
    """)
    return


@app.cell
def _():
    divmod(250, 12)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A tuple can be a key

    The market closes on fixed dates, and a date is a month and a day. A tuple can be a dictionary key because it cannot change. A list cannot:

    ```
    TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
    ```
    """)
    return


@app.cell
def _():
    market_holidays = {
        (1, 1): "New Year's Day",
        (7, 4): "Independence Day",
        (12, 25): "Christmas Day",
    }
    market_holidays[(7, 4)]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. Sets

    A set holds each value once and keeps no order. It answers two questions well: which distinct values are there, and is this one among them.

    A client traded these tickers this week, some of them more than once.
    """)
    return


@app.cell
def _():
    client_trades = ["MSFT", "AAPL", "GOOG", "MSFT", "GOOG", "TSLA", "MSFT"]
    traded_tickers = set(client_trades)
    len(client_trades), len(traded_tickers), sorted(traded_tickers)
    return (traded_tickers,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `"IBM" in traded_tickers` is `False`. A set has no positions, so `traded_tickers[0]` stops with `TypeError: 'set' object is not subscriptable`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two sets combine three ways. Compare the client's tickers with the six in the portfolio:

    | | | |
    |---|---|---|
    | `&` | in both | `{'AAPL', 'GOOG', 'MSFT', 'TSLA'}` |
    | `-` | in the first and not the second | `{'AMZN', 'NVDA'}` |
    | `\|` | in either | all six |
    """)
    return


@app.cell
def _(traded_tickers):
    portfolio_tickers = {"AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "TSLA"}
    sorted(portfolio_tickers & traded_tickers), sorted(portfolio_tickers - traded_tickers)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4. Choosing a Data Structure

    | | read by | can change | keeps each value |
    |---|---|---|---|
    | **list** | position | yes | as often as it appears |
    | **tuple** | position | no | as often as it appears |
    | **dictionary** | key | yes | keys once each |
    | **set** | membership only | yes | once |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Four questions, asked in order, from [Python §19](/handbooks/python/02-collections/#19-choosing-a-data-structure):

    1. **Are you only asking whether you have seen a value before?** A set. Stop here.
    2. **Is it one thing with named parts?** A dictionary. If the parts must never change, a tuple.
    3. **Is it many of the same thing?** A list.
    4. **Does each of those things have named parts?** Then a list of dictionaries, which is a table.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ C · Which structure

    **In the written answers cell**, name the structure for each, with one reason:

    1. The lines on one order, which the customer can add to, remove from and reorder
    2. Every customer who has ordered from you this year, each once
    3. The units sold of each product, looked up by product name
    4. One shipment's carrier, tracking number and ship date, which must not change once recorded
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. list : because order matters
    2. set : want unique names
    3. dictionary
    4. tuple :
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ D · The portfolio again

    Notebook 2 held the six holdings as a list of dictionaries. Here they are as a list of tuples, one holding per tuple.

    1. **By hand, no agent.** In the written answers cell, state which of the two shapes you would rather work with for this question, and why.
    2. **Add a cell** that computes what it costs to buy the whole portfolio. Unpack each holding into three names in the `for` line, and start each name with an underscore: `for _symbol, _shares, _price in holdings:`.
    3. **Then ask your agent** for its version, and ask it to explain the line you would not have written.

    *Check yourself: $116,302.70, the same as notebook 2.*

    **Going further.** Which holding cost the most? Build a dictionary from ticker to cost, then find the largest. *TSLA, $38,355.00.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **similar to mini project one
    """)
    return


@app.cell
def _():
    holdings = [
        ("AAPL", 100, 173.93),
        ("MSFT", 50, 319.53),
        ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33),
        ("NVDA", 20, 410.17),
        ("TSLA", 150, 255.70),
    ]
    holdings
    return (holdings,)


@app.cell
def _(holdings):
    total_cost = 0 
    #use a for loop to iterate to get the shares and price of every stock and then calculate the sub total, adding it to total cost 
    for stock in holdings: 
            print(type(stock))
            shares = stock[1]
            price = stock[2]
            subtotal = shares * price 
            total_cost += subtotal 

    total_cost
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    total_cost = 0
    for _symbol, _shares, _price in holdings:
        subtotal = _shares * _price
        total_cost += subtotal
    total_cost
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Advanced · A year of trades.** A client made the trades below this year, one tuple per trade: date, ticker, `"buy"` or `"sell"`, shares, price. When the client sells, which of the shares bought earlier were the ones sold? The usual rule is **first in, first out**: a sale uses up the oldest shares first. Selling 120 AAPL on April 15 uses the 100 bought in January, then 20 of the 50 bought in March.
    >
    > 1. **By hand, no agent.** In the written answers cell, write the algorithm in words: what you keep for each ticker, and what happens to it on a sale.
    > 2. **Then work it out with your agent**, and keep going until you can explain every line.
    > 3. Find the gain on each sale, the total, and the shares left.
    >
    > *Check yourself: gains of $7,900.00 in all, $6,700.00 on AAPL and $1,200.00 on MSFT. Left: 20 AAPL bought at $240.00, and 10 MSFT at $380.00.*
    >
    > **Going further.** Work it out again with **average cost**, where a sale uses the average price of every share held. The total changes. Which rule would the client rather report this year, and why?
    """)
    return


@app.cell
def _():
    year_trades = [
        ("2026-01-05", "AAPL", "buy", 100, 180.00),
        ("2026-02-10", "MSFT", "buy", 40, 400.00),
        ("2026-03-02", "AAPL", "buy", 50, 210.00),
        ("2026-04-15", "AAPL", "sell", 120, 230.00),
        ("2026-05-20", "MSFT", "buy", 20, 380.00),
        ("2026-06-08", "MSFT", "sell", 50, 420.00),
        ("2026-07-01", "AAPL", "buy", 30, 240.00),
        ("2026-08-12", "AAPL", "sell", 40, 250.00),
    ]
    year_trades
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 5. Asking a Server

    An **API** is a web address that answers with data. Open-Meteo is a free weather service that needs no key and no sign-up.
    """)
    return


@app.cell
def _():
    import requests

    return (requests,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The address below asks for the current temperature and wind at Babson's coordinates. `requests.get` sends the request, and `timeout=10` gives up after 10 seconds, so a server that never answers cannot hang your notebook.
    """)
    return


@app.cell
def _(requests):
    babson_url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=42.2987&longitude=-71.2595"
        "&current=temperature_2m,wind_speed_10m"
        "&temperature_unit=fahrenheit&wind_speed_unit=mph"
        "&timezone=America/New_York"
    )
    print(babson_url)
    babson_reply = requests.get(babson_url, timeout=10)
    babson_reply.status_code
    return (babson_reply,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **200** means the server understood the request and answered it. `.json()` turns what it sent into Python, and what comes back is a dictionary.
    """)
    return


@app.cell
def _(babson_reply):
    babson_weather = babson_reply.json()
    babson_weather
    return (babson_weather,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some of its values are dictionaries too. `["current"]` picks the inner dictionary and `["temperature_2m"]` picks one field out of it, the same two steps as `orders[0]["ShipCountry"]` last week.
    """)
    return


@app.cell
def _(babson_weather):
    babson_weather["current"]["temperature_2m"]
    return


@app.cell
def _(babson_weather):
    babson_weather["current"]["wind_speed_10m"]
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Read what came back before you trust it.**

    - **The units are in `current_units`.** Leave `wind_speed_unit=mph` out of the address and the wind arrives in km/h beside a temperature in °F.
    - **The coordinates are not the ones you sent.** Compare `latitude` and `longitude` in the reply with the address. The service answers for the nearest point on its own grid.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## When the request is wrong

    A latitude of 422 does not exist. The server answers **400**, which means *your request was wrong*, and its reply says why.
    """)
    return


@app.cell
def _(requests):
    bad_latitude_reply = requests.get(
        "https://api.open-meteo.com/v1/forecast?latitude=422&longitude=-71.2595&current=temperature_2m",
        timeout=10,
    )
    bad_latitude_reply.status_code, bad_latitude_reply.json()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A status code is not an answer

    Open-Meteo also finds places by name. Search for a misspelled town and read both the status and the reply.
    """)
    return


@app.cell
def _(requests):
    misspelled_reply = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=Wellesley&count=1",
        timeout=10,
    )
    misspelled_reply.status_code, misspelled_reply.json()
    return (misspelled_reply,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **200, and nothing inside.** A correct spelling returns a `results` key holding a list of places. This reply has no `results` key at all, so `misspelled_reply.json()["results"]` stops with a `KeyError`. `.get()` from section 1 asks safely:
    """)
    return


@app.cell
def _(misspelled_reply):
    misspelled_reply.json().get("results") is None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Status | What it means |
    |---|---|
    | **200** | the server understood you and answered |
    | **400** | your request was wrong, and the reply usually says how |
    | **404** | there is nothing at that address |
    | **429** | too many requests; wait before asking again |
    | **500** | the server broke |

    **The status code tells you whether the server understood the request. Whether you got an answer is in the reply**, and you have to read it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 6. ✏️ Your Turn

    **E · The wind in a sentence.** Add a cell that takes the wind speed and its unit out of `babson_weather` and puts both into one sentence with an f-string. *Check yourself: the unit reads `mp/h`, which is how this service writes miles per hour.*
    """)
    return


@app.cell
def _(babson_weather):
    wind_speed = babson_weather["current"]["wind_speed_10m"]
    wind_unit = babson_weather["current_units"]["wind_speed_10m"]
    f"The wind speed is {wind_speed} {wind_unit}."
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **F · Another town.** Search for `Wellesley` the way the misspelled search did, with the correct spelling. Take the first place out of `results`, then its `latitude`, `longitude` and `admin1`. *Check yourself: latitude 42.29649, in Massachusetts.*
    """)
    return


@app.cell
def _(requests):
    wellesley_reply = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=Wellesley&count=1",
        timeout=10,
    )
    wellesley_data = wellesley_reply.json()

    first_place = wellesley_data["results"][0]

    latitude = first_place["latitude"]
    longitude = first_place["longitude"]
    admin1 = first_place["admin1"]

    latitude, longitude, admin1
    return latitude, longitude


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **G · The first result.** Search for `Babson Park` and look at the first place in `results`. In the written answers cell, answer under **G**: which state is it in, and what would code that always takes `[0]` have done with it?

    **Going further.** Use F's coordinates to ask for Wellesley's current temperature. Build the address with an f-string, so that changing the town changes the forecast.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    G. it is in florida, code [0] chooses the first result, which in this example caused an issue
    """)
    return


@app.cell
def _(latitude, longitude, requests):
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m"

    wellesley_weather_reply = requests.get(weather_url, timeout=10)

    wellesley_weather = wellesley_weather_reply.json()

    wellesley_weather["current"]["temperature_2m"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Advanced · H · A week of forecasts.** Add `&daily=temperature_2m_max,temperature_2m_min` to the Babson address. The `daily` part of the reply holds three lists side by side: dates, highs and lows, matched by position. [Python §19](/handbooks/python/02-collections/#19-choosing-a-data-structure) shows how that shape goes wrong. Turn it into a list of dictionaries, one per day, each with a date, a high and a low.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Advanced · I · A second API.** Kraken, a cryptocurrency exchange, publishes prices with no key: `https://api.kraken.com/0/public/Ticker?pair=XBTUSD`. Request it, then change the pair to `XBTUSX`. Compare the status code and the reply with Open-Meteo's misspelled search. Both answer 200 to a request that failed, and each shows the failure in its own way.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🚀 This Week's Work

    1. **Notebook 2, sections 4 to 6**, including your *One row is...* sentence
    2. **Everything above in this notebook** that is not marked **Advanced**, in your repository under `notebooks/`
    3. **`AGENTS.md`** in the top folder of your repository, committed
    4. **Commit as you go**, with messages that state what changed, and push before you stop
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What you can do now:**

    - [ ] I can change a dictionary, and read from it safely when a key may be missing
    - [ ] I can count with a dictionary
    - [ ] I can unpack a tuple into names
    - [ ] I can find the distinct values in a list, and what two lists share
    - [ ] I can choose between a list, a tuple, a dictionary and a set, and state why
    - [ ] I can request data from an API and read both its status code and its reply
    """)
    return


if __name__ == "__main__":
    app.run()

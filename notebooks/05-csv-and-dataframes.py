# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo[sql]",
#     "altair",
#     "polars",
#     "requests",
# ]
# ///
"""From a CSV file to a dataframe.
"""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import csv

    import altair as alt
    import polars as pl
    import requests

    return alt, csv, pl, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # From a CSV File to a Dataframe

    In this notebook you save the towns you read from the course API last week to a file, read them back, and answer one question about them three ways: with a loop, in polars and in SQL. Then you chart the answer.

    | | |
    |---|---|
    | ✏️ | Your turn. Add cells with the **+** button |
    | 🚀 | This week's work |

    For a written answer, add a cell under the question, open the cell's **⋯** menu and choose **Convert to Markdown**.

    Every ✏️ is part of this week's work. The **Going further** at the end of an exercise is optional; try it once the rest is done.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Work with your agent the same way as in notebook 4.** Try it yourself first, or write the steps in words. Then ask your agent, ask it to explain any line you could not have written, and ask which concepts its answer used. Exercise A is by hand.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. Saving What You Fetched

    The towns you read last week lived in memory, and they were gone when the notebook stopped. An API also changes. The shop takes new orders every day, and the tax figures change every year. **Save a copy to a file**, and the same analysis runs again on the same data, without a network, and anybody can open it in a spreadsheet. [Mini Project 2](https://oim7510.github.io/assignments/mini-project-2/) asks you to do the same.

    **CSV** is the plainest table a file can hold: one line per record, commas between the values, and a first line that names the columns.

    First, collect every town. `/ma/counties` lists the 14 counties.
    """)
    return


@app.cell
def _(requests):
    ma_counties = requests.get("https://oim.zhili.dev/ma/counties", timeout=10).json()
    ma_counties[0], len(ma_counties)
    return (ma_counties,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `get_towns` is the function from notebook 4, section 2, with one change: `per_page=100`, because the largest county has 60 towns and the server sends 50 to a page unless you ask for more. Called once per county, it collects every town in the state.
    """)
    return


@app.cell
def _(requests):
    def get_towns(county):
        towns_reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": county, "per_page": 100},
            timeout=10,
        )
        return towns_reply.json()["items"]

    return (get_towns,)


@app.cell
def _(get_towns, ma_counties):
    ma_towns = []
    for _county in ma_counties:
        for _town in get_towns(_county["name"]):
            ma_towns.append(_town)
    len(ma_towns)
    return (ma_towns,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Writing the file.** Python's `csv` module writes and reads CSV files, so you never put the commas in yourself. `csv.DictWriter` takes a list of dictionaries, the shape you already have:

    - `fieldnames` names the columns to keep, in order. Each town has 14 fields, and `extrasaction="ignore"` leaves out the ones not named.
    - `.writeheader()` writes the first line, and `.writerows()` writes one line per town.
    - `open(path, "w")` opens the file for writing, and `with` closes it when the block ends. The empty `newline` setting is what the `csv` module asks for, so that lines end the same way on every computer.

    A data file goes in the `data` folder, which sits in the root folder of your repository, one folder up from this notebook.
    """)
    return


@app.cell
def _(csv, ma_towns, mo):
    csv_columns = [
        "name",
        "county",
        "population",
        "income_per_capita_dollars",
        "average_single_family_value_dollars",
        "average_single_family_bill_dollars",
    ]

    ma_towns_csv = mo.notebook_dir().parent / "data" / "ma-towns.csv"
    ma_towns_csv.parent.mkdir(exist_ok=True)

    with open(ma_towns_csv, "w", newline="", encoding="utf-8") as _file:
        _writer = csv.DictWriter(_file, fieldnames=csv_columns, extrasaction="ignore")
        _writer.writeheader()
        _writer.writerows(ma_towns)

    ma_towns_csv.name
    return (ma_towns_csv,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Open it.** In VS Code's Explorer, the `data` folder now sits beside the `notebooks` folder, and `ma-towns.csv` is inside it. Click it: the table is plain text, one town per line.

    **Reading it back.** `csv.DictReader` reads one line at a time and turns each into a dictionary, with the header's names as keys. `list(...)` collects them all, and you are back to a list of records, the shape the API sent.
    """)
    return


@app.cell
def _(csv, ma_towns_csv):
    with open(ma_towns_csv, newline="", encoding="utf-8") as _file:
        towns_from_file = list(csv.DictReader(_file))
    len(towns_from_file), towns_from_file[0]
    return (towns_from_file,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Every value the `csv` module reads is text.** Look at the population: `'49831'`, in quotes. A CSV file has no types, only characters, so the module gives you strings, and adding 1 to one raises a `TypeError`. `int()` turns it back into a number, or `float()` when it has a decimal point. The file does not record which columns were numbers, so you convert them yourself.
    """)
    return


@app.cell
def _(towns_from_file):
    towns_from_file[0]["population"], int(towns_from_file[0]["population"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ A · By Hand

    **No agent for this one**, and no code completion either. When the editor suggests code in grey as you type, press `Esc` and keep typing your own.

    `average_single_family_value_dollars` is the state's figure for what a single-family home in the town is worth on average, as the town assesses it for tax. Call a town a **million-dollar town** when that figure is $1,000,000 or more. Across the state the middle town is near $586,000.

    1. How many million-dollar towns are there, and which county has the most of them? Use `towns_from_file`, a `for` loop, `int()`, and a dictionary that counts, as in notebook 3. *Check yourself: 53 towns, and Middlesex has the most, with 14.*
    2. Which town has the fewest people, and which has the most? Loop over `towns_from_file` and keep the smallest and the largest you have seen so far, the way `find_largest` did in notebook 4. *Check yourself: Gosnold, with 62 people, and Boston, with 673,458.*

    **Going further.** Find the town with the most expensive average home in each county.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. Describe What You Want

    Your loops in A spelled out **how**: go through every town, convert, compare, add one or keep the smallest. That took a dozen lines, and a reader has to run them in their head to know what they answer. **polars** lets you describe **what** you want instead.

    `pl.read_csv` reads the same file into a **DataFrame**: a table with named columns. It is your list of records shown as a table, each row a record and each column a key, and polars has already turned the numbers into numbers.
    """)
    return


@app.cell
def _(ma_towns_csv, pl):
    town_table = pl.read_csv(ma_towns_csv)
    town_table
    return (town_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `.schema` lists each column with its type, the step you did with `int()`. `.shape` is the number of rows and columns.
    """)
    return


@app.cell
def _(town_table):
    town_table.schema, town_table.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **A's second step in one line.** `.sort()` puts the rows in order of one column, smallest first, so the first row is the town with the fewest people. `descending=True` puts the largest first.
    """)
    return


@app.cell
def _(town_table):
    town_table.sort("population")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here is A's first step in polars. Read it as a sentence:

    - `.filter(...)` keeps the million-dollar towns. It is the `if` in your loop, applied to every row at once, and `pl.col(...)` names the column it reads.
    - `.group_by("county")` makes one group per county, and `.agg(pl.len())` counts the rows in each. It is your counting dictionary.
    - `.sort(..., descending=True)` puts the largest first.
    """)
    return


@app.cell
def _(pl, town_table):
    (
        town_table.filter(pl.col("average_single_family_value_dollars") >= 1_000_000)
        .group_by("county")
        .agg(pl.len().alias("towns"))
        .sort("towns", descending=True)
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **A count can mislead.** Middlesex has the most million-dollar towns, and it also has 54 towns, more than any county but Worcester. The fairer question is what share of each county's towns are million-dollar towns.

    - `pl.len()` counts all the towns in each county.
    - A comparison such as `pl.col(...) >= 1_000_000` is `True` or `False` for each town, and `.sum()` adds up the `True`s, which counts them.
    - `.with_columns()` adds a column computed from the others, here one count divided by the other.
    """)
    return


@app.cell
def _(pl, town_table):
    million_dollar_share = (
        town_table.group_by("county")
        .agg(
            pl.len().alias("towns"),
            (pl.col("average_single_family_value_dollars") >= 1_000_000)
            .sum()
            .alias("million_dollar_towns"),
        )
        .with_columns((pl.col("million_dollar_towns") / pl.col("towns")).alias("share"))
        .sort("share", descending=True)
    )
    million_dollar_share
    return (million_dollar_share,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The share tells a different story from the count. Every town in Dukes County, which is Martha's Vineyard and the Elizabeth Islands, and in Nantucket is a million-dollar town, and nearly half of Barnstable's, which is Cape Cod. Middlesex comes sixth.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ B · Check Against the Server

    1. Count every town per county with `town_table`, `.group_by()` and `.agg()`. The server counts them too, in `ma_counties`, and `pl.DataFrame(ma_counties)` turns that list of records into a table. Do the two agree? *Check yourself: Worcester 60, Middlesex 54, Essex 34, and all 14 agree.*
    2. Which five towns of more than 50,000 people have the highest average single-family bill? Use `.filter()`, `.sort()` and `.head()`. *Check yourself: Brookline, Newton, Cambridge, Somerville, Quincy.*

    **Going further.** Ask the towns a question of your own that needs `.filter()`, `.group_by()` and `.sort()` together.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. The Same Question in SQL

    **This is SQL, a second language, asking A's question once more.** SQL is how databases are asked questions, and from next week the course builds and queries a database. For now, read it; you will write SQL in the database sessions.

    Behind a SQL cell is DuckDB, a database that runs inside the same Python as your notebook. The data stays in your DataFrames. When the cell runs, DuckDB looks up the name in the `FROM` line, here `town_table`, among the notebook's variables and reads that DataFrame as a table. Its answer comes back as a DataFrame too.
    """)
    return


@app.cell
def _(mo, town_table):
    towns_over_threshold = mo.sql(
        f"""
        SELECT county, COUNT(*) AS towns
        FROM town_table
        WHERE average_single_family_value_dollars >= 1000000
        GROUP BY county
        ORDER BY towns DESC
        """
    )
    return (towns_over_threshold,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read it top to bottom: `SELECT` names the columns of the answer, `FROM` the table, `WHERE` keeps some rows, `GROUP BY` makes one group per county, `COUNT(*)` counts each group, and `ORDER BY ... DESC` puts the largest first. Like the polars version, it describes what you want and leaves the how to the computer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ C · Raise the Bar

    In the SQL cell, `1000000` is the bar a town's average home value has to reach. Before you change it to `2000000`, predict in a markdown cell under this question: which counties' counts can go down, and can any go up? Then make the same change in the polars cell that counts million-dollar towns, and run both. *Check yourself: both give Dukes, Middlesex and Norfolk 2 each and Nantucket 1, which is 7 towns.*

    **Going further.** Write a SQL query of your own on `town_table`, and check its answer in polars.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4. The First Chart

    Draw the share. `.plot.bar()` on a DataFrame draws one bar per row, with a library called **altair**. `alt.X()` and `alt.Y()` name each axis's column and give it a title a reader can understand, and `.properties(title=...)` states what the chart shows.

    - Putting the county on `y` lays the bars on their side, so every county's name reads across. `sort="-x"` puts the longest bar first.
    - `axis=alt.Axis(format="%")` writes a share of `0.25` as 25%.

    Wrap it in `mo.ui.altair_chart()`, which is how marimo shows an altair chart of any size.
    """)
    return


@app.cell
def _(alt, million_dollar_share, mo):
    million_dollar_chart = mo.ui.altair_chart(
        million_dollar_share.plot.bar(
            y=alt.Y("county", sort="-x", title="County"),
            x=alt.X(
                "share",
                title="Share of towns averaging $1,000,000 or more",
                axis=alt.Axis(format="%"),
            ),
        ).properties(title="Every town in Dukes and Nantucket averages $1 million or more")
    )
    million_dollar_chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `.plot.point()` and `.plot.line()` work the same way. matplotlib is another charting library, and you will meet it in other people's code; [Python §29](https://oim7510.github.io/handbooks/python/03-data/#29-a-chart-with-labeled-axes) shows one chart in each.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ D · A Chart of Your Own

    Choose a question one chart can answer, from the data you saved for Mini Project 2 or from `town_table`. Draw it with titled axes, and a title that states what it shows.

    *Check yourself: somebody who has not seen this notebook can say what each axis measures.*

    **Going further.** Color the bars or dots by a column with `color=`, and explain what the colors add.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🚀 This Week's Work

    1. **What is due is listed under *Before next session* in the post-class notes.** I post them on the session page after each class, with the sections we reached, and the checkpoint on Canvas lists the same items.
    2. **[Mini Project 2](https://oim7510.github.io/assignments/mini-project-2/)**, due Sunday 10/25
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Self-check:**

    - [ ] I can save a list of records to a CSV file and read it back with the `csv` module
    - [ ] I can explain why every value the `csv` module reads is text until I convert it
    - [ ] I can read a CSV into a DataFrame and ask it its shape and its column types
    - [ ] I can filter, sort and group a DataFrame
    - [ ] I can read a short SQL query and explain what it asks
    - [ ] I can make one chart from a DataFrame and title its axes
    """)
    return


if __name__ == "__main__":
    app.run()

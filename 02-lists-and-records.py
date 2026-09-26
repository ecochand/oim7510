# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Lists and records.

Shared by OIM7510 and OIM6301, and used in the session What one row means.

AUTHORING NOTES.

The session is mostly consolidation. Sections 1 to 3 are a second meeting with
what notebook 1 already ran, named this time, and the table there has 11 rows
after the f-string was added on 2026-09-21. Only two things are new, in sections
4 and 5: a record is read by name, and a list of records is a table. Section 6 is
the portfolio. Decided with Zhi on 2026-09-21, against the risk of carrying a room two
weeks into Python past its own footing.

The scaffold cell after section 1's table holds ten comment lines and nothing else, so
`marimo check` reports `empty-cells` on it. That warning is expected: the cell is where a
student writes their own example of each name, in class or at home, and it is the answer
this notebook gives to the seeded-empty-cell question from OIM6301's s02 debrief. Do not
delete it to quiet the lint.

**The drills in section 3 are language exercises, not analysis questions**, and
and five of the eight come from `internal/drafts/quiz-inventory.md`, whose
answers were run on Python 3.14: A19 (the elif that never runs), M10's
accumulator, M11 (append against extend, sort against sorted) and M12
(aliasing). An earlier draft asked business questions about freight and Zhi
rejected the shape: *这些都不像是 python 的题目*. A later one stated them as bare
`nums = [1, 2]`, which he rejected too: *不要生硬的出这些题，可以简单的给出有意义的
背景*. So each drill carries one line of context and its own data, and A to E are
required while F to H are marked. Every check value here was run on 2026-09-21.

The word **reduce** does not appear in student-facing text (Zhi, 2026-09-21): the
fourth move is "turn many into one number". Decision 29 keeps the term internally.

The thirty orders in section 4 are real rows of `data/northwind/orders.parquet`,
OrderID 10248 to 10274 plus the three unshipped orders 11008, 11019 and 11039.
Check values were computed off that parquet and re-run against this file's own
data on 2026-09-21: 827.00 total freight, 3 never shipped.

The portfolio in section 6 is the six holdings from `archive/25fall/slides/
2025fall/python.md` line 826, whose printed total is $116,302.70. Two levels of
one question: the required one is a list of records, which is inside tonight's
reach, and the marked one is Zhi's original, reading `portfolio.csv`. Reading a
file belongs to s07, so in the marked version the agent writes the code and the
student works the four steps. The notebook writes the CSV itself so that no one
loses the exercise to a path.

The four steps are Zhi's, 2026-09-21: write the approach by hand first, then let
the agent solve it, then have the agent explain every detail, then have the agent
set a similar problem.

The keys carry the database's own spelling (`OrderID`, `ShipCountry`), not Python
casing, because s05 onward meets the same columns in the real table.

`hide_code=True` on every markdown-only cell, and every such cell is one call and
nothing else, or its source leaks onto the page.

It imports nothing but marimo, except the one cell in section 6 that writes the
CSV, which uses pathlib from the standard library. No cell in this file raises.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lists and Records

    Sections 1 and 2 ran in your notebook last week, and here they get their names.
    Section 3 practises them. **Sections 4 and 5 are the new material.**

    | | |
    |---|---|
    | ✏️ | Your turn. Add cells with the **+** button |
    | 🚀 | This week's work |

    **How to work with your agent, in every ✏️ section.** The order matters, and it is the
    same order all term.

    1. **Try it yourself first.** If you cannot write the code, write the steps in words.
    2. **Then ask your agent**, and read what it gives you before you keep it.
    3. **If any line of its answer is unclear, ask it to explain that line.** Keep asking
       until you could write the same line tomorrow. An answer you cannot read is not an
       answer you can check.
    4. **Then ask which concepts its answer used**, and find those rows in the table
       below.

    **The course rules for your agent** are a block of text you paste once into marimo's
    **Settings > AI Features > Custom Rules**, and they make it do steps 3 and 4 without
    being asked. Download them from the course site, under Downloads. Nothing here is
    required.
    """)
    return


@app.cell(hide_code=True)
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. What You Already Have

    Every row ran in your notebook last week.

    | | The name for it | What it is for |
    |---|---|---|
    | `16.75` | a **value** | a single number, or a single piece of text |
    | `total = sum(charges)` | a **name**, and `=` is **assignment** | storing a value you will use again |
    | `16.75` against `"16.75"` | a **type**: number against text | deciding what can be done with a value. Arithmetic and sorting behave differently on each |
    | `f"${total:.2f}"` | an **f-string** | putting a value inside a sentence, to two decimal places |
    | `[16.75, 22.25, 25.00]` | a **list** | holding many values of one kind, in order |
    | `charges[0]` | an **index**, counting from zero | reading one item by its position |
    | `for charge in charges:` | a **loop**, once for each item | running the same lines once per item |
    | `if charge < 25:` | a **condition** | running lines only when a test is true |
    | `sum(charges)` | **many values into one number** | combining every item into a single result |
    | `sorted(charges, reverse=True)` | a **function**, and `reverse=True` is an **argument** | calling an operation somebody already wrote. The argument is what you hand it |
    | `NameError`, `IndexError`, `SyntaxError` | an **error** | Python stopping and reporting why. Read the last line first |
    """)
    return


@app.cell
def _():
    # Your own example of each name.

    # 1. value: 16.75
    # 2. name and assignment: total = sum(charges)
    # 3. type: 16.75
    # 4. list:[16.75, 22.25, 25.00]
    # 5. index: charges[0]
    # 6. loop: for charge in charges:
    # 7. condition: if charge < 25
    # 8. f-string:
    # 9. many into one number: sum(charges)
    # 10. function and argument: sorted(charges, reverse = True)
    # 11. error: NameError, IndexError, Syntax Error
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    total = sum(charges)
    16.75
    list:[16.75, 22.25, 25.00]
    index: charges[0]
    loop: for charge in charges:
    condition: if charge < 25
    f-string:
    many into one number: sum(charges)
    function and argument: sorted(charges, reverse = True)
    error: NameError, IndexError, Syntax Error
    """)
    return


@app.cell
def _():
    cost = float(input ("Enter the cost: "))
    tax = float(input("Enter tax: "))
    return cost, tax


@app.cell
def _(cost, tax):
    cost + tax
    return


@app.cell
def _(cost, tax):
    float(cost) + float(tax)
    return


@app.cell
def _(cost):
    total_cost = cost * 10
    total_cost
    return (total_cost,)


@app.cell
def _(total_cost):
    print(f'The total cost is ${total_cost:.2f}.')
    return


@app.cell
def _(cost):
    type(cost)
    return


@app.cell
def _():
    charges = [16.75, 22.25, 25.00, 100, 200, 300]
    return (charges,)


@app.cell
def _(charges):
    type(charges)
    return


@app.cell
def _(charges):
    charges[-3]
    return


@app.cell
def _(charges):
    charges[1 : 4]
    return


app._unparsable_cell(
    r"""
    i = 0 
    for whatever in charges: 
            i +=1
            print (f'round {i}')
            print (whatever)
            tax_ = whatever * 0.0625
            print(tax_)
            cost_ = whatever + tax_ 
            print(cost_)
            print(f'Pre-tax: ${whatever:.2f}, total: ${cost_:.2f}'
            print()
    """,
    name="_"
)


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. What You Do to a List

    Four things, and you have done all four already.

    | | on last week's five charges |
    |---|---|
    | **Take one out** | `charges[0]` |
    | **Keep some** | `for` with an `if` |
    | **Do the same to each** | `for charge in charges:` |
    | **Turn many into one number** | `sum(charges)`, or a running `total` |

    Tonight you will do them to records. In October you will do them to a table in
    pandas, and in November to a database table.
    """)
    return


@app.cell
def _(charges):
    for charge in charges: 
            tax_ = charge + charge *0.0625
            cost_ = charge + tax_
            print(f'Pre-tax: ${charge:.2f}, total: ${cost_:.2f}')
    return


@app.cell
def _(charges):
    #sum all the charges under $25
    s = 0
    for charge in charges:
        if charge < 25:
                s = s + charge
    print(f'Total charges below $25 is {s}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## In class

    Last week's five freight charges are below. Add cells under it and type these with me.

    ```python
    charges[0]
    charges[-1]
    charges[5]
    ```

    The third one fails on purpose. Then the loop, one line at a time:

    ```python
    total = 0
    for charge in charges:
        if charge < 25:
            total = total + charge
    total
    ```

    **Check yourself: 59.25.**
    """)
    return


@app.cell
def _(charges):
    charges[0]
    return


@app.cell
def _(charges):
    charges[-1]
    return


@app.cell
def _(charges):
    charges[5]
    return


@app.cell
def _():
    charges = [16.75, 22.25, 25.00, 20.25, 36.25]
    charges
    return (charges,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. ✏️ Your Turn

    Five short ones, each a small piece of code with something surprising in it. Every
    one already has its code in a cell, so there is nothing to copy.

    **How to work them**

    - **Run a cell:** click into it and press `Ctrl+Enter`, or `Cmd+Enter` on macOS.
    - **Add a cell:** hover between two cells and click the **+** button, or use the **+**
      at the bottom of the notebook.
    - **Write words instead of code:** add a cell, open its menu (the **⋮** at its right
      edge) and choose **Convert to Markdown cell**. Prose typed into a code cell turns
      the cell red and it stays broken until you convert it or delete it.
    - **`This variable is already defined in another cell`:** you are trying to give a name
      that already exists somewhere else in this notebook. Edit the cell that already has
      it, or pick a different name. marimo allows one definition per name in the whole
      file, which is what stops two cells from quietly disagreeing.
    - **If your number is not the one written under a question**, check your data before
      you check your code. Last week's Experiment 1 put 999.99 into the freight list on
      purpose and asked you to put it back.
    - **Stuck:** try it yourself first, then ask your agent and paste the error if there
      is one. Read its answer, ask it to explain any line you could not have written, and
      finish by asking which concepts it used. The four steps are at the top of this
      notebook.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Your written answers

    Four of the drills below ask for a sentence. This cell is where they go. Click into
    it, write under the letter, and press `Ctrl+Enter`. Code still goes in cells of your
    own, added with the **+** button.

    **A ·**

    **C ·**

    **D ·**

    **E ·**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A · The training scores

    A training program marks anyone at 90 or above as `A`, and anyone at 60 or above as
    `Pass`. The cell below is supposed to do that. It does not.

    1. **Run the cell below** and read what it printed for a score of 95.
    2. **Edit that same cell** so that 95 prints `A`, changing as little as you can. Then
       set `score` to 75, run it again, and confirm it still prints `Pass`.
    3. **Add a markdown cell** and answer in one sentence: when a score satisfies two of
       these tests at once, which one decides what gets printed?

    **Going further.** Extend the same cell so that anything below 60 prints `Fail`, then
    run 95, 75, 60 and 55 through it one at a time.

    *Expected: `Pass` before your change, `A` after it, and `Pass` again for 75.*
    """)
    return


@app.cell
def _():
    score = 75
    if score >= 90:
        print("A")

    elif score >=80:
        print("B")
    elif score >= 60:
        print("Pass")
    else: 
        print("Fail")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A: the first print will get printed when a score satisfies two
    """)
    return


@app.cell(hide_code=True)
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## B · A day of orders

    Five orders, each with the status it ended the day on. Counting how many are in one
    state is the most common thing anybody does to a column of a table, and here it is on
    a plain list first.

    1. **Add a cell** under the one below that counts how many of these orders shipped. A
       `for` loop with an `if` inside it and a counter that starts at zero will do it.
    2. **Add another cell** that counts how many did not ship.
    3. **Add a third cell** that prints the percentage that shipped. It is the count
       divided by `len(statuses)`, times 100.

    *Expected: 3, then 2, then 60.0.*
    """)
    return


@app.cell
def _():
    statuses = ["shipped", "pending", "shipped", "cancelled", "shipped"]
    statuses
    return (statuses,)


@app.cell
def _(statuses):
    shipped_count = 0
    not_shipped_count = 0

    for status in statuses:
        #print (status)
        if status == "shipped":
            shipped_count += 1
        else:
            not_shipped_count += 1

    percent_shipped = shipped_count / len(statuses) * 100

    print(f"{shipped_count} orders shipped")
    print(f"{not_shipped_count} orders not shipped")
    print(f"{percent_shipped:.2f}% of orders shipped")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## C · Adding items to an order

    An order has two lines on it. Somebody adds a stapler and some tape, so it should
    finish with four. Run the cell below and it has three.

    1. **Add a cell** that prints `order_lines[2]`, and read what came back. That one item
       is the whole problem.
    2. **Edit the cell below** so the order ends up with four separate lines. The method
       you need is not `append`; ask your agent for the one that adds several items at
       once, or search the handbook for it.
    3. **Add a markdown cell** and answer in one sentence: how many items does `append`
       add, whatever you hand it?

    *Expected: `['stapler', 'tape']` printed as one item, then a list of length 4.*
    """)
    return


@app.cell
def _():

    order_lines = ["notebook", "pen"]
    order_lines.append(["stapler", "tape"])
    len(order_lines)
    return


@app.cell
def _():
    order_lines = ["notebook", "pen"]
    order_lines.extend(["stapler", "tape"])
    len(order_lines)
    order_lines[2]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## D · Sorting the tickers

    Two ways to put a list in order. They look alike and they do different things, and
    the difference costs people real time later.

    1. **Run the cell below.** It prints three things: `sorted(tickers)`, then
       `tickers.sort()`, then `tickers` itself at the end.
    2. **Add a markdown cell** and answer in one sentence: why did `tickers.sort()` print
       `None`, when `sorted(tickers)` printed a list?
    3. **Add a cell** that prints the tickers largest first, without changing `tickers`
       again. One of the two ways above takes an extra argument that does this.

    *Expected: `['AAPL', 'MSFT', 'NVDA']`, then `None`, then largest first is
    `['NVDA', 'MSFT', 'AAPL']`.*
    """)
    return


@app.cell
def _():
    tickers = ["NVDA", "AAPL", "MSFT"]
    print(sorted(tickers))
    print(tickers.sort())
    tickers
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## E · The price list that changed by itself

    A shop builds its sale prices from its regular prices, adds one more sale price, and
    the regular price list comes out wrong. Nobody touched it.

    1. **Run the cell below** and read what `prices` holds at the end.
    2. **Add a cell** that prints `prices is sale_prices`. That is Python's way of asking
       whether two names refer to one single list, and it answers `True` or `False`.
    3. **Edit the cell below**, changing the second line to `sale_prices = prices[:]`, and
       run both again. `[:]` makes a copy of the list, where the first version made a
       second name for one list.
    4. **Add a markdown cell** and answer in one sentence: when would you want two names to
       refer to the same list on purpose?

    **Going further.** With `sale_prices = prices[:]` in place, take 10% off every sale
    price and leave `prices` untouched. A `for` loop over positions, or a new list built
    from the old one, will both do it.

    *Expected: `[12.5, 8.0, 19.99, 4.99]` and `True`, then `[12.5, 8.0, 19.99]` and
    `False`. Discounted: `[11.25, 7.2, 17.99, 4.49]`, with `prices` unchanged.*
    """)
    return


@app.cell
def _():
    prices = [12.50, 8.00, 19.99]
    sale_prices = prices
    sale_prices.append(4.99)
    prices
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## If You Finish

    Required of nobody. Take them in any order.

    > **Advanced · F · A quantity that arrived as text.** A web form sent its quantities
    > with quotes around them, so Python received text where you wanted numbers. Run the
    > cell below to see both behaviours side by side.
    >
    > 1. **Add a markdown cell** and answer in one sentence: what did `"100" + "50"` do,
    >    and why is that reasonable for text?
    > 2. **Add a cell** that adds the two form values as numbers and prints `150`. The
    >    function you need is named after the type you want.
    > 3. **Add another cell** and try that same conversion on `"100.5"`. Read the error,
    >    then get `100.5` a different way.
    """)
    return


@app.cell
def _():
    print("100" + "50")
    print(100 + 50)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Advanced · G · Off the end.** `charges` in section 2 holds last week's five freight
    > charges. This one has no cell of its own, because every line in it fails on
    > purpose and a notebook that raises on load is a nuisance.
    >
    > 1. **Add a cell**, type `charges[5]` in it and run it. **Add a markdown cell** saying
    >    why there is no item 5 when the list holds five charges.
    > 2. **Add a cell** that gets the last charge, in two different ways, without counting
    >    the items by hand.
    > 3. **Add a cell** and run `charges[-6]`. Say in markdown what happened and why.

    > **Advanced · H · A line for the operations team.** Using the counts you worked out in
    > B, **add a cell** that prints exactly `3 of 5 orders shipped`. Your code has to
    > compute both numbers. Then extend it so that it reads
    > `3 of 5 orders shipped (60%)`. An f-string is the short way to build a sentence out of
    > values, and it was section 5 of last week's notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4. A Record Is a Value With Fields

    A freight charge on its own does not say whose order it was, where it went, or
    whether it ever shipped. An order carries all of that. **This one is new.**
    """)
    return


@app.cell
def _():
    first_order = {
        "OrderID": 10248,
        "CustomerID": "VINET",
        "ShipCountry": "France",
        "ShipCity": "Reims",
        "OrderDate": "2016-07-04",
        "ShippedDate": "2016-07-16",
        "Freight": 16.75,
    }
    first_order
    return (first_order,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Taking one field out

    A list is read **by position**, `charges[0]`. A record is read **by name**.
    """)
    return


@app.cell
def _(first_order):
    first_order["ShipCountry"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ One of these fails

    ```python
    first_order["Freight"]
    first_order["freight"]
    first_order[0]
    ```

    Two of them fail, and both give the same kind of error. Add a cell and find out
    which, and what the message says. A `KeyError` names the key it could not find.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 5. A Table Is a List of Records

    One order is a record. A list of records is a table. **This one is new too.**

    Real rows from the warehouse this course uses all term: orders 10248 to 10274, plus
    three that were never shipped. The full table holds 16,282 of them.
    """)
    return


@app.cell
def _():
    orders = [
    {"OrderID": 10248, "CustomerID": "VINET", "ShipCountry": "France", "ShipCity": "Reims", "OrderDate": "2016-07-04", "ShippedDate": "2016-07-16", "Freight": 16.75},
    {"OrderID": 10249, "CustomerID": "TOMSP", "ShipCountry": "Germany", "ShipCity": "Münster", "OrderDate": "2016-07-05", "ShippedDate": "2016-07-10", "Freight": 22.25},
    {"OrderID": 10250, "CustomerID": "HANAR", "ShipCountry": "Brazil", "ShipCity": "Rio de Janeiro", "OrderDate": "2016-07-08", "ShippedDate": "2016-07-12", "Freight": 25.00},
    {"OrderID": 10251, "CustomerID": "VICTE", "ShipCountry": "France", "ShipCity": "Lyon", "OrderDate": "2016-07-08", "ShippedDate": "2016-07-15", "Freight": 20.25},
    {"OrderID": 10252, "CustomerID": "SUPRD", "ShipCountry": "Belgium", "ShipCity": "Charleroi", "OrderDate": "2016-07-09", "ShippedDate": "2016-07-11", "Freight": 36.25},
    {"OrderID": 10253, "CustomerID": "HANAR", "ShipCountry": "Brazil", "ShipCity": "Rio de Janeiro", "OrderDate": "2016-07-10", "ShippedDate": "2016-07-16", "Freight": 35.50},
    {"OrderID": 10254, "CustomerID": "CHOPS", "ShipCountry": "Switzerland", "ShipCity": "Bern", "OrderDate": "2016-07-11", "ShippedDate": "2016-07-23", "Freight": 24.25},
    {"OrderID": 10255, "CustomerID": "RICSU", "ShipCountry": "Switzerland", "ShipCity": "Genève", "OrderDate": "2016-07-12", "ShippedDate": "2016-07-15", "Freight": 37.50},
    {"OrderID": 10256, "CustomerID": "WELLI", "ShipCountry": "Brazil", "ShipCity": "Resende", "OrderDate": "2016-07-15", "ShippedDate": "2016-07-17", "Freight": 16.75},
    {"OrderID": 10257, "CustomerID": "HILAA", "ShipCountry": "Venezuela", "ShipCity": "San Cristóbal", "OrderDate": "2016-07-16", "ShippedDate": "2016-07-22", "Freight": 21.50},
    {"OrderID": 10258, "CustomerID": "ERNSH", "ShipCountry": "Austria", "ShipCity": "Graz", "OrderDate": "2016-07-17", "ShippedDate": "2016-07-23", "Freight": 40.25},
    {"OrderID": 10259, "CustomerID": "CENTC", "ShipCountry": "Mexico", "ShipCity": "México D.F.", "OrderDate": "2016-07-18", "ShippedDate": "2016-07-25", "Freight": 12.75},
    {"OrderID": 10260, "CustomerID": "OTTIK", "ShipCountry": "Germany", "ShipCity": "Köln", "OrderDate": "2016-07-19", "ShippedDate": "2016-07-29", "Freight": 35.50},
    {"OrderID": 10261, "CustomerID": "QUEDE", "ShipCountry": "Brazil", "ShipCity": "Rio de Janeiro", "OrderDate": "2016-07-19", "ShippedDate": "2016-07-30", "Freight": 20.00},
    {"OrderID": 10262, "CustomerID": "RATTC", "ShipCountry": "USA", "ShipCity": "Albuquerque", "OrderDate": "2016-07-22", "ShippedDate": "2016-07-25", "Freight": 17.25},
    {"OrderID": 10263, "CustomerID": "ERNSH", "ShipCountry": "Austria", "ShipCity": "Graz", "OrderDate": "2016-07-23", "ShippedDate": "2016-07-31", "Freight": 56.00},
    {"OrderID": 10264, "CustomerID": "FOLKO", "ShipCountry": "Sweden", "ShipCity": "Bräcke", "OrderDate": "2016-07-24", "ShippedDate": "2016-08-23", "Freight": 25.00},
    {"OrderID": 10265, "CustomerID": "BLONP", "ShipCountry": "France", "ShipCity": "Strasbourg", "OrderDate": "2016-07-25", "ShippedDate": "2016-08-12", "Freight": 22.50},
    {"OrderID": 10266, "CustomerID": "WARTH", "ShipCountry": "Finland", "ShipCity": "Oulu", "OrderDate": "2016-07-26", "ShippedDate": "2016-07-31", "Freight": 13.00},
    {"OrderID": 10267, "CustomerID": "FRANK", "ShipCountry": "Germany", "ShipCity": "München", "OrderDate": "2016-07-29", "ShippedDate": "2016-08-06", "Freight": 43.75},
    {"OrderID": 10268, "CustomerID": "GROSR", "ShipCountry": "Venezuela", "ShipCity": "Caracas", "OrderDate": "2016-07-30", "ShippedDate": "2016-08-02", "Freight": 13.50},
    {"OrderID": 10269, "CustomerID": "WHITC", "ShipCountry": "USA", "ShipCity": "Seattle", "OrderDate": "2016-07-31", "ShippedDate": "2016-08-09", "Freight": 30.00},
    {"OrderID": 10270, "CustomerID": "WARTH", "ShipCountry": "Finland", "ShipCity": "Oulu", "OrderDate": "2016-08-01", "ShippedDate": "2016-08-02", "Freight": 23.75},
    {"OrderID": 10271, "CustomerID": "SPLIR", "ShipCountry": "USA", "ShipCity": "Lander", "OrderDate": "2016-08-01", "ShippedDate": "2016-08-30", "Freight": 16.00},
    {"OrderID": 10272, "CustomerID": "RATTC", "ShipCountry": "USA", "ShipCity": "Albuquerque", "OrderDate": "2016-08-02", "ShippedDate": "2016-08-06", "Freight": 27.50},
    {"OrderID": 10273, "CustomerID": "QUICK", "ShipCountry": "Germany", "ShipCity": "Cunewalde", "OrderDate": "2016-08-05", "ShippedDate": "2016-08-12", "Freight": 48.00},
    {"OrderID": 10274, "CustomerID": "VINET", "ShipCountry": "France", "ShipCity": "Reims", "OrderDate": "2016-08-06", "ShippedDate": "2016-08-16", "Freight": 16.75},
    {"OrderID": 11008, "CustomerID": "ERNSH", "ShipCountry": "Austria", "ShipCity": "Graz", "OrderDate": "2018-04-08", "ShippedDate": None, "Freight": 55.25},
    {"OrderID": 11019, "CustomerID": "RANCH", "ShipCountry": "Argentina", "ShipCity": "Buenos Aires", "OrderDate": "2018-04-13", "ShippedDate": None, "Freight": 11.25},
    {"OrderID": 11039, "CustomerID": "LINOD", "ShipCountry": "Venezuela", "ShipCity": "I. de Margarita", "OrderDate": "2018-04-21", "ShippedDate": None, "Freight": 43.00},
    ]
    len(orders)
    return (orders,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Which record and which field

    `orders[0]` asks **which record**. `["ShipCountry"]` asks **which field**.
    """)
    return


@app.cell
def _(orders):
    orders[0]["ShipCountry"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ The Orders Table

    Each question is one of the moves from section 2, done to records.

    1. What is the **total freight** across all 30 orders?
    2. How many orders have **no `ShippedDate`**? That field holds `None` for them, and
       `if order["ShippedDate"] is None:` is how you ask.
    3. Which order has the **largest** freight, and what is it?

    **Check yourself:** 827.00 · 3 · order 10263 at 56.00.

    Then ask your agent, and ask which concepts its answer used.

    **Going further.** Look at the three orders with no `ShippedDate`. What do they have
    in common that the other 27 do not? The answer is not about shipping.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ What One Row Means

    **In the markdown cell below**, replace the placeholder line with your own sentence,
    in words somebody outside this course would understand. Name what a row *is*. Listing
    the columns is not an answer.

    Start it with *One row is...*

    Then check it: if a row were what you just wrote, **how many rows would this table
    have?** Does that match 30?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *One row is ...*

    *(Replace this line with your own sentence. If this cell shows you code instead of
    text, use the cell menu to turn it into a markdown cell.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 6. The Portfolio

    Six holdings. **What does it cost to buy the whole portfolio?**

    Work the steps below in order. They are what to do with any problem you cannot yet
    write yourself.

    1. **By hand, no agent. Markdown cell.** Write how you would do it in plain words,
       three or four lines. *"For each holding, multiply... then..."*
    2. **Ask your agent to write it.** Read what comes back before you keep it.
    3. **Ask it to explain every detail.** Pick the line you would not have written and
       ask what it does and why it is there.
    4. **Ask it to set you a similar problem**, then solve that one yourself.

    **Check yourself: $116,302.70.**
    """)
    return


@app.cell
def _():
    portfolio = [
        {"Symbol": "AAPL", "Shares": 100, "Price": 173.93},
        {"Symbol": "MSFT", "Shares": 50, "Price": 319.53},
        {"Symbol": "GOOG", "Shares": 80, "Price": 131.36},
        {"Symbol": "AMZN", "Shares": 200, "Price": 129.33},
        {"Symbol": "NVDA", "Shares": 20, "Price": 410.17},
        {"Symbol": "TSLA", "Shares": 150, "Price": 255.70},
    ]
    portfolio
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Going Further · The Same Question From a File

    The version above hands you the data already typed into Python. Real data arrives in
    a file. Run the cell below: it writes `portfolio.csv` into your project's `data/`
    folder, which is where [Your Python Project](/guides/python-projects/) says a data
    file goes, and makes that folder if you do not have one yet.

    Then work the same steps on this question: **open that file, read every line, and
    print the table and the total.** We have not reached files yet, so let the agent write
    that part and spend your time on steps 3 and 4.

    ```text
    name     shares     price
    AAPL        100    173.93
    ...
    Total cost: $116302.70
    ```
    """)
    return


@app.cell
def _(mo):
    _lines = ["name,shares,price"]
    for _holding in [
        ("AAPL", 100, 173.93), ("MSFT", 50, 319.53), ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33), ("NVDA", 20, 410.17), ("TSLA", 150, 255.70),
    ]:
        _lines.append(f"{_holding[0]},{_holding[1]},{_holding[2]}")

    # A data file goes in data/, which is what guides/python-projects.md tells students,
    # so this writes one folder up from the notebook. The site's build runs this notebook
    # to capture outputs (`marimo export ipynb --include-outputs`), so it must not fail a
    # build if that directory is read-only.
    _data_dir = mo.notebook_dir().parent / "data"
    try:
        _data_dir.mkdir(parents=True, exist_ok=True)
        portfolio_csv = _data_dir / "portfolio.csv"
        portfolio_csv.write_text("\n".join(_lines) + "\n")
        _where = str(portfolio_csv)
    except OSError as _error:
        _where = f"could not write into {_data_dir}: {_error}"

    _where
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🚀 This Week's Work

    1. Everything above that is not marked **Advanced**, in this file, in your repository
       under `notebooks/`
    2. Your *One row is...* sentence
    3. Commit as you go, with messages that say what changed, and push before you stop

    **What you can do now:**

    - [ ] I can take one field out of one record, by name
    - [ ] I can state what one row of a table means, in a sentence
    - [ ] I can walk a collection and total the part of it that meets a condition
    - [ ] I can tell a missing value from a zero
    - [ ] I can hand a problem to an agent and check what comes back

    You will do the same things to a pandas table in October and to a database table in
    November.
    """)
    return


if __name__ == "__main__":
    app.run()

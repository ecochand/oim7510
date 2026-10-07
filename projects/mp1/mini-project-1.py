# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
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
    # Mini Project 1 - B: A Reorder Simulation


    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*

    This tool would be used by the person who is in charge of ordering oat milk. Possibly the owner or a manager. This will assist with the decision of quantity and timing of reording the oat milk, to avoid the existing issues the case mentions (over-ordering and storing, underordering and lost customers).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*

    I would start by looking at the shops starting stock of 60 and choose reorder point test points. This would create data to run a comparison.
    step 1: calcualte day 1 oat milk delivery/stock
    step 2: calculate end of day 1 stock post sales
    step 3: sum ending stock to ordered stock and assess where this is in relation to the reorder point
    step 4: if lower or at reorder point, place order

    question 1: The loop carries the current stock and what orders have been placed.
    question 2: In section 6 I will double check that ending stock.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 1 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    starting_stock = 60
    order_quantity = 100
    lead_time_days = 3
    reorder_points = [20, 30, 40, 50]
    daily_demand = [12, 15, 9, 14, 18, 11, 10, 16, 13, 17, 8, 12, 20, 14, 11,
                    9, 15, 13, 16, 12, 10, 14, 19, 11, 13, 15, 9, 12, 17, 14]
    return (
        daily_demand,
        lead_time_days,
        order_quantity,
        reorder_points,
        starting_stock,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(daily_demand, lead_time_days, order_quantity, starting_stock):
    #reorder point

    def run_simulation(reorder_point):
        stock = starting_stock 
        pending_orders = []
        rows = []

        for day in range(1, len(daily_demand) + 1):
            demand = daily_demand[day - 1]
            starting_day_stock = stock 

            arrived = 0 
            for order in pending_orders[:]:
                if order["arrival_day"] == day:
                    arrived += order["quantity"]
                    pending_orders.remove(order)

            stock += arrived 

            sold = min(stock, demand)
            lost = demand - sold 
            stock -= sold
            inventory_position = stock + sum(
                 order["quantity"] for order in pending_orders
            )

            units_ordered = 0

            if inventory_position <= reorder_point:
                units_ordered = order_quantity
                pending_orders.append({
                    "arrival_day": day + lead_time_days,
                    "quantity": order_quantity
                })

            rows.append({
                "day": day,
                "starting_stock": starting_day_stock,
                "arrived": arrived,
                "demand": demand,
                "sold": sold,
                "lost": lost,
                "ending_stock": stock,
                "units_ordered": units_ordered
            })

        return rows

    return (run_simulation,)


@app.cell
def _(run_simulation):
    simulation_40 = run_simulation(40)
    simulation_40
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(reorder_points, run_simulation):
    print(f"{'Reorder Point':<15}{'Units Lost':<12}{'Lost Sale Days':<16}{'Orders':<10}{'Avg Ending Stock':<18}")

    for reorder_point in reorder_points:
        results = run_simulation(reorder_point)

        units_lost = sum(row["lost"] for row in results)
        days_with_lost_sales = sum(row["lost"] > 0 for row in results)
        orders_placed = sum(row["units_ordered"] > 0 for row in results)
        average_ending_stock = sum(
            row["ending_stock"] for row in results
        ) / len(results)

        print(
            f"{reorder_point:<15}"
            f"{units_lost:<12}"
            f"{days_with_lost_sales:<16}"
            f"{orders_placed:<10}"
            f"{average_ending_stock:<18.1f}"
        )
    return (results,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Immediately I look at reorder point 40 and 50 due to the 0 units lost. I would recommend a reorder point of 40 cartons due to the lower average ending stock of 48.4 compared to the reorder point of 50 cartons at 58.4.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(results):
    check_starting_stock = 60
    check_arrived = 0
    check_sold = 12

    check_ending_stock = check_starting_stock + check_arrived - check_sold

    print(f"Calculated ending stock: {check_ending_stock}")
    print(f"Simulation ending stock: {results[0]['ending_stock']}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here I compared ending stock on day 1. I calculated starting stock plus the deliveries minus the units sold and got 48 which as seen matches  the simulation endind stock.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    AI recommended a function i did not recognize, "enumerate" , to loop the daily demand and day number simultanously. This likely would have worked, but I did not know its functions. Instead I remembered range, so I changed to this and used list instead. This produced the expected day and deand values.

    This is shown in #4:

     for day in range(1, len(daily_demand) + 1):
            demand = daily_demand[day - 1]
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    for reorder_point in range(10, 81, 10):
        results = run_simulation(reorder_point)

        holding_cost = sum(row["ending_stock"] for row in results) * 0.50
        delivery_cost = sum(row["units_ordered"] > 0 for row in results) * 40
        lost_sales_cost = sum(row["lost"] for row in results) * 8

        total_cost = holding_cost + delivery_cost + lost_sales_cost

        print(f"Reorder point {reorder_point}: Total cost = ${total_cost:.2f}")
    """)
    return


@app.cell
def _(reorder_points, run_simulation):
    print(f"{'Reorder Point':<15}{'Units Lost':<12}{'Lost Sale Days':<16}{'Orders':<10}{'Avg Ending Stock':<18}")

    for reorder_point1 in reorder_points:
        results1 = run_simulation(reorder_point1)

        units_lost1 = sum(row1["lost"] for row1 in results1)
        days_with_lost_sales1 = sum(row1["lost"] > 0 for row1 in results1)
        orders_placed1 = sum(row1["units_ordered"] > 0 for row1 in results1)

        average_ending_stock1 = (
            sum(row1["ending_stock"] for row1 in results1)
            / len(results1)
        )

        print(
            f"{reorder_point1:<15}"
            f"{units_lost1:<12}"
            f"{days_with_lost_sales1:<16}"
            f"{orders_placed1:<10}"
            f"{average_ending_stock1:<18.1f}"
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As per the going further section of the assignment, I decided to go one step further by adding a cost calculation for eaach reorder point from 10-80. The goal was to compare total costs and see if the re order point of 40 i determined earlier still stood. At first I ran into an error because I was re-using variables. I added a holding cost per carton, a delivery free, and a lost sale expense per the assignment as well.
    """)
    return


if __name__ == "__main__":
    app.run()

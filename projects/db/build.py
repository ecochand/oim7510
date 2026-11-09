import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl

    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return ask, database, duckdb, mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 1. The Tables

    The database contains seven tables: members, products, options, orders, order_lines, line_options, and payments.

    Each table has a primary key, and foreign keys connect related information. Constraints are used to enforce the café's business rules.
    """)
    return


@app.cell
def _(database, duckdb, mo):
    # Remove the existing database so each build starts fresh
    if database.exists():
        database.unlink()

    # Create a new database and define its tables
    with duckdb.connect(database) as _con:

        _con.execute("""
            CREATE TABLE members (
                member_id INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                mobile_number VARCHAR NOT NULL,
                email VARCHAR,
                join_date DATE NOT NULL,
                points_balance INTEGER NOT NULL DEFAULT 0
                    CHECK (points_balance >= 0)
            )
        """)

        _con.execute("""
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY,
                product_name VARCHAR NOT NULL,
                category VARCHAR NOT NULL
                    CHECK (category IN ('coffee', 'tea', 'food', 'other')),
                price DECIMAL(10,2) NOT NULL,
                cost DECIMAL(10,2) NOT NULL,
                is_available BOOLEAN NOT NULL DEFAULT TRUE,
                CHECK (cost >= 0),
                CHECK (price >= cost)
            )
        """)

        _con.execute("""
            CREATE TABLE options (
                option_id INTEGER PRIMARY KEY,
                option_name VARCHAR NOT NULL,
                price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
                cost DECIMAL(10,2) NOT NULL CHECK (cost >= 0)
            )
        """)

        _con.execute("""
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                order_datetime TIMESTAMP NOT NULL,
                member_id INTEGER,
                channel VARCHAR NOT NULL
                    CHECK (channel IN ('counter', 'app')),
                FOREIGN KEY (member_id) REFERENCES members(member_id)
            )
        """)

        _con.execute("""
            CREATE TABLE order_lines (
                line_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                price_charged DECIMAL(10,2) NOT NULL
                    CHECK (price_charged >= 0),
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)

        _con.execute("""
            CREATE TABLE line_options (
                line_id INTEGER NOT NULL,
                option_id INTEGER NOT NULL,
                price_charged DECIMAL(10,2) NOT NULL
                    CHECK (price_charged >= 0),
                PRIMARY KEY (line_id, option_id),
                FOREIGN KEY (line_id) REFERENCES order_lines(line_id),
                FOREIGN KEY (option_id) REFERENCES options(option_id)
            )
        """)

        _con.execute("""
            CREATE TABLE payments (
                payment_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL,
                method VARCHAR NOT NULL
                    CHECK (method IN ('cash', 'card', 'app', 'points')),
                amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )
        """)

    # Load CSV files into the seven tables
        _data_dir = mo.notebook_dir() / "data"

        _tables = [
            "members",
            "products",
            "options",
            "orders",
            "order_lines",
            "line_options",
            "payments"
        ]

        for _table in _tables:
            _csv_path = _data_dir / f"{_table}.csv"

            _con.execute(
                f"INSERT INTO {_table} SELECT * FROM read_csv_auto(?)",
                [str(_csv_path)]
            )

    # Create a reusable view for sales and profitability
        _con.execute("""
            CREATE VIEW order_line_financials AS
            SELECT
                ol.line_id,
                ol.order_id,
                o.order_datetime,
                o.member_id,
                p.product_id,
                p.product_name,
                p.category,
                ol.quantity,

                ol.quantity * (
                    ol.price_charged
                    + COALESCE(opt.option_revenue, 0)
                ) AS revenue,

                ol.quantity * (
                    p.cost
                    + COALESCE(opt.option_cost, 0)
                ) AS cost

            FROM order_lines AS ol

            JOIN orders AS o
                ON ol.order_id = o.order_id

            JOIN products AS p
                ON ol.product_id = p.product_id

            LEFT JOIN (
                SELECT
                    lo.line_id,
                    SUM(lo.price_charged) AS option_revenue,
                    SUM(op.cost) AS option_cost
                FROM line_options AS lo
                JOIN options AS op
                    ON lo.option_id = op.option_id
                GROUP BY lo.line_id
            ) AS opt
                ON ol.line_id = opt.line_id
        """)

    return


@app.cell
def _(ask):
    ask("SHOW TABLES")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 2. The Data

    I used a Python script called make_data.py to generate fictional café data using a fixed random seed of 42.

    The dataset includes 45 loyalty members, 24 products, 8 options, and 1,200 orders. The orders cover November 9, 2025, through November 8, 2026, with November 8 as the as_of date.

    I intentionally included five members who never placed an order, products with no recent sales, and orders with multiple payment methods.

    To test the payment validation rule, I intentionally created two mismatches:
    - Order 101 has payments totaling $0.25 more than its order total.
    - Order 202 has payments totaling $0.50 more than its order total.

    These mismatches will be identified using SQL in Part B.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 3. A Look at the Data

    I chose to examine the number of café orders by hour of the day to evaluate whether the generated data reflects realistic customer purchasing patterns.
    """)
    return


@app.cell
def _():
    import polars as pl

    return (pl,)


@app.cell
def _(mo, pl):
    orders_data = pl.read_csv(
        mo.notebook_dir() / "data" / "orders.csv",
        try_parse_dates=True
    )

    orders_by_hour = (
        orders_data
        .with_columns(
            pl.col("order_datetime").dt.hour().alias("hour")
        )
        .group_by("hour")
        .agg(pl.len().alias("number_of_orders"))
        .sort("hour")
    )

    orders_by_hour
    return (orders_by_hour,)


@app.cell
def _(mo, orders_by_hour):
    orders_chart = mo.ui.altair_chart(
        orders_by_hour.plot.bar(
            x="hour",
            y="number_of_orders"
        ).properties(
            title="Babson Bean Café Orders by Hour of Day"
        )
    )

    orders_chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The initial data showed orders distributed relatively evenly throughout the day, which did not seem realistic for a campus café. I updated the data-generation script to create more orders during the morning and lunch hours, when students and faculty would likely be purchasing coffee and food. The revised distribution better represents expected café purchasing patterns.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 4. Row Counts

    The following query displays the number of records in each of the seven database tables. This helps verify that the data was loaded successfully and that the dataset meets the minimum requirements.
    """)
    return


@app.cell
def _(ask):
    row_counts = ask("""
        SELECT 'members' AS table_name, COUNT(*) AS row_count FROM members
        UNION ALL
        SELECT 'products', COUNT(*) FROM products
        UNION ALL
        SELECT 'options', COUNT(*) FROM options
        UNION ALL
        SELECT 'orders', COUNT(*) FROM orders
        UNION ALL
        SELECT 'order_lines', COUNT(*) FROM order_lines
        UNION ALL
        SELECT 'line_options', COUNT(*) FROM line_options
        UNION ALL
        SELECT 'payments', COUNT(*) FROM payments
    """)

    row_counts
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The database contains 45 loyalty members, 24 menu products, 8 options, and 1,200 orders. These counts meet the minimum data requirements for the Babson Bean Café scenario.

    The order_lines, line_options, and payments tables contain additional records because an order can include multiple products, options, and payment methods.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 5. A Row It Refuses

    The café requires every order line to have a quantity greater than zero.

    I will test this rule by attempting to insert an order line with a quantity of zero. The database should reject the record because the quantity column has a CHECK constraint.
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.execute("""
                INSERT INTO order_lines
                    (line_id, order_id, product_id, quantity, price_charged)
                VALUES (999999, 1, 1, 0, 5.25)
            """)
        print("Unexpected result: The database accepted the invalid row.")

    except duckdb.ConstraintException as _error:
        print("The database correctly rejected the row.")
        print("Error:", _error)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The database rejected the invalid order line because its quantity was zero. This confirms that the CHECK constraint on the quantity column is working as intended and prevents orders from containing products with invalid quantities.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 6. Answers You Already Knew

    I created three SQL queries to verify that the database contains the data I intended to generate. Since I know how the data was created in make_data.py, I can compare the SQL results against my expected answers.
    """)
    return


@app.cell
def _(ask):
    known_orders = ask("""
        SELECT COUNT(*) AS total_orders
        FROM orders
    """)

    known_orders
    return


@app.cell
def _(ask):
    known_options = ask("""
        SELECT COUNT(*) AS total_options
        FROM options
    """)

    known_options
    return


@app.cell
def _(ask):
    known_inactive_members = ask("""
        SELECT m.member_id, m.first_name
        FROM members AS m
        LEFT JOIN orders AS o
            ON m.member_id = o.member_id
        WHERE o.order_id IS NULL
        ORDER BY m.member_id
    """)

    known_inactive_members
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The results matched my expectations:

    1. The database contains 1,200 orders, as specified in my data-generation script.
    2. The database contains eight drink options.
    3. Members 41 through 45 have never placed an order, which I intentionally designed into the dataset.

    These results help confirm that the database was populated correctly and that the relationships between members and orders work as intended.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. A View

    I created a view called order_line_financials to calculate revenue and estimated costs for each order line, including any drink options.

    The café can use this view to monitor weekly sales without repeatedly calculating the same information. It will also help answer business questions about profitability in Part B.
    """)
    return


@app.cell
def _(ask):
    weekly_sales = ask("""
        SELECT
            DATE_TRUNC('week', order_datetime) AS week,
            ROUND(SUM(revenue), 2) AS total_revenue,
            ROUND(SUM(cost), 2) AS total_cost,
            ROUND(SUM(revenue - cost), 2) AS estimated_profit
        FROM order_line_financials
        GROUP BY week
        ORDER BY week DESC
        LIMIT 8
    """)

    weekly_sales
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The order_line_financials view allows Babson Bean Café to track weekly revenue, estimated costs, and profit without repeating calculations across multiple tables.

    The view includes revenue from products and their selected options. I can also use this view in Part B to analyze revenue and profitability by menu category.
    """)
    return


if __name__ == "__main__":
    app.run()

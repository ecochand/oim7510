import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb

    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return ask, database, duckdb, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 1. The Tables

    The database contains seven tables: members, products, options, orders, order_lines, line_options, and payments.

    Each table has a primary key, and foreign keys connect related information. Constraints are used to enforce the café's business rules.
    """)
    return


@app.cell
def _(database, duckdb):
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


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

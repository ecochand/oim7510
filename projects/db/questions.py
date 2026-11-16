import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    from datetime import date

    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return date, mo


@app.cell
def _(date):
    as_of = date(2026, 11, 8)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 3. Reading It Back

    **Selected Question:** What are the revenue, cost, and profit margin for each menu category?

    **My Prediction:**

    I predict that joining the orders, order_lines, and products tables will produce exactly the same number of rows as the order_lines table.

    This is because every order line belongs to exactly one order and references exactly one product. Therefore, each order line should match one row in each of the other two tables, without creating additional rows or losing any.

    I will verify this prediction by counting the rows produced by the joins before grouping the results by category.
    """)
    return


if __name__ == "__main__":
    app.run()

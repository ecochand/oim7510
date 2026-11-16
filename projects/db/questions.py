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

    return ask, date, mo


@app.cell
def _(date):
    as_of = date(2026, 11, 8)
    return (as_of,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 3. Reading It Back

    **Selected Question:** What are the revenue, cost, and profit margin for each menu category?

    **My Prediction:**

    I predict that joining the orders, order_lines, and products tables will produce the same number of rows as the order_lines table.

    This is due to the fact that every order line belongs to exactly one order and references exactly one product. Therefore, each order line should match one row in each of the other two tables, without creating additional rows or losing any.

    I will confirm this prediction by counting the rows produced by the joins before grouping the results by category.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Question 1: What were the three best-selling products last month?

    This query identifies the three products with the highest number of units sold during October 2026.
    """)
    return


@app.cell
def _(as_of, ask):
    q1 = ask(f"""
        SELECT
            p.product_name,
            SUM(ol.quantity) AS units_sold
        FROM order_lines AS ol
        JOIN products AS p
            ON ol.product_id = p.product_id
        JOIN orders AS o
            ON ol.order_id = o.order_id
        WHERE o.order_datetime >=
            DATE_TRUNC('month', DATE '{as_of}')
            - INTERVAL '1 month'
          AND o.order_datetime <
            DATE_TRUNC('month', DATE '{as_of}')
        GROUP BY p.product_id, p.product_name
        ORDER BY units_sold DESC, p.product_name
        LIMIT 3
    """)

    q1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The three best selling products in October 2026 were Orange Juice units of 39, Chai Latte units of 30, and Mocha units of 24.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Question 2: How much revenue, cost, and profit does each menu category generate?

    This query calculates revenue, cost, gross profit, and gross margin for each menu category, including any drink add-ons.
    """)

    return


@app.cell
def _(as_of, ask):
    q2 = ask(f"""
        SELECT
            category,
            ROUND(SUM(revenue), 2) AS total_revenue,
            ROUND(SUM(cost), 2) AS total_cost,
            ROUND(SUM(revenue - cost), 2) AS gross_profit,
            ROUND(
                100.0 * SUM(revenue - cost)
                / NULLIF(SUM(revenue), 0), 2
            ) AS gross_margin_percent
        FROM order_line_financials
        WHERE order_datetime < DATE '{as_of}' + INTERVAL '1 day'
        GROUP BY category
        ORDER BY total_revenue DESC
    """)

    q2
    return


app._unparsable_cell(
    r"""
    Coffee generated the highest revenue at $8,029, with costs of $2,525.13, gross profit of $5,513.87, and a gross margin of 68.67%. Next was food, followed by tea, and other. Tea had the highest gross margin at 69.18%. The results included revenue and costs from drink add ons in their associated product categories.  
    """,
    name="_"
)


@app.cell
def _(mo):
    mo.md("""
    ## Question 3: Which loyalty members spend more than the average member?

    This query calculates each loyalty member's number of orders, total spending, and average order value. It then identifies members whose total spending exceeds the average across all loyalty members, including those who have never ordered.
    """)
    return


@app.cell
def _(as_of, ask):

    q3 = ask(f"""
        WITH order_totals AS (
            SELECT
                order_id,
                SUM(revenue) AS order_total
            FROM order_line_financials
            WHERE order_datetime < DATE '{as_of}' + INTERVAL '1 day'
            GROUP BY order_id
        ),

        member_spending AS (
            SELECT
                m.member_id,
                m.first_name,
                COUNT(o.order_id) AS number_of_orders,
                COALESCE(SUM(ot.order_total), 0) AS total_spent
            FROM members AS m
            LEFT JOIN orders AS o
                ON m.member_id = o.member_id
                AND o.order_datetime < DATE '{as_of}' + INTERVAL '1 day'
            LEFT JOIN order_totals AS ot
                ON o.order_id = ot.order_id
            GROUP BY m.member_id, m.first_name
        )

        SELECT
            member_id,
            first_name,
            number_of_orders,
            ROUND(total_spent, 2) AS total_spent,
            ROUND(
                total_spent / NULLIF(number_of_orders, 0), 2
            ) AS average_order_value
        FROM member_spending
        WHERE total_spent > (
            SELECT AVG(total_spent)
            FROM member_spending
        )
        ORDER BY total_spent DESC
    """)

    q3

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Of the 45 loyalty members, 21 spent more than the average total spending per member. Member26 was the highest-spending customer, placing 32 orders and spending $619.25, with an average order value of $19.35. Member2 followed with $579.00 across 34 orders, while Member23 spent $560.75 across 34 orders.

    This analysis includes all loyalty members, including those who have never placed an order.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Question 4: Do the payments for every order match the actual order total?

    This query compares the total amount charged for each order, including products and add-ons, against the total amount paid.

    The café requires payments to equal the order total. I intentionally created two mismatches in the generated data to test whether the query can identify them.
    """)
    return


@app.cell
def _(as_of, ask):

    q4 = ask(f"""
        WITH order_totals AS (
            SELECT
                order_id,
                SUM(revenue) AS order_total
            FROM order_line_financials
            WHERE order_datetime < DATE '{as_of}' + INTERVAL '1 day'
            GROUP BY order_id
        ),

        payment_totals AS (
            SELECT
                order_id,
                SUM(amount) AS total_paid
            FROM payments
            GROUP BY order_id
        )

        SELECT
            o.order_id,
            ROUND(ot.order_total, 2) AS order_total,
            ROUND(COALESCE(pt.total_paid, 0), 2) AS total_paid,
            ROUND(
                COALESCE(pt.total_paid, 0) - ot.order_total,
                2
            ) AS difference

        FROM orders AS o

        JOIN order_totals AS ot
            ON o.order_id = ot.order_id

        LEFT JOIN payment_totals AS pt
            ON o.order_id = pt.order_id

        WHERE ABS(
            COALESCE(pt.total_paid, 0) - ot.order_total
        ) > 0.001

        ORDER BY o.order_id
    """)

    q4

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Of the 1,200 orders, two had payment totals that did not match their purchase totals. Order 101 had a purchase total of $8.25 but payments totaling $8.50, resulting in an overpayment of $0.25. Order 202 had a purchase total of $27.75 but payments totaling $28.25, resulting in an overpayment of $0.50.

    The remaining 1,198 orders had matching payment and purchase totals. These two mismatches were intentionally created in make_data.py, confirming that the SQL query correctly identifies violations of the café's payment rule.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Question 5: Which loyalty members have never placed an order?

    This query identifies loyalty members who joined the program but have never made a purchase. It helps the café identify customers who signed up but have not used their membership.
    """)
    return


@app.cell
def _(as_of, ask):
    q5 = ask(f"""
        SELECT
            m.member_id,
            m.first_name,
            m.join_date
        FROM members AS m
        LEFT JOIN orders AS o
            ON m.member_id = o.member_id
            AND o.order_datetime < DATE '{as_of}' + INTERVAL '1 day'
        WHERE o.order_id IS NULL
        ORDER BY m.member_id
    """)

    q5
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Five of the 45 loyalty members have never placed an order as of November 8, 2026. These members are Member41, Member42, Member43, Member44, and Member45. Their join dates range from October 7, 2025, to March 9, 2026.

    These results match the five members intentionally excluded from purchases in the generated dataset.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Question 6: What percentage of orders were paid at least partly with loyalty points each month?

    This query calculates the percentage of orders each month that included at least one payment using loyalty points. Orders with multiple payment methods are counted only once.
    """)
    return


@app.cell
def _(as_of, ask):

    q6 = ask(f"""
        SELECT
            DATE_TRUNC('month', o.order_datetime)::DATE AS month,
            COUNT(*) AS total_orders,

            COUNT(*) FILTER (
                WHERE EXISTS (
                    SELECT 1
                    FROM payments AS p
                    WHERE p.order_id = o.order_id
                      AND p.method = 'points'
                )
            ) AS orders_using_points,

            ROUND(
                100.0 * COUNT(*) FILTER (
                    WHERE EXISTS (
                        SELECT 1
                        FROM payments AS p
                        WHERE p.order_id = o.order_id
                          AND p.method = 'points'
                    )
                ) / NULLIF(COUNT(*), 0),
                2
            ) AS percent_using_points

        FROM orders AS o
        WHERE o.order_datetime >= DATE '{as_of}' - INTERVAL '364 days'
          AND o.order_datetime < DATE '{as_of}' + INTERVAL '1 day'

        GROUP BY 1
        ORDER BY month
    """)

    q6

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The percentage of orders paid at least partly with loyalty points varied throughout the reporting period. October 2026 had the highest usage, with 29 of 97 orders (29.90%) including a points payment. September 2026 had the lowest usage, with 14 of 92 orders (15.22%) using points.

    The analysis counts each order only once, even when multiple payment methods were used.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Question 7: Which products have not sold in the last 60 days?

    This query identifies products that have not been purchased during the 60-day period ending November 8, 2026, including products that are currently unavailable.
    """)
    return


@app.cell
def _(as_of, ask):

    q7 = ask(f"""
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            p.is_available,
            MAX(o.order_datetime)::DATE AS last_sale_date

        FROM products AS p

        LEFT JOIN order_lines AS ol
            ON p.product_id = ol.product_id

        LEFT JOIN orders AS o
            ON ol.order_id = o.order_id
            AND o.order_datetime < DATE '{as_of}' + INTERVAL '1 day'

        GROUP BY
            p.product_id,
            p.product_name,
            p.category,
            p.is_available

        HAVING
            MAX(o.order_datetime) IS NULL
            OR MAX(o.order_datetime) <
                DATE '{as_of}' - INTERVAL '59 days'

        ORDER BY p.product_id
    """)

    q7

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two products had no sales during the 60-day period ending November 8, 2026: Seasonal Scone and Seasonal Smoothie. Both products are currently unavailable. Seasonal Scone was last purchased on September 8, 2026, while Seasonal Smoothie has never been purchased.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Question 8: Which drink add-ons generate the most gross profit?

    This query identifies the café's most profitable drink add-ons by comparing the revenue and cost associated with each option. It accounts for the number of drinks purchased, since an add-on is charged for every unit on an order line.
    """)
    return


@app.cell
def _(as_of, ask):

    q8 = ask(f"""
        SELECT
            op.option_name,
            SUM(ol.quantity) AS units_sold,
            ROUND(
                SUM(lo.price_charged * ol.quantity), 2
            ) AS total_revenue,
            ROUND(
                SUM(op.cost * ol.quantity), 2
            ) AS total_cost,
            ROUND(
                SUM((lo.price_charged - op.cost) * ol.quantity), 2
            ) AS gross_profit,
            ROUND(
                100.0 * SUM((lo.price_charged - op.cost) * ol.quantity)
                / NULLIF(SUM(lo.price_charged * ol.quantity), 0),
                2
            ) AS gross_margin_percent

        FROM line_options AS lo

        JOIN options AS op
            ON lo.option_id = op.option_id

        JOIN order_lines AS ol
            ON lo.line_id = ol.line_id

        JOIN orders AS o
            ON ol.order_id = o.order_id

        WHERE o.order_datetime < DATE '{as_of}' + INTERVAL '1 day'

        GROUP BY op.option_id, op.option_name

        ORDER BY gross_profit DESC
    """)

    q8

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Extra Matcha generated the highest gross profit at $235.45, with 277 units sold, $415.50 in revenue, and a gross margin of 56.67%. Extra Shot followed with $181.05 in gross profit and a 68.00% margin.

    Although Vanilla Syrup and Caramel Syrup generated less total profit, they had the highest gross margins at 76.00% each.

    Decaf was the only unprofitable add-on, generating a loss of $30.30 because customers were not charged for it despite the café incurring a cost.
    """)
    return


if __name__ == "__main__":
    app.run()

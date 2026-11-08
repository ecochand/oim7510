
import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

# Use the same random data every time
rng = random.Random(42)

data_dir = Path(__file__).resolve().parent / "data"
data_dir.mkdir(parents=True, exist_ok=True)

as_of = date(2026, 11, 8)
start_date = as_of - timedelta(days=364)


def save_csv(filename, rows):
    path = data_dir / filename
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"{filename}: {len(rows)} rows")


def dollars(cents):
    return f"{cents / 100:.2f}"


# 1. Loyalty members
members = []
for member_id in range(1, 46):
    joined = date(2025, 9, 1) + timedelta(
        days=rng.randint(0, 330)
    )
    members.append({
        "member_id": member_id,
        "first_name": f"Member{member_id}",
        "mobile_number": f"617555{member_id:04d}",
        "email": (
            f"member{member_id}@example.com"
            if member_id % 4 != 0 else ""
        ),
        "join_date": joined.isoformat(),
        "points_balance": rng.randint(0, 250)
    })


# 2. Menu products: name, category, price, cost (cents)
menu = [
    ("Latte", "coffee", 525, 175),
    ("Cappuccino", "coffee", 475, 150),
    ("Americano", "coffee", 350, 90),
    ("Espresso", "coffee", 300, 75),
    ("Cold Brew", "coffee", 450, 125),
    ("Iced Latte", "coffee", 550, 185),
    ("Mocha", "coffee", 575, 200),
    ("Drip Coffee", "coffee", 275, 65),
    ("Chai Latte", "tea", 500, 165),
    ("Matcha Latte", "tea", 575, 210),
    ("Green Tea", "tea", 300, 70),
    ("Black Tea", "tea", 300, 65),
    ("Herbal Tea", "tea", 325, 75),
    ("Bagel", "food", 350, 120),
    ("Croissant", "food", 400, 150),
    ("Blueberry Muffin", "food", 375, 135),
    ("Breakfast Sandwich", "food", 725, 310),
    ("Yogurt Parfait", "food", 625, 250),
    ("Banana Bread", "food", 425, 160),
    ("Cookie", "food", 275, 95),
    ("Bottled Water", "other", 250, 80),
    ("Orange Juice", "other", 350, 140),
    ("Seasonal Scone", "food", 450, 180),
    ("Seasonal Smoothie", "other", 650, 275)
]

products = []
for product_id, (name, category, price, cost) in enumerate(
    menu, start=1
):
    products.append({
        "product_id": product_id,
        "product_name": name,
        "category": category,
        "price": dollars(price),
        "cost": dollars(cost),
        "is_available": product_id not in (23, 24)
    })


# 3. Drink options: name, price, cost (cents)
option_menu = [
    ("Extra Shot", 125, 40),
    ("Oat Milk", 75, 35),
    ("Vanilla Syrup", 50, 12),
    ("Caramel Syrup", 50, 12),
    ("Almond Milk", 75, 35),
    ("Whipped Cream", 50, 18),
    ("Extra Matcha", 150, 65),
    ("Decaf", 0, 10)
]

options = []
for option_id, (name, price, cost) in enumerate(
    option_menu, start=1
):
    options.append({
        "option_id": option_id,
        "option_name": name,
        "price": dollars(price),
        "cost": dollars(cost)
    })


# 4-7. Generate orders and their related records
orders = []
order_lines = []
line_options = []
payments = []

line_id = 0
payment_id = 0

# Two intentional payment mismatches
bad_payments = {101: 25, 202: 50}

for order_id in range(1, 1201):

    order_date = start_date + timedelta(
        days=rng.randint(0, 364)
    )
    order_time = datetime.combine(
        order_date,
        datetime.min.time()
    ).replace(
        hour=rng.choices(
            range(7, 20),
            weights=[7, 12, 16, 15, 12, 10, 8, 6, 5, 4, 3, 1, 1],
            k=1
        )[0],
        minute=rng.randint(0, 59)
    )

    # Members 41-45 are intentionally never used
    eligible = [
        m["member_id"] for m in members[:40]
        if date.fromisoformat(m["join_date"]) <= order_date
    ]

    member_id = (
        rng.choice(eligible)
        if eligible and rng.random() < 0.65
        else None
    )

    orders.append({
        "order_id": order_id,
        "order_datetime": order_time.isoformat(sep=" "),
        "member_id": member_id if member_id else "",
        "channel": rng.choice(["counter", "app"])
    })

    order_total = 0
    number_of_lines = rng.randint(1, 3)

    for _ in range(number_of_lines):
        line_id += 1

        # Products 23 and 24 have no recent sales.
        # Product 24 is never sold at all.
        available_ids = list(range(1, 23))
        if order_date < as_of - timedelta(days=60):
            available_ids.append(23)

        product_id = rng.choice(available_ids)
        quantity = rng.randint(1, 3)
        product_price = menu[product_id - 1][2]

        order_lines.append({
            "line_id": line_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "price_charged": dollars(product_price)
        })

        order_total += quantity * product_price

        # Only drinks can have add-ons
        category = menu[product_id - 1][1]
        if category in ("coffee", "tea"):
            number_of_options = rng.choice([0, 0, 1, 1, 2])
            selected = rng.sample(
                range(1, 9), number_of_options
            )

            for option_id in selected:
                option_price = option_menu[option_id - 1][1]

                line_options.append({
                    "line_id": line_id,
                    "option_id": option_id,
                    "price_charged": dollars(option_price)
                })

                # Options are charged per unit
                order_total += quantity * option_price

    # Usually one payment; sometimes split payments
    if order_total > 1 and rng.random() < 0.25:
        first_amount = round(order_total * 0.4)
        amounts = [
            first_amount,
            order_total - first_amount
        ]
    else:
        amounts = [order_total]

    methods = ["cash", "card", "app"]
    if member_id is not None:
        methods.append("points")

    for index, amount in enumerate(amounts):
        payment_id += 1

        # Break the payment-total rule in exactly
        # two orders, without breaking CHECK rules
        if order_id in bad_payments and index == 0:
            amount += bad_payments[order_id]

        payments.append({
            "payment_id": payment_id,
            "order_id": order_id,
            "method": rng.choice(methods),
            "amount": dollars(amount)
        })


# Save one CSV file for every table
save_csv("members.csv", members)
save_csv("products.csv", products)
save_csv("options.csv", options)
save_csv("orders.csv", orders)
save_csv("order_lines.csv", order_lines)
save_csv("line_options.csv", line_options)
save_csv("payments.csv", payments)

print("\nIntentional payment mismatches:")
print("Order 101: payments exceed total by $0.25")
print("Order 202: payments exceed total by $0.50")
print(f"\nAs-of date: {as_of}")

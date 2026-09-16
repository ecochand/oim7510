# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Your first notebook.

Shared by OIM7510 and OIM6301, and used in the session Reading an error message.
Written for the first session, which did not reach it in either room, then extended
with that session's blocks on types, f-strings and error messages.

AUTHORING NOTES.

Every markdown cell carries `hide_code=True`, so a student sees the rendered
prose without the `mo.md` wrapper around it. Keep it on any cell that is only
markdown, and leave it off any cell whose code a student should read.

The four experiments ask a student to edit, delete and reorder cells, which
`--mode run` cannot do. This is written for `marimo edit` on the student's own
machine.

Python §2, §3, §6 and §10 carry `Try it` versions of some of the same ideas
(`"5" + "3"`, `import pandsa`, a `Freight: $16.75` line). Since 2026-09-12 the same
exercise may sit in both files when each serves its own file's purpose
(docs/handbooks.md). These use this notebook's own lists.

Handbook pointers are plain text, because the two course sites serve this one file
and a link would send one course to the other's site.

No cell in this file raises. Every error a student meets is one they type into a cell
of their own, so the notebook opens and exports clean.

It imports nothing but marimo, because a student's project has only `uv add marimo`
(measured 2026-09-13: `import matplotlib` raises ModuleNotFoundError there). The bar
chart is code a student pastes after running `uv add matplotlib`.
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
    # Your First Notebook
    """)
    return


@app.cell
def _():
    print("hello, world. I am emma")

    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # How This Notebook Works

    Every section starts with a mark.

    - **▶️ Run and read.** In class this runs on screen first. Run the cell yourself and read what it shows
    - **🙋 Predict first.** Write down what you expect before you run anything
    - **✏️ Your turn.** Write the code yourself, in new cells
    - **🚀 This week's work.** Finish it after class and push it

    Save as you go with `Ctrl+S` (Windows) or `Cmd+S` (macOS).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ A Name Holding Several Things

    A name, which most books and every job posting call a **variable**, holds a value.
    `=` puts the value there, and that is called an **assignment**. Read it as
    *put this in that*.

    The five numbers below are the freight charged on orders `10248` through `10252`.

    📖 Handbook: Python §1 Variables and values, §11 Lists
    """)
    return


@app.cell
def _():
    freight_charges = [99.99, 22.25, 25.00, 20.25, 36.25]
    freight_charges
    return (freight_charges,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✏️ Add Three Cells

    Add three cells below with the **+** button. Put one line in each.

    1. The freight on the **first** order: `freight_charges[0]`
    2. **How many** orders there are: `len(freight_charges)`
    3. The **total**: `total = sum(freight_charges)`, then `total` on the next line

    Keep them in separate cells. The next section depends on it.

    `len` and `sum` are **functions**, and what you put in the brackets is the **argument**.

    *The number in brackets is an **index**, and Python counts from zero, so
    `freight_charges[0]` is the first one.*
    """)
    return


@app.cell
def _(freight_charges):
    freight_charges[0]
    return


@app.cell
def _(freight_charges):
    len(freight_charges)
    return


@app.cell
def _(freight_charges):
    total =sum(freight_charges)
    total
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🙋 Before You Run Anything

    Write all four answers down before you run anything.

    1. Cell A says `x = 5`. Cell B says `print(x)`. You change A to `x = 50`.
       **What does B print?**
    2. Cell A says `orders = 3`. Cell B says `orders * 12`. You **delete cell A**.
       **What happens to B?**
    3. Two different cells both say `total = ...`. **What happens?**
    4. You put `print(total)` **above** the cell that says `total = 5`.
       **Does it run?**

    Four experiments follow. Do them in order, and undo each one before the next.
    """)
    return


@app.cell
def _():
    x = 10
    return (x,)


@app.cell
def _(x):
    s = x + 100
    return (s,)


@app.cell
def _(s, x):
    print(x)
    print(s)
    return


@app.cell
def _():
    order = 3
    return (order,)


@app.cell
def _(order):
    order  * 12
    return


@app.cell
def _(totals):
    totals
    return


@app.cell
def _(order, x):
    totals = x * order - 10
    totals
    return (totals,)


app._unparsable_cell(
    r"""
    1. 5
    2. 36
    3. it sums both 
    4. it refers to what is directly above it
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Experiment 1

    Change `16.75` to `999.99` in the `freight_charges` cell. Run only that cell.

    Watch your three cells.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Experiment 2

    Delete the `freight_charges` cell. Watch your three cells.

    Then bring it back: undo, or type the line again.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Experiment 3

    Add a cell anywhere and put `total = 1` in it.

    Delete it again once you have seen what happens.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Experiment 4

    Drag the cell holding `total = sum(freight_charges)` **below** the cell that shows
    `total`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ What Happened

    1. **Everything that used the number recomputed by itself.** You ran one cell.
    2. **The cells using the deleted name went blank.** No cell keeps showing a value
       whose source is gone.
    3. **You got an error.** A name is defined in exactly one cell, so you can never
       be looking at a `total` that some other cell changed.
    4. **It ran.** This notebook works out what depends on what and runs in that
       order. The name for that dependency map is a **DAG**, a directed acyclic graph,
       which is why a cell cannot depend on itself. Where a cell sits on the page is a
       layout choice.

    📖 Handbook: Python §1 Variables and values
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ A Second Name

    `orders` holds the five order numbers, each in the same position as its charge.
    """)
    return


@app.cell
def _():
    orders = [10248, 10249, 10250, 10251, 10252]
    orders
    return (orders,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🙋 Explore

    One line per cell. Write down what you expect before you run it. Every one of these
    depends on the **type** of the thing you hand it.

    1. `freight_charges[-1]`
    2. `freight_charges[:3]`, which is a **slice**
    3. `orders[0]` and `freight_charges[0]`. What do those two have in common?
    4. `category = "Confections"`, then `len(category)`. `len` counted five things a moment ago. What is it counting now?
    5. `sum(orders)`. It runs. Should it?
    6. `orders * 2`, then `orders + freight_charges`. Neither one is an error.
    7. `sorted(freight_charges)`, then `sorted(freight_charges, reverse=True)`. What did `reverse=True` change, and did `freight_charges` itself change?
    """)
    return


@app.cell
def _(freight_charges):
    freight_charges[-1]
    return


@app.cell
def _(freight_charges):
    freight_charges[:3]
    return


@app.cell
def _(orders):
    orders[0]
    return


@app.cell
def _(freight_charges):
    freight_charges[0]
    return


@app.cell
def _():
    category = "Confections"
    len(category)
    return


@app.cell
def _(orders):
    sum(orders)
    return


@app.cell
def _(freight_charges, orders):
    orders * 2
    orders + freight_charges
    return


@app.cell
def _(freight_charges):
    sorted(freight_charges)
    sorted(freight_charges, reverse=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ What Type Is It

    What kind of value is each thing in these two lists?
    """)
    return


@app.cell
def _(freight_charges, orders):
    type(freight_charges[0]), type(orders[0]), type("Confections"), type(freight_charges[0] > 20)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A value's **type** decides what you can do with it. These four come up in almost every notebook: `float` for a number with a decimal point, `int` for a whole number, `str` for text, and `bool` for `True` or `False`.

    📖 Handbook: Python §2 Types
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🙋 Text That Looks Like a Number

    Write down what each line gives, then put each one in a cell of your own.

    1. `"16.75" + "22.25"`
    2. `16.75 + "22.25"`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ What Came Back

    The first line gives `'16.7522.25'`. Both values are text, so `+` joins them end to end.

    The second stops with `TypeError: unsupported operand type(s) for +: 'float' and 'str'`, because Python will not add a number to text.

    A list of prices that arrives as text behaves like the first line. It runs, and the result is wrong.

    📖 Handbook: Python §2 Types
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✏️ Compare Two Charges

    In cells of your own:

    1. Is the first charge above 20? `freight_charges[0] > 20`
    2. Is the last charge the largest? `freight_charges[-1] == max(freight_charges)`
    3. Check the type of either answer with `type()`.

    `==` asks whether two values are equal. A single `=` stores a value.

    📖 Handbook: Python §3 Expressions and operators
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ A Sentence With a Number

    How do you put a number from the list into a sentence somebody can read?
    """)
    return


@app.cell
def _(freight_charges, orders):
    print(f"Order {orders[0]} paid ${freight_charges[0]:.2f} in freight.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `f` before the quotes makes this an **f-string**. Python works out anything inside `{ }` and places it in the text. `:.2f` shows exactly two decimal places.

    📖 Handbook: Python §6 f-strings
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✏️ A Sentence of Your Own

    In a cell of your own, print one sentence that states the total freight and the average charge, each with two decimal places. Use the `total` you made earlier, and divide it by `len(freight_charges)` for the average.

    Your sentence should show `$120.50` and `$24.10`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ Keep Only Some

    Which orders paid more than 20 in freight?
    """)
    return


@app.cell
def _(freight_charges):
    over_20 = []
    for charge in freight_charges:
        if charge > 20:
            over_20.append(charge)
    over_20
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `for` takes each charge in the list in turn and runs the indented lines once for it. `if` runs its indented line only when its condition is `True`, and `.append()` adds that charge to the end of `over_20`, which started empty.

    The indent is part of the code. Leave it out and Python stops with an `IndentationError`.

    📖 Handbook: Python §4 Conditionals, §12 Iterating over a list with `for`, §13 Filtering and the accumulator
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✏️ Charges Below 25

    In cells of your own:

    1. Build a list of the charges below 25, the same way.
    2. Print one sentence with an f-string that says how many charges are in it and what they add up to.
    3. Change `<` to `<=` and run it again. Which order joined the list, and why?

    Your loop needs names of its own. `charge` and `over_20` already belong to the cell above, and a name lives in exactly one cell, which is what Experiment 3 showed.

    With the list as it started, your sentence should show three charges and `$59.25`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ Read the Last Line First

    When a cell fails, marimo shows Python's error message under it.

    Add a cell with `freight_charges[5]` and run it. You get an `IndexError`.

    The **last line** names the error and states what went wrong: `list index out of range`. The list has five items, at positions 0 to 4, so position 5 does not exist. The lines above it show where Python was when it stopped.

    Delete the cell once you have read it.

    📖 Handbook: Python §10 Reading a traceback
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✏️ Break It Three Ways

    Each line below fails. Put each one in a cell of your own and run it. Under each, add a markdown cell that explains the last line of the error in your own words.

    1. `import pandsa`, a package name with a typo
    2. `open("sales.csv")`, a file that is not in your project
    3. `new_charges = [16.75, 22.25`, with the closing bracket missing

    You should meet three different kinds of error. Keep your markdown cells, and delete the broken cells so the notebook runs clean.

    If marimo offers to install `pandsa`, do not. No package has that name, so the install fails.

    📖 Handbook: Python §9 Modules and `import`, §10 Reading a traceback
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🙋 A Line That Does Not Break

    Write down what this gives, then run it in a cell of your own.

    `max(["9.50", "16.75", "22.25"])`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ Why the Smallest Price Came Out on Top

    It returns `'9.50'`, with no error.

    The three values are text, so Python compares them as text, one character at a time. `"9"` comes after `"2"` and `"1"`, so `"9.50"` counts as the largest. Written as numbers, `max([9.50, 16.75, 22.25])` returns `22.25`.

    📖 Handbook: Python §2 Types
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✏️ Read This One on Paper

    **By hand, with no agent.** When code an agent wrote is the thing that broke, reading the error yourself is how you find out why.

    A file called `hello.py`, with its line numbers:

    ```text
    1  freight_charges = [16.75, 22.25, "pending", 9.50]
    2
    3  total = sum(freight_charges)
    4  print(total)
    ```

    Running it prints:

    ```text
    Traceback (most recent call last):
      File "/Users/you/oim7510/hello.py", line 3, in <module>
        total = sum(freight_charges)
    TypeError: unsupported operand type(s) for +: 'float' and 'str'
    ```

    1. Which line does Python name?
    2. Which line would you change, and why is it a different line from the one Python named?
    3. What would you change it to? More than one answer is defensible, so state the rule you chose.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ The List as a Bar Chart

    > **Advanced.** Nothing later depends on this.

    A chart needs **matplotlib**, which your project does not have yet. Add it in VS Code's Terminal:

    ```text
    uv add matplotlib
    ```

    Then paste this into a new cell. Change a number in `freight_charges` and the bars move on their own.

    ```python
    import matplotlib.pyplot as plt

    _fig, _ax = plt.subplots(figsize=(6, 2.6))
    _ax.bar([str(_o) for _o in orders], freight_charges)
    _ax.set_ylabel("freight")
    _fig
    ```

    The square brackets inside `_ax.bar(...)` are a **list comprehension**, which **iterates** over `orders` and turns each number into text.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✏️ Push It

    1. Change one number in the `freight_charges` list. Watch your three cells update.
    2. Save the file **inside your repository, in the `notebooks/` folder**.
    3. In **GitHub Desktop**: write a commit message, click **Commit to main**,
       then **Push origin**.
    4. Open **github.com**, go to your repository, and click on the notebook.

    *Nothing there? Check that GitHub Desktop is showing the right repository at
    the top left, and that the file you saved is inside that repository's folder.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🚀 A Question About Your Own Numbers

    Pick a question from your own work or life that a short list of numbers can answer, such as what you spent on groceries each month since March, or how many minutes your commute took each day last week.

    **Where it goes.** A new notebook in your `notebooks/` folder, made from the page that `uv run marimo edit` opens. Commit and push it before the next session.

    **What you write.** Code, in cells. Every number in your answer comes out of a cell, and none is typed into a sentence by hand. The question, the rule and the check go in markdown cells.

    **An answer looks like this:** `Groceries from March to August cost $1,284.50, or $214.08 a month.`

    **Done looks like this:**

    1. A markdown cell with the question.
    2. Your numbers in one list, and a second list of labels (months, dates, names) in the same order. One sentence in markdown says what a single number in your list stands for.
    3. One value that arrived broken, as text or with a symbol in it, such as `"n/a"` or `"$1,200"`. Run your calculation once with it in the list and write the last line of the error in your own words. Then choose a rule for that value, state it in markdown, and apply it in code: build a clean list with a `for` loop and an `if`, the way Keep Only Some does. Delete the cell that raised, so the notebook runs clean.
    4. Your answer as one sentence printed with an f-string, from the clean list, with the numbers formatted to two decimal places.
    5. **How I know these numbers are right**: one check done a different way, such as by hand, on a calculator, or in a second cell. In OIM6301 the check has to be a cell that runs.
    6. One number changed, and a note that names what updated by itself.

    **Where AI sits in this**

    | | |
    |---|---|
    | **By hand** | Nothing in this project |
    | **AI writes, you check** | Any line of code. Ask the agent in marimo's panel, which runs on your Babson key, and read each cell before you click **Keep cell** |
    | **You direct, you verify** | The check in point 5. Choose how to check the number, and explain why that check is independent |
    | **You choose the question** | The question, and the rule for the value that arrived broken |

    **The verification question.** Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell. If the agent got it right the first time: what did you do to verify that?

    > **Advanced**
    >
    > - Add a slider with `mo.ui.slider` that changes one assumption, and make your sentence follow it
    > - Draw your list as a bar chart with its labels, after running `uv add matplotlib`
    > - Answer a second question that needs something not covered yet, such as which month changed most from the one before, and explain the agent's line in your own words
    > - Send the notebook to somebody outside this course and write down the question they asked
    """)
    return


if __name__ == "__main__":
    app.run()

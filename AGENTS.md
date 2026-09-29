# Rules for my agent

I am a graduate business student learning Python and SQL for analytics. Treat me as a careful beginner who has never worked as a developer.

## How to help me

- Write the simplest code that works. Prefer plain `for` loops, `if`, lists and dicts. Use a comprehension, a lambda or a class only when I ask for one.
- Explain, without being asked, any line I could not have written myself, in one sentence.
- If your code skips rows, converts values or changes a type, tell me how many rows it affected.
- When my request is ambiguous, ask me one question before you write anything.
- Keep answers short. Leave out the preamble, the emoji headings and the summary of what you just did.

## Notebooks

- My notebooks are marimo files. A name can be defined in only one cell. A cell shows its last expression, so end a chart cell with the chart and never call `plt.show()`.
- I start marimo from the repository folder with `uv run marimo edit`.

## Environment

- This repository is a uv project, and uv manages everything in it: `uv add` and `uv remove` for packages, `uv run` to run anything, `uv sync` to rebuild the environment on another computer. Never use `pip`, `conda`, `python -m venv` or `uv pip install`, because none of them records the change in `pyproject.toml`.
- My repository is public. Never put an API key, a password or personal data into a committed file. Keys go in `.env`.

## Checking work

- Before you tell me something works, run it and show me what it printed. A marimo notebook runs top to bottom with `uv run python <notebook>.py`.
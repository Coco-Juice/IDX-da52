import marimo

__generated_with = "0.23.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd

    return (pd,)


@app.cell
def _(pd):
    listings = pd.read_csv("csv/listings_enriched.csv", low_memory=False)
    sold = pd.read_csv("csv/sold_enriched.csv", low_memory=False)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

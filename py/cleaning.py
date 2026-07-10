import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", 200)
    return mo, pd


@app.cell
def _(pd):
    listings = pd.read_csv("csv/listings_enriched.csv", low_memory=False)
    sold = pd.read_csv("csv/sold_enriched.csv", low_memory=False)
    return listings, sold


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, let's remove all the columns that have more than 60% of their values missing. These columns are mostly useless for the purposes of this data analysis project or have too much missing that it is not worth keeping or trying to impute.
    """)
    return


@app.cell
def _(listings):
    threshold = 0.6
    _missing_pct = listings.isna().mean()
    _cols_to_drop = _missing_pct[_missing_pct > threshold].index.tolist()
    print(f"Dropping {len(_cols_to_drop)} columns with >{threshold*100:.0f}% missing:")
    print(_cols_to_drop)
    listings_dropped = listings.drop(columns=_cols_to_drop)
    return listings_dropped, threshold


@app.cell
def _(listings_dropped, pd):
    listings_missing_summary = pd.DataFrame({
        "Missing Count": listings_dropped.isna().sum(),
        "Missing %": (listings_dropped.isna().mean() * 100).round(2)
    })

    print(listings_missing_summary.sort_values("Missing %", ascending=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Do the same thing with sold.
    """)
    return


@app.cell
def _(sold, threshold):
    _missing_pct = sold.isna().mean()
    _cols_to_drop = _missing_pct[_missing_pct > threshold].index.tolist()
    print(f"Dropping {len(_cols_to_drop)} columns with >{threshold*100:.0f}% missing:")
    print(_cols_to_drop)
    sold_dropped = sold.drop(columns=_cols_to_drop)
    return (sold_dropped,)


@app.cell
def _(pd, sold_dropped):
    sold_missing_summary = pd.DataFrame({
        "Missing Count": sold_dropped.isna().sum(),
        "Missing %": (sold_dropped.isna().mean() * 100).round(2)
    })

    print(sold_missing_summary.sort_values("Missing %", ascending=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's remove buyer and listing agent related columns since we care about real estate, not the agents.
    """)
    return


@app.cell
def _(listings_dropped):
    _agent_cols = [
        "BuyerAgencyCompensation", "BuyerAgencyCompensationType",
        "BuyerAgentFirstName", "BuyerAgentLastName", "BuyerAgentMlsId",
        "BuyerOfficeAOR", "BuyerOfficeName", "CoBuyerAgentFirstName",
        "CoListAgentFirstName", "CoListAgentLastName", "CoListOfficeName",
        "ListAgentEmail", "ListAgentFirstName", "ListAgentFullName",
        "ListAgentLastName", "ListOfficeName", "ListingKey", "Unnamed: 0",
        "ListingKeyNumeric", "ListingId", 
    ]
    _cols_present = [c for c in _agent_cols if c in listings_dropped.columns]
    print(f"Removing {len(_cols_present)} agent columns from listings:")
    print(_cols_present)
    listings_clean = listings_dropped.drop(columns=_cols_present)

    print("\n", listings_clean.columns)
    return


@app.cell
def _(sold_dropped):
    _agent_cols = [
        "BuyerAgencyCompensation", "BuyerAgencyCompensationType",
        "BuyerAgentFirstName", "BuyerAgentLastName", "BuyerAgentMlsId",
        "BuyerAgentAOR", "BuyerOfficeAOR", "BuyerOfficeName",
        "CoBuyerAgentFirstName",
        "CoListAgentFirstName", "CoListAgentLastName", "CoListOfficeName",
        "ListAgentEmail", "ListAgentFirstName", "ListAgentFullName",
        "ListAgentLastName", "ListAgentAOR", "ListOfficeName", "Unnamed: 0",
        "ListingKey", "ListingKeyNumeric", "ListingId"
    ]
    _cols_present = [c for c in _agent_cols if c in sold_dropped.columns]
    print(f"Removing {len(_cols_present)} agent columns from sold:")
    print(_cols_present)
    sold_clean = sold_dropped.drop(columns=_cols_present)

    print("\n", sold_clean.columns)
    return


if __name__ == "__main__":
    app.run()

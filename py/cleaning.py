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

    Let's also remove buyer and listing agent related columns since we care about real estate, not the agents.

    Next let's remove columns that are redundant, namely UnparsedAddress and StreetNumberNumeric (Longitude and Latitude does the same job), LotSizeAcres and LotSizeSquareFeet (redundant with LotSizeArea, which is the same unit of measurement as LivingArea), and PropertyType (all remaining properties are Residential)
    """)
    return


@app.cell
def _(listings):
    threshold = 0.6
    _missing_pct = listings.isna().mean()
    _cols_to_drop = _missing_pct[_missing_pct > threshold].index.tolist()
    print(f"Dropping {len(_cols_to_drop)} columns with >{threshold*100:.0f}% missing:")
    print(_cols_to_drop, '\n')
    listings_dropped = listings.drop(columns=_cols_to_drop)

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
    print(_cols_present, '\n')
    listings_dropped = listings_dropped.drop(columns=_cols_present)

    _redundant_cols = ["UnparsedAddress", "StreetNumberNumeric", "LotSizeAcres", "LotSizeSquareFeet", "PropertyType"]
    listings_dropped = listings_dropped.drop(columns=_redundant_cols)
    print(f"Removed redundant columns from listings:")
    print(_redundant_cols, '\n')

    print("\n", listings_dropped.columns)
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
    print(_cols_to_drop, '\n')
    sold_dropped = sold.drop(columns=_cols_to_drop)

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
    print(_cols_present, '\n')
    sold_dropped = sold_dropped.drop(columns=_cols_present)

    _redundant_cols = ["UnparsedAddress", "StreetNumberNumeric", "LotSizeAcres", "LotSizeSquareFeet", "PropertyType"]
    sold_dropped = sold_dropped.drop(columns=_redundant_cols)
    print(f"Removed redundant columns from sold:")
    print(_redundant_cols, '\n')

    print("\n", sold_dropped.columns)
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
    Now let's filter to only California properties and remove rows with YearBuilt above 2026.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's remove rows with invalid numeric values: non-positive prices/areas, negative days on market, and negative bedrooms or bathrooms.

    Let's also filter to only California properties since that is the focus of this project, and also remove any properties that have YearBuilt above 2026
    """)
    return


@app.cell
def _(listings_dropped, sold_dropped):
    _before_listings = len(listings_dropped)
    _before_sold = len(sold_dropped)

    for col in ["LivingArea", "BedroomsTotal", "BathroomsFull", "DaysOnMarket", "ClosePrice"]:
        if col in listings_dropped.columns:
            listings_clean = listings_dropped[listings_dropped[col] > 0] if col != "DaysOnMarket" else listings_dropped[listings_dropped[col] >= 0]
        if col in sold_dropped.columns:
            sold_clean = sold_dropped[sold_dropped[col] > 0] if col != "DaysOnMarket" else sold_dropped[sold_dropped[col] >= 0]

    print(f"Invalid values filter (Listings): {_before_listings} -> {len(listings_clean)} rows")
    print(f"Invalid values filter (Sold): {_before_sold} -> {len(sold_clean)} rows\n")

    listings_clean = listings_clean[listings_clean["StateOrProvince"] == "CA"]
    sold_clean = sold_clean[sold_clean["StateOrProvince"] == "CA"]
    print(f"StateOrProvince filter (listings): {_before_listings} -> {len(listings_clean)}")
    print(f"StateOrProvince filter (sold): {_before_sold} -> {len(sold_clean)}\n")

    if "YearBuilt" in listings_clean.columns:
        _before = len(listings_clean)
        listings_clean = listings_clean[listings_clean["YearBuilt"] <= 2026]
        print(f"YearBuilt filter (listings): {_before} -> {len(listings_clean)}")
    if "YearBuilt" in sold_clean.columns:
        _before = len(sold_clean)
        sold_clean = sold_clean[sold_clean["YearBuilt"] <= 2026]
        print(f"YearBuilt filter (sold): {_before} -> {len(sold_clean)}")

    return


if __name__ == "__main__":
    app.run()

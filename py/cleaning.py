import marimo

__generated_with = "0.23.14"
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
    First let's change the date fields into datetime format
    """)
    return


@app.cell
def _(listings, pd, sold):
    date_cols = ["CloseDate", "PurchaseContractDate", "ListingContractDate", "ContractStatusChangeDate"]

    for _col in date_cols:
        if _col in listings.columns:
            listings[_col] = pd.to_datetime(listings[_col], errors="coerce")
        if _col in sold.columns:
            sold[_col] = pd.to_datetime(sold[_col], errors="coerce")

    print(listings[date_cols].dtypes)
    print(sold[date_cols].dtypes)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next let's validate the logical order of date fields: ListingContractDate should precede PurchaseContractDate, which should precede CloseDate.
    """)
    return


@app.cell
def _(listings, sold):
    for _df in [listings, sold]:
        _df["listing_after_close_flag"] = _df["ListingContractDate"] > _df["CloseDate"]
        _df["purchase_after_close_flag"] = _df["PurchaseContractDate"] > _df["CloseDate"]
        _df["negative_timeline_flag"] = _df["ListingContractDate"] > _df["PurchaseContractDate"]

    for _name, _df in [("listings", listings), ("sold", sold)]:
        print(f"{_name}:")
        print(f"  listing_after_close_flag: {_df['listing_after_close_flag'].sum()}")
        print(f"  purchase_after_close_flag: {_df['purchase_after_close_flag'].sum()}")
        print(f"  negative_timeline_flag: {_df['negative_timeline_flag'].sum()}")
        print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, let's remove all the columns that have more than 90% of their values missing, these columns have too much of their data missing that it's not worth trying to keep/impute missingness.

    Next let's remove columns that are redundant, namely UnparsedAddress and StreetNumberNumeric (Longitude and Latitude does the same job), LotSizeAcres and LotSizeSquareFeet (redundant with LotSizeArea, which is the same unit of measurement as LivingArea), PropertyType (all remaining properties are Residential), HighSchool (we have HighSchoolDistrict, and HighSchool has a much higher missing percentage), and ListAgentFirstName and ListAgentLastName (we already have ListAgentFullName).

    Let's also remove the columns that doesn't give us important information for the property, namely ListAgentEmail, ListingKeyNumeric, ListingKey, and ListingId.
    """)
    return


@app.cell
def _(listings):
    threshold = 0.9
    _missing_pct = listings.isna().mean()
    _cols_to_drop = _missing_pct[_missing_pct > threshold].index.tolist()
    print(f"Dropping {len(_cols_to_drop)} columns with >{threshold*100:.0f}% missing:")
    print(_cols_to_drop, '\n')
    listings_dropped = listings.drop(columns=_cols_to_drop)

    _redundant_cols = ["UnparsedAddress", "StreetNumberNumeric", "LotSizeAcres", "LotSizeSquareFeet", "PropertyType", "HighSchool",
                      "ListAgentFirstName", "ListAgentLastName"]
    listings_dropped = listings_dropped.drop(columns=_redundant_cols)
    print(f"Removed redundant columns from listings:")
    print(_redundant_cols, '\n')

    _unimportant_cols = ["ListAgentEmail", "ListingKeyNumeric", "ListingKey", "ListingId", "Unnamed: 0"]
    listings_dropped = listings_dropped.drop(columns=_unimportant_cols)
    print(f"Removed unimportant columns:")
    print(_unimportant_cols, '\n')

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

    _redundant_cols = ["UnparsedAddress", "StreetNumberNumeric", "LotSizeAcres", "LotSizeSquareFeet", "PropertyType", "HighSchool",
                      "ListAgentFirstName", "ListAgentLastName"]
    sold_dropped = sold_dropped.drop(columns=_redundant_cols)
    print(f"Removed redundant columns from sold:")
    print(_redundant_cols, '\n')

    _unimportant_cols = ["ListAgentEmail", "ListingKeyNumeric", "ListingKey", "ListingId", "Unnamed: 0"]
    sold_dropped = sold_dropped.drop(columns=_unimportant_cols)
    print(f"Removed unimportant columns:")
    print(_unimportant_cols, '\n')

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
    Now let's remove rows with invalid numeric values: non-positive prices/areas, negative days on market, and negative bedrooms or bathrooms.

    Let's also remove any properties that have YearBuilt above 2026 since they haven't been built yet.
    """)
    return


@app.cell
def _(listings_dropped, sold_dropped):
    _before_listings = len(listings_dropped)
    _before_sold = len(sold_dropped)

    listings_clean = listings_dropped.copy()
    sold_clean = sold_dropped.copy()

    for _col in ["LivingArea", "BedroomsTotal", "BathroomsTotalInteger", "DaysOnMarket"]:
        if _col in listings_clean.columns:
            _before = len(listings_clean)
            listings_clean = listings_clean[listings_clean[_col] > 0] if _col != "DaysOnMarket" else listings_clean[listings_clean[_col] >= 0]
            print(f"{_col} filter (listings): {_before} -> {len(listings_clean)}")
        if _col in sold_clean.columns:
            _before = len(sold_clean)
            sold_clean = sold_clean[sold_clean[_col] > 0] if _col != "DaysOnMarket" else sold_clean[sold_clean[_col] >= 0]
            print(f"{_col} filter (sold): {_before} -> {len(sold_clean)}")

    if "ClosePrice" in sold_clean.columns:
        _before = len(sold_clean)
        sold_clean = sold_clean[sold_clean["ClosePrice"] > 0]
        print(f"ClosePrice filter (sold): {_before} -> {len(sold_clean)}")

    print(f"\nInvalid values filter (Listings): {_before_listings} -> {len(listings_clean)} rows")
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
    return listings_clean, sold_clean


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's validate the geographic coordinates. We need to flag:
    - Records with missing coordinates (Latitude or Longitude is null)
    - Latitude = 0 or Longitude = 0 (sentinel null values)
    - Longitude > 0 errors (California coordinates should be negative)
    - Out-of-state or implausible coordinates (California bounds: 32.5°N to 42°N, -124.5°W to -114°W)
    """)
    return


@app.cell
def _(listings_clean, sold_clean):
    CA_LAT_MIN, CA_LAT_MAX = 32.5, 42.0
    CA_LON_MIN, CA_LON_MAX = -124.5, -114.0

    for _name, _df in [("listings", listings_clean), ("sold", sold_clean)]:
        _df["missing_coords_flag"] = _df["Latitude"].isna() | _df["Longitude"].isna()
        _df["sentinel_null_flag"] = (_df["Latitude"] == 0) | (_df["Longitude"] == 0)
        _df["lon_positive_flag"] = _df["Longitude"] > 0
        _df["out_of_bounds_flag"] = (
            (_df["Latitude"] < CA_LAT_MIN) | (_df["Latitude"] > CA_LAT_MAX) |
            (_df["Longitude"] < CA_LON_MIN) | (_df["Longitude"] > CA_LON_MAX)
        )
        _df["any_geo_issue"] = (
            _df["missing_coords_flag"] | _df["sentinel_null_flag"] |
            _df["lon_positive_flag"] | _df["out_of_bounds_flag"]
        )

        print(f"{_name} geographic data checks:")
        print(f"  Missing coordinates:  {_df['missing_coords_flag'].sum()}")
        print(f"  Sentinel null (0,0):  {_df['sentinel_null_flag'].sum()}")
        print(f"  Longitude > 0:        {_df['lon_positive_flag'].sum()}")
        print(f"  Out of CA bounds:     {_df['out_of_bounds_flag'].sum()}")
        print(f"  Total with issues:    {_df['any_geo_issue'].sum()}")
        print()
    return


if __name__ == "__main__":
    app.run()

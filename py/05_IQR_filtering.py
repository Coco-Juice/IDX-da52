import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", 200)
    return mo, pd


@app.cell
def _(pd):
    listings = pd.read_csv("csv/listings_engineered.csv", low_memory=False)
    sold = pd.read_csv("csv/sold_engineered.csv", low_memory=False)
    return listings, sold


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's remove records from listings and sold that fall outside of the interquartile range (IQR). This is to remove outliers that skew statistical measures and misrepresent the typical market.

    The dataframe with the records removed will be saved as separate csvs so that if we want to change anything we can come back and change the method of removing outliers.
    """)
    return


@app.cell
def _(listings):
    columns = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
    listings_cleaned = listings.copy()

    for _col in columns:
        _Q1 = listings[_col].quantile(0.25)
        _Q3 = listings[_col].quantile(0.75)
        _IQR = _Q3 - _Q1
        _lower = _Q1 - 1.5 * _IQR
        _upper = _Q3 + 1.5 * _IQR
        listings_cleaned = listings_cleaned[listings_cleaned[_col].between(_lower, _upper) | listings_cleaned[_col].isna()]

    print('Listings dataframe shape before:', listings.shape)
    print('Listings dataframe shape after:', listings_cleaned.shape)

    for _col in columns:
        print('Listings median', _col, 'value before:', listings[_col].median())
        print('Listings median', _col, 'value after:', listings_cleaned[_col].median())
    return columns, listings_cleaned


@app.cell
def _(columns, sold):
    sold_cleaned = sold.copy()

    for _col in columns:
        _Q1 = sold[_col].quantile(0.25)
        _Q3 = sold[_col].quantile(0.75)
        _IQR = _Q3 - _Q1
        _lower = _Q1 - 1.5 * _IQR
        _upper = _Q3 + 1.5 * _IQR
        sold_cleaned = sold_cleaned[sold_cleaned[_col].between(_lower, _upper) | sold_cleaned[_col].isna()]

    print('Sold dataframe shape before:', sold.shape)
    print('Sold dataframe shape after:', sold_cleaned.shape)

    for _col in columns:
        print('Sold median', _col, 'value before:', sold[_col].median())
        print('Sold median', _col, 'value after:', sold_cleaned[_col].median())
    return (sold_cleaned,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Save the filtered csvs separately.
    """)
    return


@app.cell
def _(listings_cleaned, sold_cleaned):
    listings_cleaned.to_csv('csv/listings_filtered.csv')
    sold_cleaned.to_csv('csv/sold_filtered.csv')
    return


if __name__ == "__main__":
    app.run()

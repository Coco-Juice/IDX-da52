import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", 200)
    return (pd,)


@app.cell
def _(pd):
    listings = pd.read_csv("csv/listings_cleaned.csv", low_memory=False)
    sold = pd.read_csv("csv/sold_cleaned.csv", low_memory=False)
    return listings, sold


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


@app.cell
def _(listings, sold):
    listings['price_ratio'] = listings['ClosePrice'] / listings['OriginalListPrice']
    listings['price_per_sqft'] = listings['ClosePrice'] / listings['LivingArea']
    listings['listing_to_contract'] = listings['PurchaseContractDate'] - listings['ListingContractDate']
    listings['contract_to_close'] = listings['CloseDate'] - listings['PurchaseContractDate']

    sold['price_ratio'] = sold['ClosePrice'] / sold['OriginalListPrice']
    sold['price_per_sqft'] = sold['ClosePrice'] / sold['LivingArea']
    sold['listing_to_contract'] = sold['PurchaseContractDate'] - sold['ListingContractDate']
    sold['contract_to_close'] = sold['CloseDate'] - sold['PurchaseContractDate']
    return


@app.cell
def _(sold):
    features = ['price_ratio', 'price_per_sqft', 'listing_to_contract', 'contract_to_close']
    groups = ['PropertySubType', 'CountyOrParish', 'MLSAreaMajor', 'ListOfficeName', 'BuyerOfficeName']

    for _group in groups:
        for _feat in features:
            sold.groupby(_group)[[_feat]].describe().to_csv(f"describe/sold_{_group} & {_feat}.csv")
    return features, groups


@app.cell
def _(features, groups, listings):
    for _group in groups:
        for _feat in features:
            listings.groupby(_group)[[_feat]].describe().to_csv(f"describe/listings_{_group} & {_feat}.csv")
    return


@app.cell
def _(listings, sold):
    listings.to_csv('csv/listings_engineered.csv')
    sold.to_csv('csv/sold_engineered.csv')
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

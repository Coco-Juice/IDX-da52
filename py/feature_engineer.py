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
    return np, pd


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
def _(listings, np, pd, sold):
    features = ['price_ratio', 'price_per_sqft', 'listing_to_contract', 'contract_to_close']

    for _name, _df in [("listings", listings), ("sold", sold)]:
        print(f"\n{'=' * 80}")
        print(f"  {_name.upper()} — Percentile Summaries")
        print(f"{'=' * 80}")
    
        for _f in features:
            if _f not in _df.columns:
                continue
            
            _col = _df[_f].dropna()
        
            if len(_col) == 0:
                print(f"\n  {_f}: (no non-null values)")
                continue

            # If column is timedelta / duration data, convert to numeric days
            if pd.api.types.is_timedelta64_dtype(_col):
                _col = _col.dt.total_seconds() / 86400.0

            _p = np.percentile(_col, [1, 5, 25, 50, 75, 95, 99])
        
            print(f"\n  {_f}  (n={len(_col):,})")
            print(f"    Min:      {_col.min():>15,.2f}")
            print(f"    P1:       {_p[0]:>15,.2f}")
            print(f"    P5:       {_p[1]:>15,.2f}")
            print(f"    P25:      {_p[2]:>15,.2f}")
            print(f"    Median:   {_p[3]:>15,.2f}")
            print(f"    Mean:     {_col.mean():>15,.2f}")
            print(f"    P75:      {_p[4]:>15,.2f}")
            print(f"    P95:      {_p[5]:>15,.2f}")
            print(f"    P99:      {_p[6]:>15,.2f}")
            print(f"    Max:      {_col.max():>15,.2f}")
            print(f"    Std:      {_col.std():>15,.2f}")
    return


if __name__ == "__main__":
    app.run()

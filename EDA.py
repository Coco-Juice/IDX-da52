import marimo

__generated_with = "0.23.11"
app = marimo.App(width="full")


@app.cell
def _():
    import pandas as pd

    return (pd,)


@app.cell
def _(pd):
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", 200)
    return


@app.cell
def _():
    MARKET_FIELDS = {
        "Price": [
            "OriginalListPrice", "ListPrice", "ClosePrice",
            "BuyerAgencyCompensation", "BuyerAgencyCompensationType",
        ],
        "Property": [
            "PropertyType", "PropertySubType", "MlsStatus",
        ],
        "Size": [
            "LivingArea", "LotSizeAcres", "LotSizeArea", "LotSizeSquareFeet",
            "BuildingAreaTotal", "AboveGradeFinishedArea", "BelowGradeFinishedArea",
            "LotSizeDimensions",
        ],
        "Rooms": [
            "BedroomsTotal", "BathroomsTotalInteger", "MainLevelBedrooms",
        ],
        "Age": [
            "YearBuilt", "NewConstructionYN",
        ],
        "Features": [
            "FireplacesTotal", "FireplaceYN", "Stories", "Levels",
            "GarageSpaces", "CoveredSpaces", "ParkingTotal",
            "AttachedGarageYN", "PoolPrivateYN", "ViewYN",
            "WaterfrontYN", "BasementYN", "Flooring",
        ],
        "Location": [
            "City", "CountyOrParish", "PostalCode", "StateOrProvince",
            "MLSAreaMajor", "Latitude", "Longitude", "SubdivisionName",
        ],
        "Schools": [
            "ElementarySchool", "MiddleOrJuniorSchool", "HighSchool",
            "HighSchoolDistrict", "ElementarySchoolDistrict",
            "MiddleOrJuniorSchoolDistrict",
        ],
        "Timing": [
            "DaysOnMarket", "CloseDate", "ListingContractDate",
            "PurchaseContractDate", "ContractStatusChangeDate",
        ],
        "Financial": [
            "TaxAnnualAmount", "TaxYear", "AssociationFee",
            "AssociationFeeFrequency",
        ],
    }
    METADATA_FIELDS = {
        "System_IDs": [
            "ListingKey", "ListingKeyNumeric", "ListingId",
        ],
        "System_Source": [
            "OriginatingSystemName", "OriginatingSystemSubName",
        ],
        "Agent": [
            "ListAgentEmail", "ListAgentFirstName", "ListAgentLastName",
            "ListAgentFullName",
        ],
        "Co_Agent": [
            "CoListAgentFirstName", "CoListAgentLastName",
        ],
        "Buyer_Agent": [
            "BuyerAgentMlsId", "BuyerAgentFirstName", "BuyerAgentLastName",
            "BuyerAgentAOR", "CoBuyerAgentFirstName",
        ],
        "Office": [
            "ListOfficeName", "BuyerOfficeName",
            "CoListOfficeName", "BuyerOfficeAOR", "ListAgentAOR",
        ],
        "Address": [
            "UnparsedAddress", "StreetNumberNumeric",
        ],
        "Builder": [
            "BuilderName",
        ],
    }
    ALL_MARKET = {c for g in MARKET_FIELDS.values() for c in g}
    ALL_META = {c for g in METADATA_FIELDS.values() for c in g}
    return ALL_MARKET, ALL_META, MARKET_FIELDS, METADATA_FIELDS


@app.cell
def _(pd):
    listings = pd.read_csv("csv/listings.csv", low_memory=False)
    sold = pd.read_csv("csv/sold.csv", low_memory=False)
    return listings, sold


@app.cell
def _(ALL_MARKET, ALL_META, listings, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        _rows, _cols = _df.shape
        _market_cols = [c for c in _df.columns if c in ALL_MARKET]
        _meta_cols = [c for c in _df.columns if c in ALL_META]

        print(f"\n{'=' * 80}")
        print(f"  {_name.upper()}  (csv/{_name}.csv)")
        print(f"{'=' * 80}\n")
        print(f"Rows: {_rows:,}  |  Columns: {_cols}")
        print(f"Market analysis fields: {len(_market_cols)}")
        print(f"Metadata fields:         {len(_meta_cols)}")

        _unaccounted = [c for c in _df.columns if c not in ALL_MARKET and c not in ALL_META]
        if _unaccounted:
            print(f"Unclassified:             {len(_unaccounted)} -> {_unaccounted}")
    return


@app.cell
def _(listings, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        print(f"\n--- {_name.upper()} Data Types ---")
        for _dt, _cnt in _df.dtypes.value_counts().items():
            print(f"  {_dt}: {_cnt}")
    return


@app.cell
def _(listings, sold):
    _FLAG_AT = 90
    for _name, _df in [("listings", listings), ("sold", sold)]:
        _total = len(_df)
        _miss_count = _df.isnull().sum()
        _miss_pct = (_miss_count / _total * 100).round(2)
        _summary = _miss_pct.sort_values(ascending=False)

        print(f"\n--- {_name.upper()} Missing Values (all columns) ---")
        print(f"{'Column':50s} {'Missing #':>12s} {'Missing %':>10s}  Flag")
        print("-" * 78)
        for _c, _pct in _summary.items():
            _cnt = _miss_count[_c]
            _flag = "  >90%" if _pct > _FLAG_AT else ""
            print(f"{_c:50s} {_cnt:>12,} {_pct:>9.2f}% {_flag}")

        _severe = _summary[_summary > _FLAG_AT]
        print(f"\n>>> Columns with >{_FLAG_AT}% missing ({len(_severe)}):")
        if len(_severe):
            for _c, _pct in _severe.items():
                _cnt = _miss_count[_c]
                print(f"    {_c:50s} {_cnt:>12,} ({_pct:.2f}%)")
        else:
            print("    (none)")
    return


@app.cell
def _(MARKET_FIELDS, listings, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        print(f"\n--- {_name.upper()} Market Analysis Fields ---")
        for _group, _fields in MARKET_FIELDS.items():
            _present = [f for f in _fields if f in _df.columns]
            if _present:
                print(f"  [{_group}]")
                for _f in _present:
                    _mp = _df[_f].isnull().mean() * 100
                    print(f"    {_f:42s}  dtype={_df[_f].dtype}  missing={_mp:.2f}%")
    return


@app.cell
def _(METADATA_FIELDS, listings, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        print(f"\n--- {_name.upper()} Metadata Fields ---")
        for _group, _fields in METADATA_FIELDS.items():
            _present = [f for f in _fields if f in _df.columns]
            if _present:
                print(f"  [{_group}]")
                for _f in _present:
                    _mp = _df[_f].isnull().mean() * 100
                    print(f"    {_f:42s}  dtype={_df[_f].dtype}  missing={_mp:.2f}%")
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np

    return np, plt


@app.cell
def _():
    NUMERIC_FIELDS = [
        "ClosePrice", "ListPrice", "OriginalListPrice",
        "LivingArea", "LotSizeAcres",
        "BedroomsTotal", "BathroomsTotalInteger",
        "DaysOnMarket", "YearBuilt",
    ]
    return (NUMERIC_FIELDS,)


@app.cell
def _(NUMERIC_FIELDS, listings, np, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        print(f"\n{'=' * 80}")
        print(f"  {_name.upper()} — Percentile Summaries")
        print(f"{'=' * 80}")
        for _f in NUMERIC_FIELDS:
            if _f not in _df.columns:
                continue
            _col = _df[_f].dropna()
            if len(_col) == 0:
                print(f"\n  {_f}: (no non-null values)")
                continue
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


@app.cell
def _(NUMERIC_FIELDS, listings, np, plt, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        _present = [f for f in NUMERIC_FIELDS if f in _df.columns and _df[f].notna().sum() > 0]
        if not _present:
            continue
        _ncols = 3
        _nrows = int(np.ceil(len(_present) / _ncols))

        _fig, _axes = plt.subplots(_nrows, _ncols, figsize=(5 * _ncols, 4 * _nrows))
        _axes = _axes.flatten()
        _fig.suptitle(f"{_name.upper()} — Histograms", fontsize=14, y=1.02)

        for _i, _f in enumerate(_present):
            _col = _df[_f].dropna()
            _ax = _axes[_i]
            _ax.hist(_col, bins=80, color="steelblue", edgecolor="white", linewidth=0.3)
            _ax.set_title(f"{_f}\n(n={len(_col):,})", fontsize=9)
            _ax.ticklabel_format(style="sci", axis="x", scilimits=(0, 0))
            _ax.tick_params(axis="x", rotation=45, labelsize=7)

        for _j in range(_i + 1, len(_axes)):
            _fig.delaxes(_axes[_j])

        _fig.tight_layout()
        plt.show()
    return


@app.cell
def _(NUMERIC_FIELDS, listings, np, plt, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        _present = [f for f in NUMERIC_FIELDS if f in _df.columns and _df[f].notna().sum() > 0]
        if not _present:
            continue
        _ncols = 3
        _nrows = int(np.ceil(len(_present) / _ncols))

        _fig, _axes = plt.subplots(_nrows, _ncols, figsize=(5 * _ncols, 4 * _nrows))
        _axes = _axes.flatten()
        _fig.suptitle(f"{_name.upper()} — Boxplots", fontsize=14, y=1.02)

        for _i, _f in enumerate(_present):
            _col = _df[_f].dropna()
            _ax = _axes[_i]
            _ax.boxplot(_col, orientation="horizontal", patch_artist=True,
                       boxprops=dict(facecolor="lightsteelblue"),
                       medianprops=dict(color="red"))
            _ax.set_title(f"{_f}\n(n={len(_col):,})", fontsize=9)
            _ax.ticklabel_format(style="sci", axis="x", scilimits=(0, 0))
            _ax.tick_params(axis="x", labelsize=7)

        for _j in range(_i + 1, len(_axes)):
            _fig.delaxes(_axes[_j])

        _fig.tight_layout()
        plt.show()
    return


@app.cell
def _(NUMERIC_FIELDS, listings, np, plt, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        _present = [f for f in NUMERIC_FIELDS if f in _df.columns and _df[f].notna().sum() > 0]
        if not _present:
            continue
        _ncols = 3
        _nrows = int(np.ceil(len(_present) / _ncols))

        _fig, _axes = plt.subplots(_nrows, _ncols, figsize=(5 * _ncols, 4 * _nrows))
        _axes = _axes.flatten()
        _fig.suptitle(f"{_name.upper()} — Histograms (outliers removed: P1–P99)", fontsize=14, y=1.02)

        for _i, _f in enumerate(_present):
            _col = _df[_f].dropna()
            _lo, _hi = np.percentile(_col, [1, 99])
            _clean = _col[(_col >= _lo) & (_col <= _hi)]
            _ax = _axes[_i]
            _ax.hist(_clean, bins=80, color="seagreen", edgecolor="white", linewidth=0.3)
            _ax.set_title(f"{_f}\n(n={len(_clean):,}  removed={len(_col)-len(_clean):,})", fontsize=9)
            _ax.ticklabel_format(style="sci", axis="x", scilimits=(0, 0))
            _ax.tick_params(axis="x", rotation=45, labelsize=7)

        for _j in range(_i + 1, len(_axes)):
            _fig.delaxes(_axes[_j])

        _fig.tight_layout()
        plt.show()
    return


@app.cell
def _(NUMERIC_FIELDS, listings, np, sold):
    _IQR_MULT = 3.0
    for _name, _df in [("listings", listings), ("sold", sold)]:
        print(f"\n{'=' * 80}")
        print(f"  {_name.upper()} — Extreme Outliers (>{_IQR_MULT}× IQR or beyond P1–P99)")
        print(f"{'=' * 80}")
        for _f in NUMERIC_FIELDS:
            if _f not in _df.columns:
                continue
            _col = _df[_f].dropna()
            if len(_col) == 0:
                continue
            _q1, _q3 = _col.quantile([0.25, 0.75])
            _iqr = _q3 - _q1
            _lo_iqr = _q1 - _IQR_MULT * _iqr
            _hi_iqr = _q3 + _IQR_MULT * _iqr
            _p1, _p99 = np.percentile(_col, [1, 99])
            _lo = min(_lo_iqr, _p1)
            _hi = max(_hi_iqr, _p99)
            _outliers = _col[(_col < _lo) | (_col > _hi)]
            _pct = len(_outliers) / len(_col) * 100
            print(f"\n  {_f:30s}  outliers={len(_outliers):>6,}  ({_pct:.2f}%)")
            if len(_outliers) > 0:
                print(f"    Range: [{_col.min():,.2f}, {_col.max():,.2f}]")
                print(f"    Bounds: <{_lo:,.2f}  or  >{_hi:,.2f}")
                print(f"    Min outlier: {_outliers.min():,.2f}")
                print(f"    Max outlier: {_outliers.max():,.2f}")
    return


@app.cell
def _(sold):
    _both = sold[["ClosePrice", "ListPrice"]].dropna()
    _ratio = _both["ClosePrice"] / _both["ListPrice"]
    _above = (_ratio > 1.005).sum()
    _below = (_ratio < 0.995).sum()
    _at = len(_ratio) - _above - _below
    _total = len(_ratio)

    print("=" * 80)
    print("  SOLD — Close Price vs List Price")
    print("=" * 80)
    print(f"  Sold above list price (>0.5% over):   {_above:>8,}  ({_above/_total*100:5.2f}%)")
    print(f"  Sold at list price (±0.5%):           {_at:>8,}  ({_at/_total*100:5.2f}%)")
    print(f"  Sold below list price (>0.5% under):  {_below:>8,}  ({_below/_total*100:5.2f}%)")
    print(f"  Total with both prices:               {_total:>8,}")
    print(f"  Mean close/list ratio:                {_ratio.mean():.4f}")
    print(f"  Median close/list ratio:              {_ratio.median():.4f}")
    return


@app.cell
def _(listings, pd, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        print(f"\n{'=' * 80}")
        print(f"  {_name.upper()} — Date Consistency Checks")
        print(f"{'=' * 80}")

        _has_close = "CloseDate" in _df.columns and "ListingContractDate" in _df.columns
        _has_purchase = "PurchaseContractDate" in _df.columns
        _has_listing = "ListingContractDate" in _df.columns

        if _has_close:
            _cd = pd.to_datetime(_df["CloseDate"], errors="coerce")
            _ld = pd.to_datetime(_df["ListingContractDate"], errors="coerce")
            _both_dates = _cd.notna() & _ld.notna()
            _close_before_listing = (_cd < _ld) & _both_dates
            print(f"\n  CloseDate < ListingContractDate:  {_close_before_listing.sum():>8,}  ({_close_before_listing.sum()/_both_dates.sum()*100:.2f}%)")
            if _close_before_listing.sum() > 0:
                _worst = (_ld - _cd).loc[_close_before_listing].max()
                print(f"    Worst gap (listing - close):     {_worst.days} days")

        if _has_listing and _has_purchase:
            _ld = pd.to_datetime(_df["ListingContractDate"], errors="coerce")
            _pd = pd.to_datetime(_df["PurchaseContractDate"], errors="coerce")
            _both_p = _ld.notna() & _pd.notna()
            _purchase_before_listing = (_pd < _ld) & _both_p
            if _purchase_before_listing.sum() > 0 or True:
                print(f"\n  PurchaseContractDate < ListingContractDate:  {_purchase_before_listing.sum():>8,}  ({_purchase_before_listing.sum()/_both_p.sum()*100:.2f}%)")

        if "DaysOnMarket" in _df.columns and _has_listing and _has_close:
            _dom = _df["DaysOnMarket"]
            _calc_dom = (_cd - _ld).dt.days
            _both_dom = _dom.notna() & _calc_dom.notna()
            _diff = (_dom - _calc_dom.abs()).abs()
            _mismatch = (_diff > 1) & _both_dom
            print(f"\n  DaysOnMarket mismatches (>1 day):  {_mismatch.sum():>8,}  ({_mismatch.sum()/_both_dom.sum()*100:.2f}%)")
    return


@app.cell
def _(listings, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        _price_col = "ClosePrice" if _name == "sold" else "ListPrice"
        if _price_col not in _df.columns:
            continue
        _g = _df.groupby("CountyOrParish")[_price_col].agg(["median", "mean", "count"]).sort_values("median", ascending=False)
        _g.columns = ["Median Price", "Mean Price", "Count"]

        print(f"\n{'=' * 80}")
        print(f"  {_name.upper()} — Top 20 Counties by Median {_price_col}")
        print(f"{'=' * 80}")
        print(f"  {'County':30s}  {'Median':>12s}  {'Mean':>14s}  {'Count':>8s}")
        print(f"  {'-'*30}  {'-'*12}  {'-'*14}  {'-'*8}")
        for _county, _row in _g.head(20).iterrows():
            _m = f"${_row['Median Price']:,.0f}"
            _a = f"${_row['Mean Price']:,.0f}"
            print(f"  {_county:30s}  {_m:>12s}  {_a:>14s}  {_row['Count']:>8,}")

        _low = _g.tail(5).iloc[::-1]
        print(f"\n  Bottom 5 counties:")
        print(f"  {'County':30s}  {'Median':>12s}  {'Mean':>14s}  {'Count':>8s}")
        print(f"  {'-'*30}  {'-'*12}  {'-'*14}  {'-'*8}")
        for _county, _row in _low.iterrows():
            _m = f"${_row['Median Price']:,.0f}"
            _a = f"${_row['Mean Price']:,.0f}"
            print(f"  {_county:30s}  {_m:>12s}  {_a:>14s}  {_row['Count']:>8,}")
    return


@app.cell
def _(listings, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        _price_col = "ClosePrice" if _name == "sold" else "ListPrice"
        if _price_col not in _df.columns:
            continue
        _df = _df[_df["LivingArea"] > 0]
        _df["PricePerSqft"] = _df[_price_col] / _df["LivingArea"]
        _p = _df["PricePerSqft"]
        print(f"\n{'=' * 80}")
        print(f"  {_name.upper()} — Price per SqFt Overview")
        print(f"{'=' * 80}")
        print(f"  Median: ${_p.median():,.0f}  Mean: ${_p.mean():,.0f}  P1: ${_p.quantile(0.01):,.0f}  P99: ${_p.quantile(0.99):,.0f}")

        print(f"\n  Top 10 counties by median $/sqft:")
        _g = _df.groupby("CountyOrParish")["PricePerSqft"].agg(["median", "mean", "count"]).sort_values("median", ascending=False)
        for _county, _row in _g.head(10).iterrows():
            print(f"    {_county:25s}  ${_row['median']:>7,.0f}/sqft  mean=${_row['mean']:>7,.0f}  n={_row['count']:,}")

        print(f"\n  By property subtype (top 10):")
        _g2 = _df.groupby("PropertySubType")["PricePerSqft"].agg(["median", "mean", "count"]).sort_values("median", ascending=False)
        for _sub, _row in _g2.head(10).iterrows():
            print(f"    {_sub:30s}  ${_row['median']:>7,.0f}/sqft  mean=${_row['mean']:>7,.0f}  n={_row['count']:,}")

        print(f"\n  By bedrooms:")
        _g3 = _df.groupby("BedroomsTotal")["PricePerSqft"].agg(["median", "mean", "count"])
        for _beds, _row in _g3.iterrows():
            if _row["count"] > 100:
                print(f"    {_beds:2.0f} beds  ${_row['median']:>7,.0f}/sqft  mean=${_row['mean']:>7,.0f}  n={_row['count']:,}")
    return


@app.cell
def _(listings, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        _price_col = "ClosePrice" if _name == "sold" else "ListPrice"
        if _price_col not in _df.columns or "OriginalListPrice" not in _df.columns:
            continue
        _both = _df[[_price_col, "OriginalListPrice"]].dropna()
        _both["DropPct"] = (_both["OriginalListPrice"] - _both[_price_col]) / _both["OriginalListPrice"] * 100
        _dropped = _both[_both["DropPct"] > 1]
        _increased = _both[_both["DropPct"] < -1]
        _unchanged = _both[abs(_both["DropPct"]) <= 1]

        print(f"\n{'=' * 80}")
        print(f"  {_name.upper()} — Price Drop Analysis (OriginalListPrice vs {_price_col})")
        print(f"{'=' * 80}")
        print(f"  Price decreased (>1%):     {len(_dropped):>8,}  ({len(_dropped)/len(_both)*100:.1f}%)")
        print(f"  Unchanged (±1%):           {len(_unchanged):>8,}  ({len(_unchanged)/len(_both)*100:.1f}%)")
        print(f"  Price increased (>1%):     {len(_increased):>8,}  ({len(_increased)/len(_both)*100:.1f}%)")
        if len(_dropped) > 0:
            print(f"  Avg drop among reduced:    {_dropped['DropPct'].mean():.1f}%")
            print(f"  Median drop:               {_dropped['DropPct'].median():.1f}%")
        if _name == "listings":
            _current = _df[["ListPrice", "OriginalListPrice"]].dropna()
            _current["DropPct"] = (_current["OriginalListPrice"] - _current["ListPrice"]) / _current["OriginalListPrice"] * 100
            _curr_dropped = _current[_current["DropPct"] > 1]
            print(f"\n  Current ListPrice vs Original (active listings):")
            print(f"    Reduced: {len(_curr_dropped):,} ({len(_curr_dropped)/len(_current)*100:.1f}%)")
            if len(_curr_dropped) > 0:
                print(f"    Avg reduction: {_curr_dropped['DropPct'].mean():.1f}%  Median: {_curr_dropped['DropPct'].median():.1f}%")
    return


@app.cell
def _(listings, pd, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        _price_col = "ClosePrice" if _name == "sold" else "ListPrice"
        if _price_col not in _df.columns:
            continue
        _d = _df[_df["DaysOnMarket"].notna() & _df[_price_col].notna()].copy()
        _d["PriceTier"] = pd.qcut(_d[_price_col], q=5, labels=["Very Low", "Low", "Mid", "High", "Very High"])
        print(f"\n{'=' * 80}")
        print(f"  {_name.upper()} — DaysOnMarket by Price Tier")
        print(f"{'=' * 80}")
        print(f"  {'Tier':12s}  {'Median DOM':>10s}  {'Mean DOM':>10s}  {'Count':>8s}")
        for _tier in ["Very Low", "Low", "Mid", "High", "Very High"]:
            _sub = _d[_d["PriceTier"] == _tier]
            print(f"  {_tier:12s}  {_sub['DaysOnMarket'].median():>10.1f}  {_sub['DaysOnMarket'].mean():>10.1f}  {len(_sub):>8,}")
    return


@app.cell
def _(listings, pd, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        _date_col = "CloseDate" if _name == "sold" else "ListingContractDate"
        _price_col = "ClosePrice" if _name == "sold" else "ListPrice"
        if _date_col not in _df.columns:
            continue
        _d = _df[_df[_date_col].notna()].copy()
        _d["Month"] = pd.to_datetime(_d[_date_col], errors="coerce").dt.month
        _d = _d[_d["Month"].notna()]

        print(f"\n{'=' * 80}")
        print(f"  {_name.upper()} — Monthly Volume & Median {_price_col}")
        print(f"{'=' * 80}")
        print(f"  {'Month':10s}  {'Count':>8s}  {'Median Price':>14s}")
        _month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for _m in range(1, 13):
            _sub = _d[_d["Month"] == _m]
            if len(_sub) == 0:
                continue
            _p = _sub[_price_col].median() if _price_col in _sub.columns else 0
            _m_label = _month_names[_m - 1]
            _p_str = f"${_p:,.0f}" if _p else "N/A"
            print(f"  {_m_label:10s}  {len(_sub):>8,}  {_p_str:>14s}")
    return


@app.cell
def _(sold):
    _d = sold.copy()
    _features = {
        "Pool": "PoolPrivateYN",
        "Fireplace": "FireplaceYN",
        "View": "ViewYN",
        "Waterfront": "WaterfrontYN",
        "Basement": "BasementYN",
    }
    print(f"\n{'=' * 80}")
    print(f"  SOLD — Feature Price Lift (median ClosePrice)")
    print(f"{'=' * 80}")
    print(f"  {'Feature':15s}  {'With':>14s}  {'Without':>14s}  {'Lift':>10s}  {'Count With':>10s}")
    for _label, _col in _features.items():
        if _col not in _d.columns:
            continue
        _with = _d[_d[_col] == True]["ClosePrice"].dropna()
        _without = _d[_d[_col] == False]["ClosePrice"].dropna()
        if len(_with) < 10 or len(_without) < 10:
            continue
        _lift = (_with.median() / _without.median() - 1) * 100
        _w = f"${_with.median():,.0f}"
        _wo = f"${_without.median():,.0f}"
        print(f"  {_label:15s}  {_w:>14s}  {_wo:>14s}  {_lift:>+9.1f}%  {len(_with):>10,}")
    return


@app.cell
def _(listings, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        _price_col = "ClosePrice" if _name == "sold" else "ListPrice"
        _d = _df[_df["NewConstructionYN"].notna() & _df[_price_col].notna()]

        print(f"\n{'=' * 80}")
        print(f"  {_name.upper()} — New Construction vs Existing")
        print(f"{'=' * 80}")
        for _val, _label in [(True, "New Construction"), (False, "Existing")]:
            _sub = _d[_d["NewConstructionYN"] == _val]
            print(f"  {_label:20s}  n={len(_sub):>7,}  median=${_sub[_price_col].median():>9,.0f}  mean=${_sub[_price_col].mean():>9,.0f}  median DOM={_sub['DaysOnMarket'].median():.0f}d")
    return


@app.cell
def _(listings, sold):
    for _name, _df in [("listings", listings), ("sold", sold)]:
        _price_col = "ClosePrice" if _name == "sold" else "ListPrice"
        _d = _df[_df["YearBuilt"].notna() & _df[_price_col].notna()].copy()
        _d["Decade"] = (_d["YearBuilt"] // 10 * 10).clip(lower=1900).astype(int)

        print(f"\n{'=' * 80}")
        print(f"  {_name.upper()} — Median Price by Decade Built")
        print(f"{'=' * 80}")
        print(f"  {'Decade':10s}  {'Median Price':>14s}  {'Count':>8s}")
        for _decade, _sub in _d.groupby("Decade", sort=False):
            if len(_sub) < 50:
                continue
            print(f"  {_decade}s{' ' if _decade < 2000 else ''}   ${_sub[_price_col].median():>8,.0f}  {len(_sub):>8,}")
    return


@app.cell
def _(np, plt, sold):
    _d = sold[["Latitude", "Longitude", "ClosePrice"]].dropna()
    _lat, _lon, _p = _d["Latitude"], _d["Longitude"], _d["ClosePrice"]

    print("=" * 80)
    print("  SOLD — Lat/Long vs ClosePrice")
    print("=" * 80)
    print(f"  Records with valid coordinates: {len(_d):,}")
    print(f"  Corr(Latitude, ClosePrice):    {_lat.corr(_p):+.4f}")
    print(f"  Corr(Longitude, ClosePrice):   {_lon.corr(_p):+.4f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Sold — Lat/Long vs ClosePrice", fontsize=13)

    ax1.scatter(_lat, _p / 1e6, s=1, alpha=0.15, c="steelblue")
    ax1.set_xlabel("Latitude")
    ax1.set_ylabel("ClosePrice ($M)")
    _bins = np.linspace(_lat.min(), _lat.max(), 40)
    _bin_centers = (_bins[:-1] + _bins[1:]) / 2
    _bin_medians = [_p[(_lat >= _bins[i]) & (_lat < _bins[i + 1])].median() for i in range(len(_bins) - 1)]
    ax1.plot(_bin_centers, np.array(_bin_medians) / 1e6, "r-", linewidth=2, label="Median")
    ax1.legend()

    ax2.scatter(_lon, _p / 1e6, s=1, alpha=0.15, c="steelblue")
    ax2.set_xlabel("Longitude")
    ax2.set_ylabel("ClosePrice ($M)")
    _bins2 = np.linspace(_lon.min(), _lon.max(), 40)
    _bc2 = (_bins2[:-1] + _bins2[1:]) / 2
    _bm2 = [_p[(_lon >= _bins2[i]) & (_lon < _bins2[i + 1])].median() for i in range(len(_bins2) - 1)]
    ax2.plot(_bc2, np.array(_bm2) / 1e6, "r-", linewidth=2, label="Median")
    ax2.legend()

    fig.tight_layout()
    plt.show()

    print("\n  Median ClosePrice by Latitude Band:")
    _d["LatBand"] = (_lat // 0.5 * 0.5).round(1)
    _g = _d.groupby("LatBand")["ClosePrice"].agg(["median", "mean", "count"]).sort_index()
    for _b, _row in _g.iterrows():
        if _row["count"] > 100:
            print(f"    {_b:5.1f}° – {_b+0.5:5.1f}°   n={_row['count']:>6,}   median=${_row['median']:>9,.0f}   mean=${_row['mean']:>10,.0f}")

    print("\n  Top 10 cities by median ClosePrice (with coordinates):")
    _cities = sold[["City", "ClosePrice", "Latitude", "Longitude"]].dropna()
    _cities = _cities.groupby("City").agg(MedianPrice=("ClosePrice", "median"), Count=("ClosePrice", "count"), Lat=("Latitude", "first"), Lon=("Longitude", "first"))
    _cities = _cities[_cities["Count"] >= 50].sort_values("MedianPrice", ascending=False).head(10)
    for _city, _row in _cities.iterrows():
        print(f"    {_city:25s}  ${_row['MedianPrice']:>9,.0f}  n={_row['Count']:>5,}  @({_row['Lat']:.3f}, {_row['Lon']:.3f})")
    return


if __name__ == "__main__":
    app.run()

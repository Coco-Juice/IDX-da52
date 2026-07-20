import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import geopandas as gpd
    import pandas as pd
    from shapely.geometry import Point

    return Point, gpd, pd


@app.cell
def _(Point, gpd, pd):
    listings = pd.read_csv("csv/listings.csv", low_memory=False)
    sold = pd.read_csv("csv/sold.csv", low_memory=False)

    # Load the school district GeoJSON into a GeoDataFrame
    districts = gpd.read_file("csv/DistrictAreas2526_-284845464123469011.geojson")

    # Filter to Unified school districts only
    unified = districts[districts["DistrictType"] == "Unified"].copy()

    # Convert property Latitude/Longitude into geographic points (EPSG:4326)
    # Keep them as regular DataFrames during the conversion
    listings_geo = listings[listings['Latitude'].notna() & listings['Longitude'].notna()].copy()
    sold_geo = sold[sold['Latitude'].notna() & sold['Longitude'].notna()].copy()

    listings_geo["geometry"] = [
        Point(x, y) for x, y in zip(listings_geo["Longitude"], listings_geo["Latitude"])
    ]
    sold_geo["geometry"] = [
        Point(x, y) for x, y in zip(sold_geo["Longitude"], sold_geo["Latitude"])
    ]
    listings_geo = gpd.GeoDataFrame(listings_geo, geometry="geometry", crs="EPSG:4326")
    sold_geo = gpd.GeoDataFrame(sold_geo, geometry="geometry", crs="EPSG:4326")

    # Spatial join: find which Unified district contains each property
    # Reproject districts to match property CRS (EPSG:4326)
    unified = unified.to_crs("EPSG:4326")
    listings_geo = gpd.sjoin(
        listings_geo, unified[["DistrictName", "geometry"]], how="left", predicate="intersects",
    )
    # Handle duplicate matches: keep first
    listings_geo = listings_geo[~listings_geo.index.duplicated(keep="first")]

    sold_geo = gpd.sjoin(
        sold_geo, unified[["DistrictName", "geometry"]], how="left", predicate="intersects",
    )
    sold_geo = sold_geo[~sold_geo.index.duplicated(keep="first")]

    # Drop the geometry column and index column from sjoin
    listings_geo = listings_geo.drop(columns=["geometry", "index_right"])
    sold_geo = sold_geo.drop(columns=["geometry", "index_right"])

    # Keep DistrictName on the geo DataFrames too
    # Merge the DistrictName back into the full DataFrames on index
    listings["DistrictName"] = listings_geo["DistrictName"]
    sold["DistrictName"] = sold_geo["DistrictName"]
    return listings, sold


@app.cell
def _(pd):
    # Step 1 – Fetch the mortgage rate data from FRED

    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
    mortgage = pd.read_csv(url, parse_dates=['observation_date'])
    mortgage.columns = ['date', 'rate_30yr_fixed']
    return (mortgage,)


@app.cell
def _(mortgage):
    # Step 2 – Resample weekly rates to monthly averages

    mortgage['year_month'] = mortgage['date'].dt.to_period('M')
    mortgage_monthly = (
     mortgage.groupby('year_month')['rate_30yr_fixed']
     .mean()
     .reset_index()
    )
    return (mortgage_monthly,)


@app.cell
def _(listings, pd, sold):
    # Step 3 – Create a matching year_month key on the MLS datasets

    # Sold dataset — key off CloseDate
    sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')

    # Listings dataset — key off ListingContractDate
    listings['year_month'] = pd.to_datetime(
     listings['ListingContractDate']
    ).dt.to_period('M')
    return


@app.cell
def _(listings, mortgage_monthly, sold):
    # Step 4 – Merge

    sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
    listings_with_rates = listings.merge(mortgage_monthly, on='year_month', how='left')
    return listings_with_rates, sold_with_rates


@app.cell
def _(listings_with_rates, sold_with_rates):
    # Step 5 – Validate the merge

    # Check for any unmatched rows (rate should not be null)
    print(sold_with_rates['rate_30yr_fixed'].isnull().sum())
    print(listings_with_rates['rate_30yr_fixed'].isnull().sum())
    return


@app.cell
def _(sold_with_rates):
    print(
     sold_with_rates[
     ['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']
     ].head()
    )
    return


@app.cell
def _(listings_with_rates, sold_with_rates):
    # Step 6 - Save the new enriched CSVs

    listings_with_rates.to_csv("csv/listings_enriched.csv")
    sold_with_rates.to_csv("csv/sold_enriched.csv")
    return


if __name__ == "__main__":
    app.run()

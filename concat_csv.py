import pandas as pd
import glob


def concat_csvs(pattern, output, exclude_cols=None):
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No files matched {pattern}")
        return

    # Rows before concat: 893594 (listings), 681599 (sold)
    dfs = [pd.read_csv(f, low_memory=False) for f in files]
    raw = pd.concat(dfs, ignore_index=True)
    total_raw = len(raw)
    print(output)
    print(f"Rows before concat: {total_raw}")

    # Rows after concat: 893594 (listings), 681599 (sold)
    total_concat = len(raw)
    print(f"Rows after concat: {total_concat}")

    # Rows before Residential filter: 893594 (listings), 681599 (sold)
    print(f"Rows before Residential filter: {total_concat}")

    residential = raw[raw["PropertyType"] == "Residential"]
    # Rows after Residential filter: 567549 (listings), 458336 (sold)
    print(f"Rows after Residential filter: {len(residential)}\n")

    if exclude_cols:
        residential = residential.drop(columns=[c for c in exclude_cols if c in residential.columns])

    residential.to_csv(output, index=False)


def main():
    concat_csvs("raw_csv/CRMLSListing*.csv", "csv/listings.csv")
    concat_csvs("raw_csv/CRMLSSold[0-9]*.csv", "csv/sold.csv", exclude_cols={"latfilled", "lonfilled"})


if __name__ == "__main__":
    main()

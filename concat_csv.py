import csv
import glob


def collect_headers(files):
    """Collect the union of all headers across CSV files."""
    all_headers = []
    for fpath in files:
        with open(fpath, newline="") as f:
            all_headers.append(next(csv.reader(f)))
    # Union of all headers, preserving order from first occurrence
    seen = set()
    union = []
    for h in all_headers:
        for col in h:
            if col not in seen:
                seen.add(col)
                union.append(col)
    return union


def concat_csvs(pattern, output, exclude_cols=None):
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No files matched {pattern}")
        return

    headers = collect_headers(files)
    if exclude_cols:
        headers = [h for h in headers if h not in exclude_cols]
    rows = 0
    with open(output, "w", newline="") as fout:
        writer = csv.DictWriter(fout, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for fpath in files:
            with open(fpath, newline="") as fin:
                reader = csv.DictReader(fin)
                count = 0
                for row in reader:
                    writer.writerow(row)
                    count += 1
                rows += count
    print(f"Wrote {output} with {rows} rows from {len(files)} files")


def main():
    concat_csvs("csv/CRMLSListing*.csv", "listings.csv")
    concat_csvs("csv/CRMLSSold[0-9]*.csv", "sold.csv", exclude_cols={"latfilled", "lonfilled"})


if __name__ == "__main__":
    main()

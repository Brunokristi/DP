from pathlib import Path
import pandas as pd
import csv

def read_text(path: Path) -> str:
    """
    Read a text file safely and return stripped content.
    """
    try:
        return path.read_text(encoding="utf-8").strip()
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace").strip()

def collect_pairs(root: Path):
    """
    Collect matching judgement/summary text pairs.
    Files must share the same filename.
    """
    rows = []

    for jud_dir in root.rglob("judgement"):
        sum_dir = jud_dir.parent / "summary"
        if not sum_dir.exists():
            continue

        summaries = {p.name: p for p in sum_dir.glob("*.txt")}

        for jud_path in jud_dir.glob("*.txt"):
            sum_path = summaries.get(jud_path.name)
            if sum_path is None:
                continue

            rows.append({
                "judgement": read_text(jud_path),
                "summary": read_text(sum_path),
            })

    return rows

def main():
    # CHANGE THIS to the root folder of your dataset
    dataset_root = Path("/Users/brunokristian/Downloads/dataset")

    # Build dataframe
    df = pd.DataFrame(collect_pairs(dataset_root))

    print(f"Initial rows: {len(df)}")

    # Drop NaN values
    df = df.dropna(subset=["judgement", "summary"])

    # Drop empty / whitespace-only rows
    df = df[
        df["judgement"].str.strip().ne("") &
        df["summary"].str.strip().ne("")
    ]

    print(f"Rows after cleaning: {len(df)}")

    # Write CSV (safe for commas, quotes, and newlines)
    out_csv = dataset_root / "judgement_summary.csv"
    df.to_csv(
        out_csv,
        index=False,
        encoding="utf-8",
        quoting=csv.QUOTE_ALL
    )

    print(f"Saved cleaned dataset to: {out_csv}")

if __name__ == "__main__":
    main()

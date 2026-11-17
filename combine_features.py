import csv
from pathlib import Path

files = sorted(Path("extracted_features").glob("features_p0000[0-4].csv"))

with open("sample_features.csv", "w", newline="") as out:
    writer = None

    for file in files:
        with file.open(newline="") as f:
            reader = csv.DictReader(f)

            if writer is None:
                writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
                writer.writeheader()

            writer.writerows(reader)

print(f"Combined {len(files)} files.")
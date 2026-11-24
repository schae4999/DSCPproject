import csv
import shutil
from pathlib import Path

root = Path("Project_CodeNet")
subset = Path("CodeNet_subset")
for source_csv in sorted((root / "metadata").glob("p[0-9][0-9][0-9][0-9][0-9].csv")):
    problem = source_csv.stem
    
    output_csv = subset / "metadata" / f"{problem}.csv"
    output_code = subset / "data" / problem / "Python"

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_code.mkdir(parents=True, exist_ok=True)

    copied = 0
    with source_csv.open(newline="") as source, output_csv.open("w", newline="") as output:
        reader = csv.DictReader(source)
        writer = csv.DictWriter(output, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            if row["language"] != "Python" or row["status"] != "Accepted":
                continue

            filename = f"{row['submission_id']}.{row['filename_ext']}"
            source_file = root / "data" / problem / "Python" / filename
            shutil.copyfile(source_file, output_code / filename)
            writer.writerow(row)
            copied += 1

        print(f"{problem}: copied {copied} Python files.")

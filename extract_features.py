import sys
import ast
import csv
import warnings
from pathlib import Path
from lib2to3.refactor import RefactoringTool, get_fixers_from_package
from lib2to3.pgen2.parse import ParseError

warnings.filterwarnings("ignore", category=DeprecationWarning)

converter = RefactoringTool(get_fixers_from_package("lib2to3.fixes"))

if len(sys.argv) != 2:
  print("Usage: python3 extract_features.py <problem_id>")
  sys.exit(1)

problem_id = sys.argv[1]

source_dir = Path(f"CodeNet_subset/data/{problem_id}/Python")
metadata_file = Path(f"CodeNet_subset/metadata/{problem_id}.csv")

def extract_features(source_path):
  """
  Extract structural features from Python 2 or Python 3 source code.
  Converts Python 2 syntax in memory if necessary.

  Returns:
    dict: Line count, loop count, maximum loop nesting depth, and function count.
  """
  code = source_path.read_text(encoding="utf-8", errors="replace")

  try:
    tree = ast.parse(code)
  except SyntaxError:
    converted_code = str(converter.refactor_string(
      code.rstrip() + "\n", str(source_path)
    ))
    tree = ast.parse(converted_code)

  loop_count = 0
  function_count = 0
  max_depth = 0

  def visit(node, depth=0):
    nonlocal loop_count, function_count, max_depth

    if isinstance(node, (ast.For, ast.While, ast.AsyncFor)):
      loop_count += 1
      depth += 1
      max_depth = max(max_depth, depth)

    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
      function_count += 1

    for child in ast.iter_child_nodes(node):
      visit(child, depth)

  visit(tree)

  return {
    "line_count": len(code.splitlines()),
    "loop_count": loop_count,
    "max_loop_depth": max_depth,
    "function_count": function_count,
  }

with open("problem_list.csv", newline="") as f:
  problem_info = {
    row["id"]: row
    for row in csv.DictReader(f)
  }

limits = problem_info[problem_id]

results = []

with metadata_file.open(newline="") as f:
  reader = csv.DictReader(f)

  for row in reader:
    if row["status"] != "Accepted" or row["language"] != "Python":
      continue

    source_path = source_dir / f"{row['submission_id']}.py"

    if not source_path.exists():
      continue
    
    try:
      features = extract_features(source_path)
    except (SyntaxError, RecursionError, ValueError, ParseError):
      continue

    results.append({
      "submission_id": row["submission_id"],
      "problem_id": row["problem_id"],
      "cpu_time": row["cpu_time"],
      "code_size": row["code_size"],
      "time_limit": limits["time_limit"],
      "memory_limit": limits["memory_limit"],
      **features,
    })

fieldnames = [
  "submission_id", "problem_id", "cpu_time", "code_size",
  "time_limit", "memory_limit",
  "line_count", "loop_count", "max_loop_depth", "function_count"
]

output_dir = Path("extracted_features")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / f"features_{problem_id}.csv"

with output_file.open("w", newline="") as f:
  writer = csv.DictWriter(f, fieldnames=fieldnames)
  writer.writeheader()
  writer.writerows(results)

print(f"Extracted features from {len(results)} submissions.")
import csv, glob, hashlib, math, os, sys

files = glob.glob(os.path.join(sys.argv[1], "p*.csv"))
if not files:
    sys.exit("No p*.csv files found")

def rows():
    for path in files:
        with open(path, newline="", encoding="utf-8", errors="replace") as f:
            for r in csv.DictReader(f):
                if "accepted" not in r.get("status", "").lower():
                    continue
                if "python" not in r.get("language", "").lower():
                    continue
                try:
                    x, y = float(r["code_size"]), float(r["cpu_time"])
                    if not (math.isfinite(x) and math.isfinite(y)):
                        continue
                except (KeyError, ValueError, TypeError):
                    continue
                problem = r.get("problem_id", "").strip() or os.path.basename(path)[1:-4]
                fold = int(hashlib.md5(problem.encode()).hexdigest()[:8], 16) % 5
                yield fold, x, y

# Fit five models, holding out whole problems for each fold
stats = [[0, 0., 0., 0., 0.] for _ in range(5)]
for fold, x, y in rows():
    a = stats[fold]
    a[0] += 1
    a[1] += x
    a[2] += y
    a[3] += x*x
    a[4] += x*y

models = []
for fold in range(5):
    train = [stats[i] for i in range(5) if i != fold]
    n = sum(a[0] for a in train)
    sx, sy = sum(a[1] for a in train), sum(a[2] for a in train)
    sxx, sxy = sum(a[3] for a in train), sum(a[4] for a in train)
    denom = n*sxx - sx*sx
    if n < 2 or abs(denom) < 1e-12:
        sys.exit("Not enough training data")
    slope = (n*sxy - sx*sy) / denom
    models.append(((sy - slope*sx) / n, slope))

abs_err, sq_err, counts = [0.]*5, [0.]*5, [0]*5
for fold, x, y in rows():
    intercept, slope = models[fold]
    error = y - (intercept + slope*x)
    abs_err[fold] += abs(error)
    sq_err[fold] += error*error
    counts[fold] += 1

total_abs, total_sq, total_n = 0., 0., 0
print("Model: cpu_time ~ code_size")
for i in range(5):
    if counts[i]:
        print(f"Fold {i+1}: n={counts[i]}, MAE={abs_err[i]/counts[i]:.4f}, RMSE={math.sqrt(sq_err[i]/counts[i]):.4f}")
        total_abs += abs_err[i]
        total_sq += sq_err[i]
        total_n += counts[i]
if total_n:
    print(f"Overall: n={total_n}, MAE={total_abs/total_n:.4f}, RMSE={math.sqrt(total_sq/total_n):.4f}")

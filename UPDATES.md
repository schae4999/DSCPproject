# Updates (Nov 17)

## Things to Discuss

**Dataset size**
- Filtered CodeNet subset: ~337 MB compressed
- Uncompressed file sizes: ~1.08 GiB
- Actual disk usage after extraction on CHTC: ~15 GB
- **Need to confirm with everyone:** Doesn't satisfy the 10–100 GB dataset requirement?

## What I Did

### 1. Feature Extraction

Created `extract_features.py` to extract features from accepted Python submissions.

Features:
- `code_size` — code size from metadata
- `line_count` — number of lines
- `loop_count` — number of loops
- `max_loop_depth` — maximum nested loop depth
- `function_count` — number of functions
- `time_limit` — problem time limit
- `memory_limit` — problem memory limit

Response variable: `cpu_time` (milliseconds).

Used Python AST to extract code structure.

### 2. Tested Parallel Processing on CHTC

- Tested the first 5 problems (`p00000`–`p00004`).
- Submitted 5 HTCondor jobs, one per problem.
- Successfully extracted features from 3,585 accepted Python submissions.
- Combined the outputs into `sample_features.csv`.
- Prepared individual `.tar.gz` input archives for all 4,053 problems, but haven't run the full extraction yet.

### 3. Tested Multiple Linear Regression

Created `train_model.py` using Scikit-learn.

- **Predictors:** `code_size`, `line_count`, `loop_count`, `max_loop_depth`, `function_count`, `time_limit`, `memory_limit`
- **Response:** `cpu_time`
- **Evaluation:** 5-fold GroupKFold by `problem_id` (train/test problems don't overlap)
- **Baseline:** Predict the mean CPU time of the training submissions

Results from 3,585 submissions across 5 problems:

| Metric | Linear Regression | Baseline |
|---|---:|---:|
| MAE | 9.52 ms | 8.61 ms |
| RMSE | 11.92 ms | 11.27 ms |

The regression performed slightly worse than the baseline, but this was only a small test to make sure the pipeline works.

## Next

- Confirm dataset size and requirements.
- Run feature extraction on all 4,053 problems.
- Retrain and evaluate using the full dataset.
- Discuss whether we should add features or transform CPU runtime if performance remains poor.
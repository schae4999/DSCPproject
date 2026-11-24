# Predicting Python Program CPU Time

## Project Question

Can structural features of Python source code and problem-specific characteristics predict CPU execution time without running the code?

## Dataset

We use accepted Python submissions from IBM Project CodeNet. The dataset is stored separately on CHTC and is not included in this repository.

## Baseline Model

This repository includes a simple linear regression baseline that predicts CPU time from code size:

`cpu_time ~ code_size`

The model was evaluated with five-fold cross-validation grouped by `problem_id`, so submissions from the same problem were kept in the same fold.

- Submissions evaluated: 1,796,563
- MAE: 232.89 ms
- RMSE: 683.14 ms

This baseline uses only `code_size`. Future models can add AST-derived code features and problem-specific limits.

## Files

- `filter.py`: filters the accepted Python submissions
- `model.py`: fits and evaluates the baseline model
- `model.sub`: CHTC job submission file
- `run_model.sh`: runs the model in a CHTC job
- `model.out`: model results

## Running on CHTC

The job expects `metadata.tar.gz` to contain the extracted `CodeNet_subset/metadata/` directory. From the directory containing the model files and `metadata.tar.gz`, submit the job with:

```bash
condor_submit model.sub

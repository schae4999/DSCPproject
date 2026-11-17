import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import GroupKFold, cross_val_predict
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load extracted features
df = pd.read_csv("sample_features.csv")

# Predictor variables
predictors = [
    "code_size",
    "time_limit",
    "memory_limit",
    "line_count",
    "loop_count",
    "max_loop_depth",
    "function_count"
]

X = df[predictors]
y = df["cpu_time"]
groups = df["problem_id"]

# Grouped cross-validation:
# Submissions from the same problem stay in the same fold
cv = GroupKFold(n_splits=5)

# Multiple linear regression
model = LinearRegression()

predictions = cross_val_predict(
    model, X, y, cv=cv, groups=groups
)

mae = mean_absolute_error(y, predictions)
rmse = np.sqrt(mean_squared_error(y, predictions))

# Baseline: predict the training-set mean CPU time
baseline = DummyRegressor(strategy="mean")

baseline_predictions = cross_val_predict(
    baseline, X, y, cv=cv, groups=groups
)

baseline_mae = mean_absolute_error(y, baseline_predictions)
baseline_rmse = np.sqrt(mean_squared_error(y, baseline_predictions))

# Results
print(f"Submissions: {len(df)}")
print(f"Problems: {groups.nunique()}")

print("\nMultiple Linear Regression:")
print(f"MAE: {mae:.2f} ms")
print(f"RMSE: {rmse:.2f} ms")

print("\nBaseline (Mean Prediction):")
print(f"MAE: {baseline_mae:.2f} ms")
print(f"RMSE: {baseline_rmse:.2f} ms")

print("\nImprovement over baseline:")
print(f"MAE improvement: {baseline_mae - mae:.2f} ms")
print(f"RMSE improvement: {baseline_rmse - rmse:.2f} ms")
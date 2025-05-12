import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

# 0. Baca Feature
df = pd.read_parquet('../data/features_2024-05-01_to_2025-05-07.parquet')

# 1. PILIH FITUR & TARGET
all_features = [col for col in df.columns if col.startswith('lag_') or 
                col.startswith('same_hour_')] + [
    'hour_of_day', 'day_of_week', 'is_weekend', 'week_of_year', 'month', 'is_holiday'
]

df_model = df.dropna(subset=all_features + ['demand']).copy()

X = df_model[all_features]
y = df_model['demand']

# 2. SPLIT TRAIN/TEST (test = data after 2025-04-01)
train_mask = df_model['datetime'] < '2025-04-01'
X_train, y_train = X[train_mask], y[train_mask]
X_test, y_test = X[~train_mask], y[~train_mask]

# 3. INISIASI MODEL DAN GRID PARAMS
models = {
    'DecisionTree': (DecisionTreeRegressor(), {
        'max_depth': [5, 10, 20],
        'min_samples_split': [2, 5, 10]
    }),
    'RandomForest': (RandomForestRegressor(random_state=42, n_jobs=-1), {
        'n_estimators': [50, 100],
        'max_depth': [10, 20],
        'min_samples_split': [2, 5]
    }),
    'XGBoost': (XGBRegressor(random_state=42, n_jobs=-1, verbosity=0), {
        'n_estimators': [50, 100],
        'max_depth': [3, 6],
        'learning_rate': [0.05, 0.1]
    }),
    'LightGBM': (LGBMRegressor(random_state=42), {
        'n_estimators': [50, 100],
        'max_depth': [10, 20],
        'learning_rate': [0.05, 0.1]
    }),
    'CatBoost': (CatBoostRegressor(random_state=42, verbose=0), {
        'iterations': [50, 100],
        'depth': [6, 10],
        'learning_rate': [0.05, 0.1]
    }),
}

# 4. FITTING, GRID SEARCH & EVALUASI
results = {}

for name, (model, params) in models.items():
    print(f"\n🔍 Training {name}...")
    grid = GridSearchCV(model, params, cv=3, scoring='neg_mean_absolute_error', n_jobs=-1)
    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_
    y_pred = best_model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    results[name] = {
        'Best Params': grid.best_params_,
        'MAE': mae,
        'MSE': mse,
        'R2': r2
    }

# 5. TAMPILKAN HASIL
print("\n📊 MODEL PERFORMANCE COMPARISON:\n")
for model_name, res in results.items():
    print(f"{model_name}")
    print(f"  Best Params: {res['Best Params']}")
    print(f"  MAE: {res['MAE']:.4f}")
    print(f"  MSE: {res['MSE']:.4f}")
    print(f"  R2:  {res['R2']:.4f}")
    print("-" * 50)

# 6. CREATE FINAL COMPARISON TABLE
metrics_table = pd.DataFrame([
    {
        'Model': model_name,
        'MAE': res['MAE'],
        'MSE': res['MSE'],
        'R2': res['R2']
    }
    for model_name, res in results.items()
])

# Urutkan berdasarkan MAE terkecil (semakin kecil semakin bagus)
metrics_table = metrics_table.sort_values('MAE').reset_index(drop=True)

print("\n📋 Final Metrics Comparison Table:")
print(metrics_table)
metrics_table.to_csv('../data/model_metrics.csv')
🛒 Hourly Demand Forecasting (1-Hour Ahead)

🔍 Problem Statement

Demand forecasting is a critical task commonly found in many industries such as retail, logistics, food delivery, and manufacturing. Accurate demand predictions help businesses:

    Optimize inventory and resource allocation

    Reduce stockouts and overstock scenarios

    Maximize order fulfillment and customer satisfaction

This project focuses on hourly demand forecasting per location, with the goal of predicting the number of orders 1 hour ahead based on historical transactional data and temporal patterns.

📈 Prediction Target

The target variable is the number of orders (demand) at each location for the next hour, using past demand values and time-based features.

🧠 Features Used

This project generates both lag-based and seasonality-aware features, including:

    demand_lag_1 to demand_lag_24: demand in the past 24 hours

    demand_same_hour_1d_ago to demand_same_hour_7d_ago: demand at the same hour in past 7 days

    Time-based context:

        Hour of day (0–23)

        Day of week (Monday–Sunday)

        Weekend flag

        Week of year, month

        Holiday indicator (based on Indonesian calendar)

🧪 Model Benchmark

Several machine learning models were trained using GridSearchCV for hyperparameter tuning:

    Decision Tree Regressor

    Random Forest Regressor

    XGBoost Regressor

    LightGBM Regressor

    CatBoost Regressor

The following table compares the performance of each model on the test set (data after 2025-04-01):
### 📊 Model Performance Comparison

| Model         | MAE  | MSE   | R²    |
|---------------|------|-------|-------|
| XGBoost       | 5.69 | 60.92 | 0.962 |
| CatBoost      | 5.76 | 62.54 | 0.961 |
| LightGBM      | 5.92 | 66.37 | 0.958 |
| RandomForest  | 5.98 | 69.33 | 0.957 |
| DecisionTree  | 6.73 | 91.15 | 0.943 |

📊 Forecast Results

Each model's prediction is compared against actual demand for the test period. Below are example plots:

✅ XGBoost. https://github.com/restunugroho/demand-forecast/blob/master/src/plots/xgboost.png

✅ CatBoost. https://github.com/restunugroho/demand-forecast/blob/master/src/plots/catboost.png

✅ LightGBM. https://github.com/restunugroho/demand-forecast/blob/master/src/plots/lightgbm.png

✅ Random Forest. https://github.com/restunugroho/demand-forecast/blob/master/src/plots/random_forest.png

✅ Decision Tree. https://github.com/restunugroho/demand-forecast/blob/master/src/plots/decision_tree.png



🛠 Tech Stack

    Python (pandas, scikit-learn, matplotlib, holidays, xgboost, lightgbm, catboost)

    GridSearchCV for hyperparameter tuning

    Plotly for visualization


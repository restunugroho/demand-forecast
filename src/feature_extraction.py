"""
FEATURE EXTRACTION (LAG & SEASONALITY)

This script generates time-series features from the hourly demand aggregation.

Assumptions:
- Hours with no demand are missing from the original aggregation result.
- For modeling purposes, we impute the data so that every hour is present for each location.

Steps:
1. Create a complete set of combinations: location × hour, from the earliest to latest timestamp.
2. Merge the original aggregated data into the full time grid, filling missing demand with 0.
3. Generate features:
   - Lag features for the past 1 to 24 hours → lag_1 to lag_24
   - Same-hour demand from the past 1 to 7 days → same_hour_1d_ago to same_hour_7d_ago

Additional Time-based Features:
- hour_of_day: Hour (0–23)
- day_of_week: Day of the week (Monday=0, Sunday=6)
- is_weekend: 1 if Saturday/Sunday, else 0
- week_of_year: ISO week number (1–52)
- month: Month number (1–12)
- is_holiday: 1 if the date is a national holiday (Indonesia), else 0

Output:
- Enriched data with columns: location, hour, demand, lag_1..24, same_hour_1d_ago..7d_ago
"""


import pandas as pd
import holidays

df = pd.read_parquet(f"../data/demand_2024-05-01_to_2025-05-07.parquet")
print(df)

# Pastikan hour dalam datetime dan sudah difloor ke jam
df['hour'] = pd.to_datetime(df['hour'])
df = df.sort_values(['location', 'hour'])

# Dapatkan range waktu global
start = df['hour'].min()
end = df['hour'].max()

# create full time series combination location and hour to make sure all hours are covered
full_hours = pd.date_range(start=start, end=end, freq='H')

# get unique locations
locations = df['location'].unique()

full_index = pd.MultiIndex.from_product([locations, full_hours], names=['location', 'hour'])
df_full = pd.DataFrame(index=full_index).reset_index()
df_merged = df_full.merge(df, on=['location', 'hour'], how='left')

print(df_merged)

# fill demand to zero if there isn't in record
df_merged['demand'] = df_merged['demand'].fillna(0)

df_merged = df_merged.sort_values(['location', 'hour'])
df_merged = df_merged.set_index('hour')

# time series features for last 24 hour, every 1 hour
for lag in range(1, 25):
    df_merged[f'lag_{lag}'] = df_merged.groupby('location')['demand'].shift(lag)

# create feature last 7 days, at same hour. this to catch cyclic daily pattern
for day in range(1, 8):
    df_merged[f'same_hour_{day}d_ago'] = df_merged.groupby('location')['demand'].shift(24 * day)

df_merged = df_merged.dropna().reset_index()
df_merged = df_merged.rename(columns={'hour':'datetime'})

print(df_merged)

# Extract time-based features
df_merged['hour_of_day'] = df_merged['datetime'].dt.hour
df_merged['day_of_week'] = df_merged['datetime'].dt.dayofweek
df_merged['is_weekend'] = df_merged['day_of_week'].isin([5, 6]).astype(int)
df_merged['week_of_year'] = df_merged['datetime'].dt.isocalendar().week
df_merged['month'] = df_merged['datetime'].dt.month

# add Indonesian holiday feature
indo_holidays = holidays.Indonesia()
df_merged['is_holiday'] = df_merged['datetime'].dt.date.isin(indo_holidays).astype(int)

print(df_merged)

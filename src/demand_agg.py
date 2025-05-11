"""
DEMAND AGGREGATION

This script performs hourly demand aggregation per location based on transactional data.

Input:
- Transactional data with columns: order_id, location, timestamp

Steps:
1. Convert the 'timestamp' column to datetime format.
2. Floor each timestamp to the nearest hour (e.g., 08:15 → 08:00).
3. Count the number of transactions (demand) per location and per hour.

Output:
- Aggregated data with columns: location, hour, demand
"""


from datetime import datetime, timedelta, time
import pandas as pd

df = pd.read_parquet(f"../data/food_orders_2024-05-01_to_2025-05-07.parquet")
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.floor('H')

agg = df.groupby(['location', 'hour']).size().reset_index(name='demand')
print(agg)

agg.to_parquet(f"../data/demand_2024-05-01_to_2025-05-07.parquet")
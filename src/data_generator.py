import random
import uuid
from datetime import datetime, timedelta, time
import pandas as pd

# Konfigurasi outlet & menu
outlets = [
    {"name": "Outlet A", "location": "Palu Utara"},
    {"name": "Outlet B", "location": "Palu Selatan"},
    {"name": "Outlet C", "location": "Palu Barat"},
    {"name": "Outlet D", "location": "Palu Timur"},
    {"name": "Outlet E", "location": "Palu Tengah"},
]

menu_items = ["Sup Kacang Merah", "Bubur Manado", "Ikan Bakar", "Minuman Saraba"]
order_types = ["apps", "offline"]
statuses = ["created", "processing", "food ready", "on the way", "delivered"]

# Bobot kepadatan per jam
hour_weights = {
    h: w for h, w in [
        *( [(h, 2) for h in range(0, 6)] ),
        *( [(h, 5) for h in range(6, 7)] ),
        *( [(h, 10) for h in range(7, 10)] ),
        *( [(h, 6) for h in range(10, 11)] ),
        *( [(h, 15) for h in range(11, 14)] ),
        *( [(h, 5) for h in range(14, 17)] ),
        *( [(h, 12) for h in range(17, 20)] ),
        *( [(h, 4) for h in range(20, 24)] )
    ]
}

# Daftar tanggal libur nasional / libur panjang
holiday_dates = {
    "2024-12-25",  # Natal
    "2025-01-01",  # Tahun Baru
    "2024-04-10", "2024-04-11", "2024-04-12",  # Libur panjang
    "2024-05-01",  # Hari Buruh
    "2024-06-17",  # Idul Adha
}

# Fungsi waktu dalam jam tertentu
def generate_time_in_hour(hour):
    return time(hour, random.randint(0, 59), random.randint(0, 59))

# Fungsi generate 1 order (multi-status)
def generate_order(outlet, base_time):
    order_id = str(uuid.uuid4())
    item = random.choice(menu_items)
    order_type = random.choice(order_types)
    canceled = random.random() < 0.1  # 10% kemungkinan dibatalkan
    events = []

    for i, status in enumerate(statuses):
        timestamp = base_time + timedelta(minutes=i * random.randint(2, 5))
        events.append({
            "order_id": order_id,
            "outlet_name": outlet["name"],
            "location": outlet["location"],
            "menu_item": item,
            "order_type": order_type,
            "status": status,
            "timestamp": timestamp.isoformat()
        })
        if canceled and status == "created":
            events.append({
                "order_id": order_id,
                "outlet_name": outlet["name"],
                "location": outlet["location"],
                "menu_item": item,
                "order_type": order_type,
                "status": "canceled",
                "timestamp": (timestamp + timedelta(minutes=1)).isoformat()
            })
            break
    return events

# Generate order per hari
def generate_daily_orders(order_count, current_date):
    all_events = []
    total_weight = sum(hour_weights.values())
    for hour, weight in hour_weights.items():
        hour_order_count = int(order_count * (weight / total_weight))
        for _ in range(hour_order_count):
            outlet = random.choice(outlets)
            time_part = generate_time_in_hour(hour)
            base_time = datetime.combine(current_date, time_part)
            events = generate_order(outlet, base_time)
            all_events.extend(events)
    return all_events

# Fungsi generate data range dengan seasonalitas dan tren
def generate_data_range(start_date: str, end_date: str):
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    data = []
    total_days = (end - start).days + 1

    for day_index, current_date in enumerate(start + timedelta(n) for n in range(total_days)):
        weekday = current_date.weekday()
        is_weekend = weekday >= 5
        is_holiday = current_date.strftime("%Y-%m-%d") in holiday_dates

        # Base order count
        order_count = 7500 if is_weekend else 5000

        # Seasonal effect: lonjakan saat libur
        if is_holiday:
            order_count = int(order_count * 1.5)

        # Trend effect: peningkatan linear selama periode waktu
        trend_multiplier = 1 + (day_index / total_days) * 0.2  # naik 20% sampai akhir
        order_count = int(order_count * trend_multiplier)

        print(f"{current_date} ({'Weekend' if is_weekend else 'Weekday'}{' + Holiday' if is_holiday else ''}) - {order_count} orders")

        daily_events = generate_daily_orders(order_count, current_date)
        data.extend(daily_events)

    return data

# Main
if __name__ == "__main__":
    start_date = "2025-05-01"
    end_date = "2025-05-07"

    all_data = generate_data_range(start_date, end_date)
    df = pd.DataFrame(all_data)
    df = df.sort_values(by="timestamp")
    print(df.head())
    # df.to_csv(f"food_orders_{start_date}_to_{end_date}.csv", index=False)
    print(f"Saved {len(df)} rows from {start_date} to {end_date}.")

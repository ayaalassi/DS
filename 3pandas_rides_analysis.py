import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Load Data ---
file_path = r"C:/Users/Amani/Desktop/DS project/archive/ncr_ride_bookings.csv"
df = pd.read_csv(file_path)

# --- 2. Normalize column names ---
df.columns = [col.lower().replace(" ", "_") for col in df.columns]

# --- 3. Clean Booking ID ---
df['booking_id'] = df['booking_id'].str.replace('"','')

# --- 4. Convert data types ---
df['date'] = pd.to_datetime(df['date'])
df['vehicle_type'] = df['vehicle_type'].astype('category')
df['booking_status'] = df['booking_status'].astype('category')

# --- 5. Fill missing numeric values ---
numeric_cols = ['avg_vtat','avg_ctat','cancelled_rides_by_customer','cancelled_rides_by_driver',
                'incomplete_rides','booking_value','ride_distance','driver_ratings','customer_rating']

for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mean())

# --- 6. Inspect Data ---
print(df.head())
print(df.info())
print(df.describe())

# --- 7. Indexing & Selecting ---
print(df[['booking_id','booking_value','ride_distance']].head())
print(df.iloc[0:5, 0:3])

# --- 8. Filtering ---
long_rides = df[df['ride_distance'] > 20]
high_booking_value = df[df['booking_value'] > 500]

# --- 9. Sorting ---
top_bookings = df.sort_values(by='booking_value', ascending=False).head(10)

# --- 10. GroupBy ---
avg_booking_per_vehicle = df.groupby('vehicle_type', observed=True)['booking_value'].mean()
daily_distance_sum = df.groupby('date')['ride_distance'].sum()

# --- 11. Iteration Example ---
for idx, row in df.head(5).iterrows():
    print(f"Booking ID {row['booking_id']} | Booking Value: {row['booking_value']:.2f} | Distance: {row['ride_distance']:.2f}")

# --- 12. Statistical Functions ---
booking_mean = df['booking_value'].mean()
booking_median = df['booking_value'].median()
distance_max = df['ride_distance'].max()

# --- 13. Working with Text Data ---
df['pickup_location_lower'] = df['pickup_location'].str.lower()
airport_rides = df[df['pickup_location_lower'].str.contains('airport', na=False)]

# --- 14. Time Series Analysis ---
df.set_index('date', inplace=True)
daily_booking_sum = df['booking_value'].resample('D').sum()

# --- 15. Visualization ---
sns.histplot(df['booking_value'], bins=20)
plt.title("Booking Value Distribution")
plt.show()

sns.boxplot(x='vehicle_type', y='booking_value', data=df)
plt.title("Booking Value by Vehicle Type")
plt.show()

# --- 16. Save Processed Data ---
df.to_csv("processed_rides_cleaned.csv", index=False)

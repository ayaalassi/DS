import numpy as np
import pandas as pd

# --- 1️⃣ Load CSV with Pandas first ---
file_path = r"C:/Users/Amani/Desktop/DS project/archive/ncr_ride_bookings.csv"
df = pd.read_csv(file_path)

# --- 2️⃣ Clean column names and remove quotes from booking_id ---
df.columns = [col.lower().replace(" ", "_") for col in df.columns]
df['booking_id'] = df['booking_id'].str.replace('"', '', regex=False)

# --- 3️⃣ Fill missing numeric values with column mean ---
numeric_cols = ['avg_vtat','avg_ctat','cancelled_rides_by_customer','cancelled_rides_by_driver',
                'incomplete_rides','booking_value','ride_distance','driver_ratings','customer_rating']
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mean())

# --- 4️⃣ Convert key columns to NumPy arrays ---
booking_value = df['booking_value'].to_numpy()
ride_distance = df['ride_distance'].to_numpy()
driver_ratings = df['driver_ratings'].to_numpy()
customer_rating = df['customer_rating'].to_numpy()

# --- 5️⃣ Array properties ---
print("Shape of booking_value:", booking_value.shape)
print("Data type:", booking_value.dtype)
print("Number of dimensions:", booking_value.ndim)

# --- 6️⃣ Array indexing and slicing ---
print("First 5 booking values:", booking_value[:5])
print("Last 5 distances:", ride_distance[-5:])
print("Every 2nd driver rating:", driver_ratings[::2])

# --- 7️⃣ Array arithmetic (ufuncs) ---
avg_rating = np.mean([driver_ratings, customer_rating], axis=0)
print("Average rating for first 5 rides:", avg_rating[:5])

# --- 8️⃣ Filtering arrays ---
long_rides_mask = ride_distance > 20
high_booking_mask = booking_value > 500
print("Number of long rides (>20km):", np.sum(long_rides_mask))
print("Number of high bookings (>500):", np.sum(high_booking_mask))

# --- 9️⃣ Sorting ---
sorted_booking_idx = np.argsort(booking_value)[::-1]  # descending
print("Top 5 bookings (highest value):", booking_value[sorted_booking_idx[:5]])

# --- 10️⃣ Reshaping & ravel/flatten ---
booking_reshaped = booking_value[:20].reshape(4,5)  # example reshape
print("Reshaped array 4x5:\n", booking_reshaped)
print("Flattened array:", booking_reshaped.ravel())

# --- 11️⃣ Iterating arrays ---
print("Iterating first 5 rides:")
for b, d in zip(booking_value[:5], ride_distance[:5]):
    print(f"Booking Value: {b:.2f}, Distance: {d:.2f}")

# --- 12️⃣ Random numbers examples ---
rand_array = np.random.rand(5) * 100  # 5 random numbers between 0-100
print("Random array:", rand_array)

# --- 13️⃣ Joining arrays ---
combined_array = np.column_stack((booking_value[:5], ride_distance[:5]))
print("Combined booking_value + ride_distance:\n", combined_array)

# --- 14️⃣ Splitting arrays ---
split_arrays = np.array_split(booking_value[:10], 2)
print("Split booking_value into 2 parts:", split_arrays)

# --- 15️⃣ Searching arrays ---
idx_high = np.where(booking_value > 1000)[0]
print("Indexes of bookings >1000:", idx_high)

# --- 16️⃣ Boolean masking (filtering) ---
filtered = booking_value[(booking_value > 300) & (ride_distance > 20)]
print("Bookings >300 & distance >20:", filtered)

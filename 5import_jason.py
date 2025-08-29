import pandas as pd
import json

# 🔹 Step 1: Define the CSV file path
file_path = r"C:/Users/Amani/Desktop/DS project/archive/ncr_ride_bookings.csv"

# 🔹 Step 2: Load the CSV file into a Pandas DataFrame
rides_df = pd.read_csv(file_path)

# 🔹 Step 3: Data Cleaning (Optional)
# Example: Replace missing values with a default placeholder
# You can modify this according to your dataset columns
rides_df.fillna({'Pickup Location': 'Unknown', 'Vehicle Type': 'Unknown'}, inplace=True)

# 🔹 Step 4: Save DataFrame to JSON (list of dictionaries → records)
output_json_path = r"C:/Users/Amani/Desktop/DS project/archive/rides_cleaned.json"
rides_df.to_json(output_json_path, orient="records", force_ascii=False)

# 🔹 Step 5: Reload the JSON file to verify it was saved correctly
with open(output_json_path, 'r', encoding='utf-8') as f:
    rides_data = json.load(f)

# 🔹 Step 6: Print some basic information
print(f"Total number of rides saved: {len(rides_data)}")
print("First ride example:", rides_data[0])

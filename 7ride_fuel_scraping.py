import pandas as pd
import requests
from pyquery import PyQuery as pq
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================
# 1️⃣ Read the ride bookings CSV
# ==========================
file_path = r"C:/Users/Amani/Desktop/DS project/archive/ncr_ride_bookings.csv"
rides_df = pd.read_csv(file_path)

# ✅ Show columns to understand the structure of our dataset
print("Columns in rides dataset:", rides_df.columns.tolist())

# ==========================
# 2️⃣ Fetch real fuel price from Jordan
# ==========================
url = "https://www.globalpetrolprices.com/Jordan/gasoline_prices/"
res = requests.get(url)

if res.status_code == 200:
    doc = pq(res.text)
    # Extract the current gasoline price (from the table, first row)
    price_text = doc("table.tbl_prc tr:nth-child(1) td:nth-child(2)").text()
    try:
        fuel_price = float(price_text.replace('JOD','').replace(',','').strip())
        print("Real Fuel Price from Jordan:", fuel_price)
        data_source = "Real fuel price (scraped from website)"
    except ValueError:
        fuel_price = 1.08  # default if scraping fails
        print("Could not convert scraped price to number, using default:", fuel_price)
        data_source = "Default/assumed fuel price"
else:
    fuel_price = 1.08  # default if request fails
    print("Could not fetch fuel price from website, using default:", fuel_price)
    data_source = "Default/assumed fuel price"

# ==========================
# 3️⃣ Add Fuel Price column to each ride
# ==========================
rides_df['Fuel Price'] = fuel_price

# ✅ Optional: inspect first 5 rows to ensure Fuel Price was added correctly
print(rides_df.head())

# ==========================
# 4️⃣ Why we added Fuel Price (professional note)
# ==========================
# We added Fuel Price to analyze how the cost of fuel may influence the
# Booking Value and Ride Distance. This is relevant for decision-making
# in ride-sharing operations, cost estimation, and financial analytics.

# ==========================
# 5️⃣ Plotting a scatterplot example
# ==========================
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=rides_df.sample(1000),  # sample 1000 rides to reduce overplotting
    x='Ride Distance',
    y='Booking Value',
    hue='Fuel Price',
    palette='viridis',
    alpha=0.7
)
plt.title(f"Booking Value vs Ride Distance ")
plt.xlabel("Ride Distance (km)")
plt.ylabel("Booking Value (JOD)")
plt.show()


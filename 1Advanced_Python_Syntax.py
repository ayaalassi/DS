import pandas as pd
import random

# 1️⃣ قراءة ملف الرحلات
file_path = r"C:/Users/Amani/Desktop/DS project/archive/ncr_ride_bookings.csv"
df = pd.read_csv(file_path)

# إزالة أي فراغات زائدة من أسماء الأعمدة
df.columns = df.columns.str.strip()

# 2️⃣ عرض أول 5 صفوف للتأكد من البيانات
print("First 5 rows:\n", df.head())

# 3️⃣ حساب المتوسط والمجموع للـ Booking Value و Ride Distance
print("\nTotal Booking Value:", df['Booking Value'].sum())
print("Average Booking Value:", df['Booking Value'].mean())

print("\nTotal Ride Distance:", df['Ride Distance'].sum())
print("Average Ride Distance:", df['Ride Distance'].mean())

# 4️⃣ ترتيب الرحلات حسب Booking Value (الأعلى أولاً)
df_sorted_value = df.sort_values(by='Booking Value', ascending=False)
print("\nTop 5 most expensive rides:\n", df_sorted_value.head())

# 5️⃣ اختيار الرحلات التي تتجاوز قيمة معينة (filter)
high_value_rides = df[df['Booking Value'] > 50]  # مثال: الرحلات التي تتجاوز 50
print("\nRides with Booking Value > 50:\n", high_value_rides.head())

# 6️⃣ تعديل أسماء السائقين (map/lambda) إلى lowercase
# في حال كان لديك عمود Driver Name استخدمه، أو Driver Ratings فقط إذا الاسم غير متوفر
if 'Driver Name' in df.columns:
    df['driver_name_clean'] = df['Driver Name'].map(lambda x: x.lower())
    print("\nDriver names cleaned:\n", df['driver_name_clean'].head())
else:
    print("\nColumn 'Driver Name' not found, skipping name cleaning.")

# 7️⃣ إنشاء معرفات وهمية لكل سائق (anonymization)
if 'Driver Name' in df.columns:
    drivers = df['Driver Name'].unique()
    driver_ids = {name: f"{name.lower().replace(' ','_')}_{random.randint(100,999)}" for name in drivers}
    print("\nDriver IDs:\n", driver_ids)

    # 8️⃣ إضافة العمود الجديد IDs إلى DataFrame
    df['driver_id'] = df['Driver Name'].map(driver_ids)
    print("\nDataFrame with driver_id:\n", df[['Driver Name','driver_id']].head())
else:
    print("\nColumn 'Driver Name' not found, skipping driver_id creation.")

# 9️⃣ حفظ نسخة جديدة من البيانات بعد التعديلات
df.to_csv(r"C:/Users/Amani/Desktop/DS project/archive/ncr_ride_bookings_cleaned.csv", index=False)
print("\nCleaned file saved successfully!")

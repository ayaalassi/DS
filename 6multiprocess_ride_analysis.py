import pandas as pd
import multiprocessing

file_path = r"C:/Users/Amani/Desktop/DS project/archive/ncr_ride_bookings.csv"

# Read first 5 rows to inspect columns
df = pd.read_csv(file_path, nrows=5)
print(df.columns.tolist())

# -----------------------------
def process_chunk(chunk):
    result = {}
    numeric_cols = [
        'Avg VTAT', 'Avg CTAT', 'Cancelled Rides by Customer',
        'Cancelled Rides by Driver', 'Incomplete Rides', 'Booking Value',
        'Ride Distance', 'Driver Ratings', 'Customer Rating'
    ]
    
    # Sum of numeric columns
    for col in numeric_cols:
        if col in chunk.columns:
            result[col] = chunk[col].sum()
    
    # Max & Min of Ride Distance and Booking Value
    if 'Ride Distance' in chunk.columns:
        result['Max Ride Distance'] = chunk['Ride Distance'].max()
        result['Min Ride Distance'] = chunk['Ride Distance'].min()
    if 'Booking Value' in chunk.columns:
        result['Max Booking Value'] = chunk['Booking Value'].max()
        result['Min Booking Value'] = chunk['Booking Value'].min()
    
    # Percentage of cancelled rides
    if 'Cancelled Rides by Customer' in chunk.columns and 'Booking ID' in chunk.columns:
        total_bookings = chunk.shape[0]
        result['Cancelled by Customer %'] = (chunk['Cancelled Rides by Customer'].sum() / total_bookings) * 100
    if 'Cancelled Rides by Driver' in chunk.columns and 'Booking ID' in chunk.columns:
        total_bookings = chunk.shape[0]
        result['Cancelled by Driver %'] = (chunk['Cancelled Rides by Driver'].sum() / total_bookings) * 100
    
    return result

# -----------------------------
def chunkify(file_path, chunksize=10000):
    for chunk in pd.read_csv(file_path, chunksize=chunksize):
        yield chunk

# -----------------------------
if __name__ == '__main__':
    print("CPU cores:", multiprocessing.cpu_count())

    pool = multiprocessing.Pool(processes=4)

    results = []
    for chunk in chunkify(file_path):
        results.append(pool.apply_async(process_chunk, args=(chunk,)))

    pool.close()
    pool.join()

    # Aggregate results
    final_result = {}
    for r in results:
        chunk_result = r.get()
        for col, val in chunk_result.items():
            if col in ['Max Ride Distance', 'Max Booking Value']:
                final_result[col] = max(final_result.get(col, val), val)
            elif col in ['Min Ride Distance', 'Min Booking Value']:
                final_result[col] = min(final_result.get(col, val), val)
            elif '%' in col:  # percentage columns
                final_result[col] = final_result.get(col, 0) + val
            else:  # sum columns
                final_result[col] = final_result.get(col, 0) + val

    # Average the percentages across chunks
    chunk_count = len(results)
    for col in final_result:
        if '%' in col:
            final_result[col] /= chunk_count

    print("Final analytics:")
    for col, val in final_result.items():
        print(f"{col}: {val}")

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    MinMaxScaler, StandardScaler, Normalizer, Binarizer,
    LabelEncoder, OneHotEncoder
)
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# --- Load dataset ---
file_path = r"C:/Users/Amani/Desktop/DS project/archive/ncr_ride_bookings.csv"
rides_df = pd.read_csv(file_path)

# --- Define numeric and categorical features ---
numeric_features = ['Booking Value', 'Ride Distance']
categorical_features = ['Vehicle Type', 'Payment Method']

# --- Step 1: Encode categorical columns with LabelEncoder first ---
# Create a copy to avoid modifying original df
rides_encoded = rides_df.copy()
label_encoders = {}
for col in categorical_features:
    le = LabelEncoder()
    # Fill missing values temporarily to fit LabelEncoder
    rides_encoded[col] = rides_encoded[col].fillna('Missing')
    rides_encoded[col] = le.fit_transform(rides_encoded[col])
    label_encoders[col] = le  # Save encoder for inverse transform if needed

# --- Pipeline for numeric features ---
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),   # Fill missing numeric values with mean
    ('minmax', MinMaxScaler()),                    # Scale values to 0-1
    ('standard', StandardScaler()),                # Standardize: mean=0, std=1
    ('normalize', Normalizer(norm='l2')),          # Normalize values (L2 norm)
    ('binarizer', Binarizer(threshold=0.5))       # Convert to 0/1 based on threshold
])

# --- Pipeline for categorical features ---
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),  # Fill missing categorical values
    ('onehot', OneHotEncoder(sparse_output=False))         # Convert to one-hot vectors
])

# --- Combine numeric and categorical pipelines ---
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='passthrough'  # Keep any other columns not specified
)

# --- Apply transformations ---
processed_data = preprocessor.fit_transform(rides_encoded)

# --- Create a DataFrame with proper column names ---
cat_columns = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_features)
all_columns = numeric_features + list(cat_columns) + [
    col for col in rides_encoded.columns if col not in numeric_features + categorical_features
]

processed_df = pd.DataFrame(processed_data, columns=all_columns)

# --- Optional: reorder columns like Dr's examples ---
# Example: ['Booking Value', 'Ride Distance', <OneHotCols>, <Other columns>]
processed_df = processed_df[numeric_features + list(cat_columns) + [
    col for col in rides_encoded.columns if col not in numeric_features + categorical_features
]]

# --- Display the first 5 rows ---
print(processed_df.head())

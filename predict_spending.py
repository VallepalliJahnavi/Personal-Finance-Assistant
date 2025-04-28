import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pickle
import boto3

# Load data
df = pd.read_csv('categorized_transactions.csv')

# Convert date to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Create new features
df['DayOfWeek'] = df['Date'].dt.dayofweek
df['Month'] = df['Date'].dt.month
df['PreviousSpending'] = df['Amount'].shift(1).fillna(method='bfill')

# Encode categories
label_encoder = LabelEncoder()
df['CategoryEncoded'] = label_encoder.fit_transform(df['SpendingCategory'])

# Define features and target
X = df[['DayOfWeek', 'Month', 'PreviousSpending', 'CategoryEncoded']]
y = df['Amount']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Save model using pickle
with open('spending_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as spending_model.pkl")

# Upload model to S3 (optional)
try:
    s3 = boto3.client('s3')
    bucket_name = 'cc-finance-bucket'  # change this
    s3.upload_file('spending_model.pkl', bucket_name, 'models/spending_model.pkl')
    print("✅ Model uploaded to S3 in folder: models/spending_model.pkl")
except Exception as e:
    print(f" S3 upload failed: {e}")

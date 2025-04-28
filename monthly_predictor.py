import pandas as pd
import boto3
import pickle
from io import BytesIO
from sklearn.preprocessing import LabelEncoder

# Step 1: Load model from S3
s3 = boto3.client('s3')
bucket_name = 'cc-finance-bucket'
model_key = 'models/spending_model.pkl'

model_obj = s3.get_object(Bucket=bucket_name, Key=model_key)
model = pickle.load(BytesIO(model_obj['Body'].read()))

print("✅ Model loaded from S3")

# Step 2: Load or simulate new month's transaction data
# For now, simulate 10 random transactions
data = {
    'Date': pd.date_range(start='2025-05-01', periods=10, freq='3D'),
    'SpendingCategory': ['Shopping', 'Groceries', 'Entertainment', 'Transportation', 'Gas', 'Utilities', 'Healthcare', 'Travel', 'Shopping', 'Restaurants'],
    'Amount': [50, 80, 30, 20, 45, 90, 75, 200, 55, 65]
}
new_df = pd.DataFrame(data)

# Step 3: Feature engineering
new_df['DayOfWeek'] = new_df['Date'].dt.dayofweek
new_df['Month'] = new_df['Date'].dt.month
new_df['PreviousSpending'] = new_df['Amount'].shift(1).bfill()

# Step 4: Encode categories (Important: MUST match the previous encoding)
label_encoder = LabelEncoder()
# simulate fitting using known categories from training
known_categories = ['Shopping', 'Gas', 'Entertainment', 'Travel', 'Restaurants', 'Groceries', 'Healthcare', 'Transportation', 'Utilities', 'Other']
label_encoder.fit(known_categories)

new_df['CategoryEncoded'] = label_encoder.transform(new_df['SpendingCategory'])

# Step 5: Select Features
X_new = new_df[['DayOfWeek', 'Month', 'PreviousSpending', 'CategoryEncoded']]

# Step 6: Predict future spending
new_df['PredictedAmount'] = model.predict(X_new)

print("✅ Future spending predicted for the next month!")

# Step 7: Save predictions
new_df.to_csv('predicted_next_month_spending.csv', index=False)
print("✅ Predictions saved as predicted_next_month_spending.csv")

# Step 8: (Optional) Upload predictions to S3
try:
    s3.upload_file('predicted_next_month_spending.csv', bucket_name, 'predictions/predicted_next_month_spending.csv')
    print("✅ Predictions uploaded to S3 at predictions/predicted_next_month_spending.csv")
except Exception as e:
    print(f"❌ Upload failed: {e}")

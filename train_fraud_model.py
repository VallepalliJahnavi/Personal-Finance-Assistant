import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load credit card dataset
df = pd.read_csv('ExportCleanedCreditcard_21Apr2025_1745206344195_part00000.csv')

# Assume 'Class' is the fraud label (adjust if needed)
X = df.drop('Class', axis=1)
y = df['Class']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train simple model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
with open('fraud_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Fraud model trained and saved!")

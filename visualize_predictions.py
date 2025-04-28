import pandas as pd
import matplotlib.pyplot as plt

# Load the predicted data
df = pd.read_csv('predicted_next_month_spending.csv')

# 📈 1. Line Chart: Actual vs Predicted Amount
plt.figure(figsize=(12,6))
plt.plot(df['Date'], df['Amount'], marker='o', label='Actual Amount')
plt.plot(df['Date'], df['PredictedAmount'], marker='x', linestyle='--', label='Predicted Amount')
plt.title('Actual vs Predicted Spending')
plt.xlabel('Date')
plt.ylabel('Amount ($)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('actual_vs_predicted_spending.png')
print("✅ Saved: actual_vs_predicted_spending.png")

# 📊 2. Bar Chart: Predicted Spending by Category
grouped = df.groupby('SpendingCategory')['PredictedAmount'].sum().sort_values(ascending=False)

plt.figure(figsize=(10,6))
grouped.plot(kind='bar', color='mediumseagreen')
plt.title('Predicted Total Spending by Category')
plt.xlabel('Spending Category')
plt.ylabel('Predicted Total Amount ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('predicted_spending_by_category.png')
print("✅ Saved: predicted_spending_by_category.png")

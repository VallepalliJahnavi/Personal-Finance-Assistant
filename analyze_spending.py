import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('categorized_transactions.csv')

# Group & sort
grouped = df.groupby("SpendingCategory")["Amount"].sum().sort_values(ascending=False)

# Bar plot with log scale
plt.figure(figsize=(12, 6))
grouped.plot(kind="bar", color='teal')
plt.yscale("log")
plt.title("Total Spending by Category (Log Scale)")
plt.xlabel("Spending Category")
plt.ylabel("Log Scale: Total Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("spending_by_category_log.png")

print(" Log-scaled bar graph saved as spending_by_category_log.png")

# Pie chart
plt.figure(figsize=(8, 8))
grouped = grouped[grouped > 0]  # remove zeroes
plt.pie(grouped, labels=grouped.index, autopct='%1.1f%%', startangle=140)
plt.title("Spending Share by Category")
plt.tight_layout()
plt.savefig("spending_pie_chart.png")

print(" Pie chart saved as spending_pie_chart.png")

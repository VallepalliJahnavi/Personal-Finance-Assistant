import boto3
import pandas as pd
import time

# 1. Connect to AWS Comprehend
comprehend = boto3.client('comprehend', region_name='us-east-1')

# 2. Load Transactions CSV (correct filename here)
df = pd.read_csv('ExportCleanedTransactions_21Apr2025_1745205457149_part00000.csv')
df = df.dropna(subset=['Description'])

# 3. Define Entity to Category Mapping
entity_to_category = {
    'Amazon': 'Shopping',
    'Shell': 'Gas',
    'Spotify': 'Entertainment',
    'Netflix': 'Entertainment',
    'Walmart': 'Groceries',
    'Target': 'Groceries',
    'Starbucks': 'Restaurants',
    'McDonalds': 'Restaurants',
    'Uber': 'Transportation',
    'Lyft': 'Transportation',
    'Chevron': 'Gas',
    'ExxonMobil': 'Gas',
    'Best Buy': 'Electronics',
    'Apple': 'Electronics',
    'Home Depot': 'Home Improvement',
    'Lowe\'s': 'Home Improvement',
    'AT&T': 'Utilities',
    'Verizon': 'Utilities',
    'Comcast': 'Utilities',
    'Chase': 'Banking',
    'Wells Fargo': 'Banking',
    'Bank of America': 'Banking',
    'Costco': 'Groceries',
    'CVS': 'Healthcare',
    'Walgreens': 'Healthcare',
    'Kroger': 'Groceries',
    'Publix': 'Groceries',
    'Safeway': 'Groceries',
    'Southwest Airlines': 'Travel',
    'Delta Airlines': 'Travel',
    'United Airlines': 'Travel',
    'American Airlines': 'Travel',
    'Airbnb': 'Travel',
    'Marriott': 'Travel',
    'Hilton': 'Travel',
    'Expedia': 'Travel',
}


# 4. Function to Map Entities
def map_to_category(entities):
    for entity in entities:
        entity_text = entity['Text']
        for known_entity in entity_to_category:
            if known_entity.lower() in entity_text.lower():
                return entity_to_category[known_entity]
    return 'Other'

# 5. Detect Entities and Categorize
categories = []

for desc in df['Description']:
    try:
        response = comprehend.detect_entities(Text=desc, LanguageCode='en')
        category = map_to_category(response['Entities'])
    except Exception as e:
        print(f"Error processing: {desc} - {str(e)}")
        category = 'Other'
    categories.append(category)
    time.sleep(0.3)  # avoid throttling

# 6. Save Final CSV
df['SpendingCategory'] = categories
df.to_csv('categorized_transactions.csv', index=False)

print(" Categorization complete! Saved as categorized_transactions.csv")

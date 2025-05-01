# Personal-Finance-Assistant

### 📄 **Project Description:**

> We developed a full-stack personal finance analytics and fraud detection system by integrating multiple AWS services with Python-based machine learning workflows.  
> The solution processes raw transaction data to categorize expenses, generate visual spending insights, predict future spending trends, and detect potential credit card fraud.  
> It also triggers real-time email alerts via Amazon SNS when suspicious activity is identified.

### 🔧 **Key Components & Technologies Used:**

- **AWS S3:** Cloud storage for raw, cleaned, and model files  
- **AWS Glue DataBrew:** No-code data cleaning and preprocessing  
- **Amazon Comprehend:** Entity detection from transaction descriptions (for categorization)  
- **EC2 (Amazon Linux):** Python environment for model training, visualization, and deployment  
- **scikit-learn:** Used for regression (spending prediction) and classification (fraud detection)  
- **Matplotlib:** Bar charts for spending patterns  
- **Amazon SNS:** Sends real-time email alerts on fraud detection  
- **boto3:** Programmatic AWS access in Python

### ✅ **Features:**

- 📊 Categorizes transactions using NLP (Amazon Comprehend)  
- 📈 Analyzes and visualizes spending by category  
- 🤖 Predicts next month's spending using Linear Regression  
- 🔍 Detects fraudulent transactions using a trained Random Forest Classifier  
- 📩 Sends fraud alerts instantly via Amazon SNS  
- 💡 Deployable with minimal cost using free-tier AWS resources (no SageMaker or Lambda required)

Datasets: 
1)Transaction analysis dataset - https://www.kaggle.com/datasets/bukolafatunde/personal-finance
Columns present in this dataset:
Date
Description(Ex: Amazon, Spotify, Shell..)
Amount
Transaction(Ex:Credit or Debit)
Account Name(Ex: Checking, silver card..)

2)Fraud Detection Analysis - https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/data
Columns present in this dataset:
Time
V1...V28(PCA Dimensionality reduction
to protect user identities and sensitive
features)
Amount
Class(0-not fraudulent, 1- fraudulent)

STEP 1: Set up AWS Environment
* Created AWS account
* Set up AWS S3 bucket (cc-finance-bucket) to store datasets

STEP 2: Upload Raw Datasets to S3
* Uploaded:
    * personal_transactions.csv
    * creditcard.csv into the S3 bucket

STEP 3: Clean Data using AWS Glue DataBrew
* Opened AWS Glue DataBrew (no-code visual data wrangling tool)
* Created Projects for:
    * personal_transactions.csv
    * creditcard.csv
* Used DataBrew visual tools to:
    * Fix date columns
    * Drop empty/missing values
    * Convert "Credit"/"Debit" to numeric values (0/1)
    * Standardize column names
* Exported cleaned datasets:
    * ExportCleanedTransactions_21Apr2025_...
    * ExportCleanedCreditcard_21Apr2025_...
* Exported cleaned files back into S3
    NO EC2 manual cleaning required — Glue DataBrew handled it graphically!

STEP 4: Categorize Spending (Behavior Analysis)
* Used EC2 to run Python script
* Used AWS Comprehend for entity detection from transaction descriptions
* Categorized transaction types (e.g., Amazon → Shopping, Shell → Gas)
   Saved: categorized_transactions.csv

STEP 5: Analyze Spending Patterns
* Used Matplotlib locally
* Grouped by Spending Category
* Summed total Amount
* Created bar graphs for visualization
* Saved graphs as .png files

STEP 6: Predict Next Month’s Spending (Regression)
* Trained a Linear Regression model:
    * Features: Day of Week, Previous Spending, Category
* Saved model as: spending_model.pkl
* Uploaded to S3

STEP 7: Fraud Detection Model
* Trained a Random Forest Classifier on ExportCleanedCreditcard.csv
* Saved trained model as: fraud_model.pkl
* Uploaded to S3 inside fraud/ folder

STEP 8: Decided NO Lambda (due to deployment size issue)
* Originally tried AWS Lambda
* Zip file with numpy + scikit-learn exceeded AWS Lambda size limit
*  Smartly switched to Local MacBook setup for fraud detection

   STEP 9: Local Fraud Detection Script
* Wrote and ran predict_fraud.py locally
* Used Python to:
    * Load fraud_model.pkl
    * Predict if a transaction is fraud
 No AWS SageMaker used, no Lambda.

 STEP 10: AWS IAM Setup for Access
* Created IAM user with Programmatic Access
* Attached AmazonSNSFullAccess policy
* Generated Access Key ID and Secret Access Key for boto3 usage

 STEP 11: Setup SNS for Alerts
* Created SNS Topic fraud-alerts
* Subscribed personal email to topic
* Confirmed subscription via email
 Ready to receive fraud alerts

 STEP 12: Full Fraud Detection + SNS Alerts Working
* Ran local prediction
* If transaction is legit → Print "Transaction is Legit"
* If transaction is fraud → Triggered SNS Email Alert 
* Email delivered successfully via AWS SNS

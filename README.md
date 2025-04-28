# Personal-Finance-Assistant
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

import pandas as pd
import datetime as dt

print("Loading and cleaning data...")
df = pd.read_excel('Online Retail.xlsx')

# 1. Data Cleaning
df.dropna(subset=['CustomerID'], inplace=True)
df['InvoiceNo'] = df['InvoiceNo'].astype(str)
df = df[~df['InvoiceNo'].str.startswith('C')]
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
df['TotalSum'] = df['Quantity'] * df['UnitPrice']

print("Data cleaning complete!")
print("-" * 50)

print("Generating Cohort Analysis Matrix...")

# 2. Get the month of each transaction
def get_month(x):
    return dt.datetime(x.year, x.month, 1)

df['InvoiceMonth'] = df['InvoiceDate'].apply(get_month)

# 3. Find the first purchase month (Cohort Month) for each customer
df['CohortMonth'] = df.groupby('CustomerID')['InvoiceMonth'].transform('min')

# 4. Calculate the time offset (in months) between purchase month and cohort month
def get_date_int(dataframe, column):
    year = dataframe[column].dt.year
    month = dataframe[column].dt.month
    return year, month

invoice_year, invoice_month = get_date_int(df, 'InvoiceMonth')
cohort_year, cohort_month = get_date_int(df, 'CohortMonth')

years_diff = invoice_year - cohort_year
months_diff = invoice_month - cohort_month

# Calculate month index (0 represents the first month of purchase)
df['CohortIndex'] = years_diff * 12 + months_diff

# 5. Group by CohortMonth and CohortIndex to count unique customers
cohort_data = df.groupby(['CohortMonth', 'CohortIndex'])['CustomerID'].nunique().reset_index()

# 6. Pivot the data to create a cohort matrix
cohort_matrix = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='CustomerID')

# 7. Calculate retention percentages
cohort_sizes = cohort_matrix.iloc[:, 0]
retention = cohort_matrix.divide(cohort_sizes, axis=0)
retention = retention.round(3) * 100

print("Cohort Analysis Complete!")
print("-" * 50)

print("Customer Retention Rate Matrix (Percentage %):")
# Showing the first few rows of the retention table
print(retention.head())
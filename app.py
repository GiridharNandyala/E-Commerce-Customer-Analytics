import streamlit as st
import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt

# Set Page Configuration
st.set_page_config(page_title="E-Commerce Analytics Dashboard", layout="wide")

st.title("E-Commerce Customer Analytics Dashboard")
st.markdown("This dashboard showcases **RFM Customer Segmentation** and **Cohort Retention Analysis** using Python.")

@st.cache_data
def load_and_process_data():
    # Load Data
    df = pd.read_excel('Online Retail.xlsx')
    
    # Clean Data
    df.dropna(subset=['CustomerID'], inplace=True)
    df['InvoiceNo'] = df['InvoiceNo'].astype(str)
    df = df[~df['InvoiceNo'].str.startswith('C')]
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    df['TotalSum'] = df['Quantity'] * df['UnitPrice']
    
    # 1. RFM Calculation
    latest_date = df['InvoiceDate'].max()
    snapshot_date = latest_date + dt.timedelta(days=1)
    
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalSum': 'sum'
    }).rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'TotalSum': 'Monetary'})
    
    # Scoring
    rfm['R'] = pd.qcut(rfm['Recency'], q=4, labels=[4, 3, 2, 1])
    rfm['F'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4])
    rfm['M'] = pd.qcut(rfm['Monetary'], q=4, labels=[1, 2, 3, 4])
    
    def segment_me(row):
        r, f = int(row['R']), int(row['F'])
        if r == 4 and f == 4: return 'VIP Customers'
        elif r >= 3 and f >= 3: return 'Loyal Customers'
        elif r <= 2 and f >= 3: return 'At Risk / Churn Risk'
        elif r <= 2 and f <= 2: return 'Lost Customers'
        else: return 'Regular Customers'
        
    rfm['Customer_Segment'] = rfm.apply(segment_me, axis=1)
    
    # 2. Cohort Calculation
    df['InvoiceMonth'] = df['InvoiceDate'].apply(lambda x: dt.datetime(x.year, x.month, 1))
    df['CohortMonth'] = df.groupby('CustomerID')['InvoiceMonth'].transform('min')
    
    df['CohortIndex'] = (df['InvoiceMonth'].dt.year - df['CohortMonth'].dt.year) * 12 + (df['InvoiceMonth'].dt.month - df['CohortMonth'].dt.month)
    cohort_data = df.groupby(['CohortMonth', 'CohortIndex'])['CustomerID'].nunique().reset_index()
    cohort_matrix = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='CustomerID')
    
    retention = cohort_matrix.divide(cohort_matrix.iloc[:, 0], axis=0).round(3) * 100
    retention.index = retention.index.strftime('%Y-%m')
    
    return rfm, retention

# Load processed analytics data
rfm, retention = load_and_process_data()

# Layout Tabs
tab1, tab2 = st.tabs(["RFM Customer Segmentation", "Cohort Retention Analysis"])

with tab1:
    st.header("Customer Segmentation Breakdown")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers Analyzed", f"{len(rfm):,}")
    col2.metric("VIP Customers", f"{len(rfm[rfm['Customer_Segment'] == 'VIP Customers']):,}")
    col3.metric("At Risk Customers", f"{len(rfm[rfm['Customer_Segment'] == 'At Risk / Churn Risk']):,}")
    
    # Filter Dropdown
    segment = st.selectbox("Select Segment to View Customer List:", rfm['Customer_Segment'].unique())
    filtered_rfm = rfm[rfm['Customer_Segment'] == segment]
    st.dataframe(filtered_rfm[['Recency', 'Frequency', 'Monetary', 'Customer_Segment']].head(100), use_container_width=True)

with tab2:
    st.header("Monthly Customer Retention Rate (%)")
    st.write("This heatmap shows the percentage of customers returning in subsequent months.")
    
    # Adjusted size and layouts for perfect screen fit
    fig, ax = plt.subplots(figsize=(16, 10))
    
    sns.heatmap(
        data=retention, 
        annot=True, 
        fmt='.1f', 
        cmap='YlGnBu', 
        cbar_kws={'label': 'Retention %'}, 
        vmin=0, 
        vmax=50,
        linewidths=0.5,
        annot_kws={"size": 10}
    )
    
    plt.title('Customer Retention Heatmap', fontsize=16, pad=20)
    plt.ylabel('Cohort Month', fontsize=12)
    plt.xlabel('Months Passed (Cohort Index)', fontsize=12)
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    st.pyplot(fig)
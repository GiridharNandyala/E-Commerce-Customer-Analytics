# E-Commerce Customer Analytics Dashboard

An interactive Data Analytics dashboard built using Python and Streamlit to analyze e-commerce transaction data. This project implements **RFM (Recency, Frequency, Monetary) Customer Segmentation** and **Monthly Cohort Retention Analysis** to derive actionable business insights.

## 🚀 Features
* **RFM Segmentation:** Categorizes customers into value-based groups like VIP, Loyal, At-Risk, and Lost to guide targeted marketing strategies.
* **Cohort Retention Heatmap:** Tracks monthly customer retention rates using a visual Seaborn heatmap to monitor user engagement over time.
* **Interactive Filtering:** Allows users to dynamically filter and view specific customer lists directly through the Streamlit UI.

## 📁 Repository Structure
* `analysis.py`: Main data analytics script containing core logic for data cleaning, RFM scoring, and cohort calculations.
* `app.py`: Streamlit web application code that builds the interactive frontend dashboard and visualizations.
* `requirements.txt`: List of Python libraries required to run the project.
* `Online Retail.xlsx`: The original transaction dataset used for the analysis.

## 📊 Project Preview & Documentation

📺 Video Demo:https://github.com/GiridharNandyala/E-Commerce-Customer-Analytics/blob/main/E-Commenrece-Analysis-Dashboard.mp4

## 🛠️ Tech Stack
* **Language:** Python
* **Libraries:** Streamlit, Pandas, Openpyxl, Seaborn, Matplotlib

## 📦 Installation & Setup
1. Clone this repository to your local machine.
2. Install all required dependencies:
   ```bash
   pip install -r requirements.txt

   Run the interactive Streamlit dashboard:
streamlit run app.py

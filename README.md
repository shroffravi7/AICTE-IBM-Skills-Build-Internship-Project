🛒 Supermarket Sales Analysis Dashboard

A complete Supermarket Sales Analysis project built with Python, Pandas, Plotly, and Streamlit.

The project analyzes supermarket transactions to understand sales performance, products, branches, customer types, payment methods, quantities, and customer ratings. The results are presented through an interactive web dashboard.

📊 Project Overview

Supermarkets generate a large amount of transaction data every day. Analyzing this data can help identify:

High-performing products

High-performing branches

Popular product categories

Common payment methods

Customer purchasing behavior

Customer satisfaction through ratings

Sales and transaction performance

This project converts supermarket transaction data into useful business insights through data analysis and visualization.

🎯 Objectives

Load and analyze supermarket sales data.

Check the dataset for missing or incorrect values.

Calculate sales using quantity and unit price where required.

Analyze sales by product and category.

Compare branch and city performance.

Analyze customer types and purchasing behavior.

Analyze payment method usage.

Study customer ratings.

Create clear visualizations.

Build an interactive Streamlit dashboard.

🛠️ Technologies Used

Technology

Purpose

Python

Data analysis and application development

Pandas

Data cleaning and analysis

Plotly

Interactive charts

Streamlit

Interactive dashboard

CSV

Sales dataset storage

VS Code

Development environment

📁 Project Structure

SuperMarket/
│
├── app.py
├── supermarket_sales.csv
├── supermarket_sales_analysis.py
├── create_dataset.py
├── requirements.txt
├── README.md
│
├── output/
│   ├── product_sales.csv
│   ├── branch_sales.csv
│   ├── category_sales.csv
│   ├── payment_summary.csv
│   └── charts/
│
└── venv/

venv/ is a local Python virtual environment and normally should not be uploaded to GitHub. Add it to .gitignore.

📄 Dataset

The project uses a supermarket transaction CSV file.

Typical fields include:

Transaction ID

Product

Branch

City

Category / Product Line

Customer Type

Quantity

Unit Price

Payment

Rating

Sales

The dashboard automatically calculates sales from:

Sales = Quantity × Unit Price

when a sales column is not already available.

📈 Dashboard Features

The Streamlit dashboard contains a clean, modern interface with a dark navigation sidebar and a responsive analytics area. No filter panel is included.

📊 Dashboard

The main dashboard displays:

Total Sales

Total Transactions

Total Quantity

Average Rating

Average Transaction

It also provides key insights such as:

🏆 Top Product Line

🏬 Highest Sales Branch

💳 Most Used Payment Method

📦 Products

Product-wise sales

Quantity sold

Number of transactions

Product performance comparison

🏬 Branches

Sales by branch

City performance

Transaction counts

Quantity sold

💳 Payments

Payment method usage

Sales by payment method

Average transaction value

👥 Customers

Customer type distribution

Sales by customer type

Average transaction value

Quantity purchased

⭐ Ratings

Average rating

Highest rating

Lowest rating

Rating distribution

📊 Visualizations

The dashboard uses Plotly to create interactive charts including:

Sales by Product Line

Sales by Branch

Top 5 Products by Sales

Payment Method Usage

Customer Type Distribution

Ratings Distribution

Branch Sales Comparison

Sales by Customer Type

🚀 How to Run the Project

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/supermarket-sales-analysis.git
cd supermarket-sales-analysis

2. Create a virtual environment

python -m venv venv

Activate it on Windows:

.\venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

Main packages:

streamlit
pandas
plotly

4. Add the dataset

Place your CSV file in the project root:

supermarket_sales.csv

The structure should look like:

SuperMarket/
├── app.py
├── supermarket_sales.csv
├── requirements.txt
└── README.md

5. Run the dashboard

python -m streamlit run app.py

On Windows, you can also use:

.\venv\Scripts\python.exe -m streamlit run app.py

Then open the local Streamlit address, normally:

http://localhost:8501

🔍 Data Analysis Workflow

Raw Sales Data
      ↓
Data Loading
      ↓
Data Cleaning
      ↓
Missing / Invalid Value Check
      ↓
Sales Calculation
      ↓
Grouping & Aggregation
      ↓
Data Visualization
      ↓
Business Insights
      ↓
Interactive Dashboard

💡 Business Insights

The analysis can help supermarket management:

Stock products with high sales.

Identify categories generating strong revenue.

Compare branch performance.

Understand customer purchasing patterns.

Support commonly used payment methods.

Monitor customer ratings and service quality.

Develop targeted customer or membership offers.

Use sales data to improve inventory and business decisions.

🖥️ Dashboard Layout

┌─────────────────────────────────────────────────────────┐
│              Supermarket Sales Dashboard                │
├────────────┬────────────┬────────────┬─────────────────┤
│ Total Sales│Transactions│  Quantity  │ Average Rating  │
├────────────┴────────────┴────────────┴─────────────────┤
│                    Key Insights                         │
├─────────────────────────┬───────────────────────────────┤
│ Sales by Product Line   │ Sales by Branch               │
├─────────────────────────┴───────────────────────────────┤
│ Top Products │ Payments │ Customers │ Ratings           │
└─────────────────────────────────────────────────────────┘

📌 Important Note About the Dataset

The dashboard calculates its displayed values directly from the CSV file placed in the project folder. Therefore, dashboard results can differ if a different supermarket dataset is used.

🔮 Future Improvements

Add date/time-based sales analysis.

Add monthly and yearly sales trends.

Add sales forecasting.

Add inventory analysis.

Add profit and margin analysis.

Add downloadable reports.

Add authentication for dashboard users.

Deploy the dashboard online.

Connect the dashboard to a live database.

👨‍💻 Author

Ravi Shroff

Supermarket Sales Analysis — Data Analytics Project

⭐ If You Like This Project

If this project helped you understand supermarket sales analysis, feel free to:

⭐ Star the repository

🍴 Fork the repository

💡 Suggest improvements

🐛 Report issues

📜 License

This project is intended for educational and data analytics purposes.

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================
# SUPERMARKET SALES ANALYSIS PROJECT
# ==========================================

# File settings
CSV_FILE = "supermarket_sales.csv"
OUTPUT_FOLDER = Path("output")

# Create output folder
OUTPUT_FOLDER.mkdir(exist_ok=True)

print("=" * 60)
print("       SUPERMARKET SALES ANALYSIS")
print("=" * 60)


# ==========================================
# 1. LOAD DATASET
# ==========================================

try:
    df = pd.read_csv(CSV_FILE)
    print("\nDataset loaded successfully!")
except FileNotFoundError:
    print("\nERROR: supermarket_sales.csv file not found.")
    print("Please put the CSV file in the same folder as this Python file.")
    exit()


print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Records:")
print(df.head())


# ==========================================
# 2. CLEAN COLUMN NAMES
# ==========================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nColumns:")
print(df.columns.tolist())


# ==========================================
# 3. CHECK MISSING VALUES
# ==========================================

print("\n" + "=" * 60)
print("DATA QUALITY CHECK")
print("=" * 60)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())


# ==========================================
# 4. FIND IMPORTANT COLUMNS
# ==========================================

def find_column(possible_names):

    for name in possible_names:

        if name in df.columns:
            return name

    return None


product_col = find_column([
    "product",
    "product_name",
    "item"
])

branch_col = find_column([
    "branch"
])

city_col = find_column([
    "city"
])

customer_col = find_column([
    "customer_type",
    "customer"
])

quantity_col = find_column([
    "quantity",
    "qty"
])

price_col = find_column([
    "unit_price",
    "price",
    "unitprice"
])

payment_col = find_column([
    "payment",
    "payment_method"
])

rating_col = find_column([
    "rating",
    "customer_rating"
])

sales_col = find_column([
    "sales",
    "total",
    "total_sales",
    "revenue"
])

category_col = find_column([
    "category",
    "product_category"
])


print("\nDetected Columns:")
print("Product   :", product_col)
print("Branch    :", branch_col)
print("City      :", city_col)
print("Customer  :", customer_col)
print("Quantity  :", quantity_col)
print("Price     :", price_col)
print("Payment   :", payment_col)
print("Rating    :", rating_col)
print("Sales     :", sales_col)
print("Category  :", category_col)


# ==========================================
# 5. CONVERT NUMERIC DATA
# ==========================================

for column in [
    quantity_col,
    price_col,
    rating_col,
    sales_col
]:

    if column is not None:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ==========================================
# 6. CALCULATE SALES
# ==========================================

print("\n" + "=" * 60)
print("SALES CALCULATION")
print("=" * 60)

if quantity_col and price_col:

    df["calculated_sales"] = (
        df[quantity_col] *
        df[price_col]
    )

    print("\nSales calculated using:")

    print("Sales = Quantity × Unit Price")

    # If dataset does not have sales column
    if sales_col is None:

        df["sales"] = df["calculated_sales"]

        sales_col = "sales"


# ==========================================
# 7. TOTAL SALES
# ==========================================

if sales_col:

    total_sales = df[sales_col].sum()

    average_sales = df[sales_col].mean()

    print("\nTotal Sales:")
    print(f"₹{total_sales:,.2f}")

    print("\nAverage Transaction:")
    print(f"₹{average_sales:,.2f}")


# ==========================================
# 8. PRODUCT ANALYSIS
# ==========================================

if product_col and sales_col:

    print("\n" + "=" * 60)
    print("PRODUCT ANALYSIS")
    print("=" * 60)

    product_sales = (
        df.groupby(product_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nSales by Product:")
    print(product_sales)

    highest_product = product_sales.idxmax()

    highest_product_sales = product_sales.max()

    print("\nHighest Selling Product:")
    print(highest_product)

    print(f"Sales: ₹{highest_product_sales:,.2f}")

    # Save result
    product_sales.to_csv(
        OUTPUT_FOLDER / "product_sales.csv"
    )

    # Chart
    plt.figure(figsize=(10, 6))

    product_sales.sort_values().plot(
        kind="barh"
    )

    plt.title("Sales by Product")
    plt.xlabel("Sales (₹)")
    plt.ylabel("Product")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "product_sales.png"
    )

    plt.close()


# ==========================================
# 9. BRANCH ANALYSIS
# ==========================================

if branch_col and sales_col:

    print("\n" + "=" * 60)
    print("BRANCH ANALYSIS")
    print("=" * 60)

    branch_sales = (
        df.groupby(branch_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nSales by Branch:")
    print(branch_sales)

    best_branch = branch_sales.idxmax()

    best_branch_sales = branch_sales.max()

    print("\nBest Performing Branch:")
    print(best_branch)

    print(
        f"Sales: ₹{best_branch_sales:,.2f}"
    )

    branch_sales.to_csv(
        OUTPUT_FOLDER / "branch_sales.csv"
    )

    plt.figure(figsize=(8, 5))

    branch_sales.plot(
        kind="bar"
    )

    plt.title("Sales by Branch")
    plt.xlabel("Branch")
    plt.ylabel("Sales (₹)")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "branch_sales.png"
    )

    plt.close()


# ==========================================
# 10. CITY ANALYSIS
# ==========================================

if city_col and sales_col:

    print("\n" + "=" * 60)
    print("CITY ANALYSIS")
    print("=" * 60)

    city_sales = (
        df.groupby(city_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nSales by City:")
    print(city_sales)

    city_sales.to_csv(
        OUTPUT_FOLDER / "city_sales.csv"
    )

    plt.figure(figsize=(8, 5))

    city_sales.plot(
        kind="bar"
    )

    plt.title("Sales by City")
    plt.xlabel("City")
    plt.ylabel("Sales (₹)")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "city_sales.png"
    )

    plt.close()


# ==========================================
# 11. CATEGORY ANALYSIS
# ==========================================

if category_col and sales_col:

    print("\n" + "=" * 60)
    print("CATEGORY ANALYSIS")
    print("=" * 60)

    category_sales = (
        df.groupby(category_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nSales by Category:")
    print(category_sales)

    highest_category = category_sales.idxmax()

    highest_category_sales = category_sales.max()

    print("\nHighest Selling Category:")
    print(highest_category)

    print(
        f"Sales: ₹{highest_category_sales:,.2f}"
    )

    category_sales.to_csv(
        OUTPUT_FOLDER / "category_sales.csv"
    )

    plt.figure(figsize=(10, 6))

    category_sales.plot(
        kind="bar"
    )

    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales (₹)")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "category_sales.png"
    )

    plt.close()


# ==========================================
# 12. PAYMENT METHOD ANALYSIS
# ==========================================

if payment_col:

    print("\n" + "=" * 60)
    print("PAYMENT METHOD ANALYSIS")
    print("=" * 60)

    payment_count = df[
        payment_col
    ].value_counts()

    print("\nPayment Method Usage:")
    print(payment_count)

    popular_payment = payment_count.idxmax()

    popular_payment_count = payment_count.max()

    print("\nMost Popular Payment Method:")
    print(popular_payment)

    print(
        f"Transactions: {popular_payment_count}"
    )

    payment_count.to_csv(
        OUTPUT_FOLDER / "payment_methods.csv"
    )

    plt.figure(figsize=(8, 5))

    payment_count.plot(
        kind="bar"
    )

    plt.title("Payment Method Usage")
    plt.xlabel("Payment Method")
    plt.ylabel("Number of Transactions")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "payment_methods.png"
    )

    plt.close()


# ==========================================
# 13. MEMBER VS NORMAL CUSTOMER
# ==========================================

if customer_col and sales_col:

    print("\n" + "=" * 60)
    print("CUSTOMER TYPE ANALYSIS")
    print("=" * 60)

    customer_analysis = (
        df.groupby(customer_col)[sales_col]
        .agg([
            "count",
            "sum",
            "mean"
        ])
    )

    print("\nCustomer Analysis:")
    print(customer_analysis)

    customer_analysis.to_csv(
        OUTPUT_FOLDER /
        "customer_type_analysis.csv"
    )

    print("\nAverage Transaction:")

    for customer_type, row in customer_analysis.iterrows():

        print(
            f"{customer_type}: "
            f"₹{row['mean']:,.2f}"
        )

    plt.figure(figsize=(8, 5))

    customer_analysis["mean"].plot(
        kind="bar"
    )

    plt.title(
        "Average Transaction by Customer Type"
    )

    plt.xlabel("Customer Type")

    plt.ylabel(
        "Average Sales (₹)"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER /
        "customer_type.png"
    )

    plt.close()


# ==========================================
# 14. CUSTOMER RATING
# ==========================================

if rating_col:

    print("\n" + "=" * 60)
    print("CUSTOMER RATING ANALYSIS")
    print("=" * 60)

    average_rating = df[
        rating_col
    ].mean()

    print(
        f"\nAverage Customer Rating: "
        f"{average_rating:.2f} / 5"
    )

    plt.figure(figsize=(8, 5))

    df[rating_col].dropna().plot(
        kind="hist",
        bins=10
    )

    plt.title(
        "Customer Rating Distribution"
    )

    plt.xlabel("Rating")

    plt.ylabel(
        "Number of Customers"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER /
        "rating_distribution.png"
    )

    plt.close()


# ==========================================
# 15. FINAL BUSINESS INSIGHTS
# ==========================================

print("\n" + "=" * 60)
print("BUSINESS INSIGHTS")
print("=" * 60)

if product_col and sales_col:

    print(
        f"\n1. {highest_product} "
        f"is the highest-selling product."
    )

if branch_col and sales_col:

    print(
        f"2. Branch {best_branch} "
        f"has the highest sales."
    )

if category_col and sales_col:

    print(
        f"3. {highest_category} "
        f"is the highest-selling category."
    )

if payment_col:

    print(
        f"4. {popular_payment} "
        f"is the most-used payment method."
    )

if rating_col:

    print(
        f"5. Average customer rating is "
        f"{average_rating:.2f}/5."
    )


# ==========================================
# 16. SAVE CLEANED DATA
# ==========================================

df.to_csv(
    OUTPUT_FOLDER /
    "cleaned_supermarket_sales.csv",
    index=False
)


# ==========================================
# PROJECT COMPLETED
# ==========================================

print("\n" + "=" * 60)

print(
    "PROJECT COMPLETED SUCCESSFULLY!"
)

print(
    f"All charts and results are saved in: "
    f"{OUTPUT_FOLDER.absolute()}"
)

print("=" * 60)
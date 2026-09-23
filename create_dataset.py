import pandas as pd
import random

# ==========================================
# CREATE SUPERMARKET SALES CSV
# ==========================================

products = [
    "Cheese",
    "Milk",
    "Bread",
    "Biscuits",
    "Coffee",
    "Tea",
    "Juice",
    "Soft Drinks",
    "Chips",
    "Chocolate"
]

branches = ["A", "B", "C"]

cities = {
    "A": "Delhi",
    "B": "Pune",
    "C": "Mumbai"
}

customer_types = [
    "Member",
    "Normal"
]

payments = [
    "UPI",
    "Cash",
    "Credit Card",
    "Debit Card"
]

categories = [
    "Beverages",
    "Food",
    "Dairy",
    "Snacks"
]

data = []

# Create 500 transactions
for i in range(500):

    product = random.choice(products)

    branch = random.choice(branches)

    city = cities[branch]

    customer_type = random.choice(customer_types)

    quantity = random.randint(1, 10)

    unit_price = round(
        random.uniform(20, 1000),
        2
    )

    payment = random.choice(payments)

    rating = round(
        random.uniform(1, 5),
        2
    )

    category = random.choice(categories)

    # Sales calculation
    sales = round(
        quantity * unit_price,
        2
    )

    data.append([
        i + 1,
        product,
        branch,
        city,
        category,
        customer_type,
        quantity,
        unit_price,
        payment,
        rating,
        sales
    ])


# Create DataFrame
df = pd.DataFrame(
    data,
    columns=[
        "Transaction_ID",
        "Product",
        "Branch",
        "City",
        "Category",
        "Customer_Type",
        "Quantity",
        "Unit_Price",
        "Payment",
        "Rating",
        "Sales"
    ]
)


# Save CSV
df.to_csv(
    "supermarket_sales.csv",
    index=False
)

print("======================================")
print("SUPERMARKET SALES DATASET CREATED")
print("======================================")

print("\nTotal Records:")
print(len(df))

print("\nFirst 10 Records:")
print(df.head(10))

print("\nCSV file created successfully:")
print("supermarket_sales.csv")
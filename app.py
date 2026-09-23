import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# SUPERMARKET SALES DASHBOARD
# Clean dashboard inspired by the reference design
# No filters
# ============================================================

st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: #f5f7fb;
    }

    [data-testid="stSidebar"] {
        background: #172033;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        padding: 8px 10px;
        border-radius: 8px;
    }

    .brand {
        font-size: 25px;
        font-weight: 800;
        padding: 12px 5px 28px 5px;
        color: white;
    }

    .page-title {
        font-size: 34px;
        line-height: 1.1;
        font-weight: 800;
        color: #172033;
        margin: 0;
    }

    .page-subtitle {
        color: #60708a;
        font-size: 17px;
        margin-top: 7px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 23px;
        font-weight: 800;
        color: #172033;
        margin: 22px 0 13px 0;
    }

    .kpi {
        background: #ffffff;
        border-radius: 15px;
        padding: 18px 20px;
        min-height: 108px;
        box-shadow: 0 5px 18px rgba(31, 48, 75, 0.08);
    }

    .kpi-label {
        color: #60708a;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #172033;
        font-size: 26px;
        font-weight: 800;
    }

    .insight {
        background: #ffffff;
        border-radius: 14px;
        border-left: 5px solid #2f80ed;
        padding: 17px 20px;
        min-height: 82px;
        box-shadow: 0 5px 18px rgba(31, 48, 75, 0.07);
    }

    .insight-label {
        color: #60708a;
        font-size: 14px;
        margin-bottom: 5px;
    }

    .insight-value {
        color: #172033;
        font-size: 20px;
        font-weight: 800;
    }

    .chart-card {
        background: white;
        border-radius: 15px;
        padding: 4px 8px 0 8px;
        box-shadow: 0 5px 18px rgba(31, 48, 75, 0.06);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    div[data-testid="stMetric"] {
        background: white;
        border-radius: 14px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    files = [
        "supermarket_sales.csv",
        "supermarket_sales_demo.csv",
        "data/supermarket_sales.csv",
    ]

    df = None

    for file in files:
        try:
            df = pd.read_csv(file)
            break
        except FileNotFoundError:
            pass

    if df is None:
        st.error(
            "CSV file not found. Put 'supermarket_sales.csv' in the same folder as app.py."
        )
        st.stop()

    # Standardize column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    # Common column aliases
    aliases = {
        "sales_amount": "sales",
        "total_sales": "sales",
        "revenue": "sales",
        "price": "unit_price",
        "qty": "quantity",
        "units": "quantity",
        "payment_method": "payment",
        "product_line": "category",
        "customer": "customer_type",
        "customer_category": "customer_type",
    }

    for old, new in aliases.items():
        if old in df.columns and new not in df.columns:
            df[new] = df[old]

    # Calculate sales when necessary
    if "sales" not in df.columns and {"quantity", "unit_price"}.issubset(df.columns):
        df["sales"] = df["quantity"] * df["unit_price"]

    # Make sure important columns exist
    defaults = {
        "product": "Unknown",
        "branch": "Unknown",
        "city": "Unknown",
        "category": "Unknown",
        "customer_type": "Unknown",
        "payment": "Unknown",
        "quantity": 0,
        "sales": 0,
        "rating": None,
    }

    for col, default in defaults.items():
        if col not in df.columns:
            df[col] = default

    # Numeric columns
    for col in ["sales", "quantity", "rating"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["sales"] = df["sales"].fillna(0)
    df["quantity"] = df["quantity"].fillna(0)

    return df


df = load_data()


# -----------------------------
# Helper functions
# -----------------------------
def money(value):
    return f"₹{value:,.2f}"


def rating_display(series):
    values = pd.to_numeric(series, errors="coerce").dropna()

    if values.empty:
        return "N/A"

    avg = values.mean()
    maximum = values.max()

    if maximum <= 5:
        return f"{avg:.2f}/5"
    return f"{avg:.2f}/10"


def chart_layout(fig, height=300):
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            color="#172033",
            size=12,
        ),
        margin=dict(l=50, r=25, t=55, b=55),
        showlegend=True,
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#e5e9f0",
        zeroline=False,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#e5e9f0",
        zeroline=False,
    )

    return fig


def kpi_card(label, value):
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(label, value):
    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-label">{label}</div>
            <div class="insight-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR - ONLY NAVIGATION
# ============================================================
with st.sidebar:
    st.markdown(
        '<div class="brand">🛒 Supermarket</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "📦 Products",
            "🏬 Branches",
            "💳 Payments",
            "👥 Customers",
            "⭐ Ratings",
        ],
        label_visibility="collapsed",
    )


# ============================================================
# DASHBOARD PAGE
# ============================================================
if page == "📊 Dashboard":

    st.markdown(
        '<div class="page-title">Supermarket Sales Dashboard</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Overview of sales, products, branches, customers and payments</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------
    # KPI calculations
    # -----------------------------
    total_sales = df["sales"].sum()
    transactions = len(df)
    total_quantity = df["quantity"].sum()
    avg_rating = rating_display(df["rating"])
    avg_transaction = total_sales / transactions if transactions else 0

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        kpi_card("Total Sales", money(total_sales))

    with c2:
        kpi_card("Transactions", f"{transactions:,}")

    with c3:
        kpi_card("Total Quantity", f"{total_quantity:,.0f}")

    with c4:
        kpi_card("Average Rating", avg_rating)

    with c5:
        kpi_card("Avg. Transaction", money(avg_transaction))

    # -----------------------------
    # Key insights
    # -----------------------------
    st.markdown(
        '<div class="section-title">Key Insights</div>',
        unsafe_allow_html=True,
    )

    category_sales = (
        df.groupby("category")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    branch_sales = (
        df.groupby("branch")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    payment_usage = df["payment"].value_counts()

    top_category = category_sales.index[0] if len(category_sales) else "N/A"
    top_branch = branch_sales.index[0] if len(branch_sales) else "N/A"
    top_payment = payment_usage.index[0] if len(payment_usage) else "N/A"

    i1, i2, i3 = st.columns(3)

    with i1:
        insight_card("🏆 Top Product Line", str(top_category))

    with i2:
        insight_card("🏬 Highest Sales Branch", str(top_branch))

    with i3:
        insight_card("💳 Most Used Payment", str(top_payment))

    # -----------------------------
    # Main charts
    # -----------------------------
    st.markdown(
        '<div class="section-title">Sales Analysis</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    # Sales by category
    with left:
        category_chart = (
            df.groupby("category", as_index=False)["sales"]
            .sum()
            .sort_values("sales", ascending=False)
        )

        fig = px.bar(
            category_chart,
            x="category",
            y="sales",
            title="Sales by Product Line",
            labels={
                "category": "Product Line",
                "sales": "Sales",
            },
        )

        fig.update_traces(
            marker_color="#8ecae6",
            marker_line_width=0,
        )

        fig = chart_layout(fig, 330)

        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False},
        )

    # Sales by branch
    with right:
        branch_chart = (
            df.groupby("branch", as_index=False)["sales"]
            .sum()
            .sort_values("sales", ascending=False)
        )

        fig = px.bar(
            branch_chart,
            x="branch",
            y="sales",
            title="Sales by Branch",
            labels={
                "branch": "Branch",
                "sales": "Sales",
            },
        )

        fig.update_traces(
            marker_color="#8ecae6",
            marker_line_width=0,
        )

        fig = chart_layout(fig, 330)

        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False},
        )

    # -----------------------------
    # Lower charts
    # -----------------------------
    a, b, c, d = st.columns(4)

    # Top 5 products
    with a:
        product_chart = (
            df.groupby("product", as_index=False)["sales"]
            .sum()
            .sort_values("sales", ascending=False)
            .head(5)
            .sort_values("sales")
        )

        fig = px.bar(
            product_chart,
            x="sales",
            y="product",
            orientation="h",
            title="Top 5 Products by Sales",
            labels={
                "product": "",
                "sales": "Sales",
            },
        )

        fig.update_traces(
            marker_color="#8ecae6",
            marker_line_width=0,
        )

        fig = chart_layout(fig, 285)
        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False},
        )

    # Payment donut
    with b:
        payment_chart = (
            df["payment"]
            .value_counts()
            .rename_axis("payment")
            .reset_index(name="transactions")
        )

        fig = px.pie(
            payment_chart,
            names="payment",
            values="transactions",
            title="Payment Method Usage",
            hole=0.55,
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent",
        )

        fig = chart_layout(fig, 285)
        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False},
        )

    # Customer donut
    with c:
        customer_chart = (
            df["customer_type"]
            .value_counts()
            .rename_axis("customer_type")
            .reset_index(name="transactions")
        )

        fig = px.pie(
            customer_chart,
            names="customer_type",
            values="transactions",
            title="Customer Type Distribution",
            hole=0.55,
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent",
        )

        fig = chart_layout(fig, 285)
        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False},
        )

    # Rating distribution
    with d:
        ratings = pd.to_numeric(
            df["rating"],
            errors="coerce",
        ).dropna()

        if len(ratings):
            rating_chart = (
                ratings
                .round(0)
                .value_counts()
                .sort_index()
                .rename_axis("rating")
                .reset_index(name="count")
            )

            fig = px.bar(
                rating_chart,
                x="rating",
                y="count",
                title="Ratings Distribution",
                labels={
                    "rating": "Rating",
                    "count": "Count",
                },
            )

            fig.update_traces(
                marker_color="#8ecae6",
                marker_line_width=0,
            )

            fig = chart_layout(fig, 285)

            st.plotly_chart(
                fig,
                width="stretch",
                config={"displayModeBar": False},
            )
        else:
            st.info("Rating data is not available.")


# ============================================================
# PRODUCTS PAGE
# ============================================================
elif page == "📦 Products":

    st.markdown(
        '<div class="page-title">Products</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Product sales and quantity analysis</div>',
        unsafe_allow_html=True,
    )

    product_summary = (
        df.groupby("product", as_index=False)
        .agg(
            Sales=("sales", "sum"),
            Quantity=("quantity", "sum"),
            Transactions=("product", "size"),
        )
        .sort_values("Sales", ascending=False)
    )

    st.dataframe(
        product_summary.rename(
            columns={
                "product": "Product",
                "Sales": "Sales",
                "Quantity": "Quantity",
                "Transactions": "Transactions",
            }
        ),
        width="stretch",
        hide_index=True,
    )


# ============================================================
# BRANCHES PAGE
# ============================================================
elif page == "🏬 Branches":

    st.markdown(
        '<div class="page-title">Branches</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Branch and city sales performance</div>',
        unsafe_allow_html=True,
    )

    branch_summary = (
        df.groupby(["branch", "city"], as_index=False)
        .agg(
            Sales=("sales", "sum"),
            Transactions=("branch", "size"),
            Quantity=("quantity", "sum"),
        )
        .sort_values("Sales", ascending=False)
    )

    fig = px.bar(
        branch_summary,
        x="branch",
        y="Sales",
        color="city",
        title="Branch Sales Comparison",
    )

    fig = chart_layout(fig, 420)
    st.plotly_chart(fig, width="stretch")

    st.dataframe(
        branch_summary,
        width="stretch",
        hide_index=True,
    )


# ============================================================
# PAYMENTS PAGE
# ============================================================
elif page == "💳 Payments":

    st.markdown(
        '<div class="page-title">Payments</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Payment method usage and sales</div>',
        unsafe_allow_html=True,
    )

    payment_summary = (
        df.groupby("payment", as_index=False)
        .agg(
            Transactions=("payment", "size"),
            Sales=("sales", "sum"),
            Average_Transaction=("sales", "mean"),
        )
        .sort_values("Transactions", ascending=False)
    )

    left, right = st.columns(2)

    with left:
        fig = px.bar(
            payment_summary,
            x="payment",
            y="Transactions",
            title="Payment Method Usage",
        )
        fig.update_traces(marker_color="#8ecae6")
        fig = chart_layout(fig, 400)
        st.plotly_chart(fig, width="stretch")

    with right:
        fig = px.pie(
            payment_summary,
            names="payment",
            values="Sales",
            title="Sales by Payment Method",
            hole=0.5,
        )
        fig = chart_layout(fig, 400)
        st.plotly_chart(fig, width="stretch")

    st.dataframe(payment_summary, width="stretch", hide_index=True)


# ============================================================
# CUSTOMERS PAGE
# ============================================================
elif page == "👥 Customers":

    st.markdown(
        '<div class="page-title">Customers</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Customer type and purchasing behavior</div>',
        unsafe_allow_html=True,
    )

    customer_summary = (
        df.groupby("customer_type", as_index=False)
        .agg(
            Transactions=("customer_type", "size"),
            Sales=("sales", "sum"),
            Average_Transaction=("sales", "mean"),
            Quantity=("quantity", "sum"),
        )
        .sort_values("Sales", ascending=False)
    )

    left, right = st.columns(2)

    with left:
        fig = px.bar(
            customer_summary,
            x="customer_type",
            y="Sales",
            title="Sales by Customer Type",
        )
        fig.update_traces(marker_color="#8ecae6")
        fig = chart_layout(fig, 400)
        st.plotly_chart(fig, width="stretch")

    with right:
        fig = px.pie(
            customer_summary,
            names="customer_type",
            values="Transactions",
            title="Customer Type Distribution",
            hole=0.5,
        )
        fig = chart_layout(fig, 400)
        st.plotly_chart(fig, width="stretch")

    st.dataframe(customer_summary, width="stretch", hide_index=True)


# ============================================================
# RATINGS PAGE
# ============================================================
elif page == "⭐ Ratings":

    st.markdown(
        '<div class="page-title">Ratings</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Customer rating analysis</div>',
        unsafe_allow_html=True,
    )

    ratings = pd.to_numeric(
        df["rating"],
        errors="coerce",
    ).dropna()

    if ratings.empty:
        st.warning("No rating data available.")
    else:
        avg = ratings.mean()
        maximum = ratings.max()
        minimum = ratings.min()
        scale = 5 if maximum <= 5 else 10

        c1, c2, c3 = st.columns(3)

        with c1:
            kpi_card("Average Rating", f"{avg:.2f}/{scale}")

        with c2:
            kpi_card("Highest Rating", f"{maximum:.0f}/{scale}")

        with c3:
            kpi_card("Lowest Rating", f"{minimum:.0f}/{scale}")

        rating_chart = (
            ratings.round(0)
            .value_counts()
            .sort_index()
            .rename_axis("rating")
            .reset_index(name="count")
        )

        fig = px.bar(
            rating_chart,
            x="rating",
            y="count",
            title="Ratings Distribution",
        )

        fig.update_traces(marker_color="#8ecae6")
        fig = chart_layout(fig, 420)

        st.plotly_chart(fig, width="stretch")


# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption(
    "Supermarket Sales Analysis • Python • Pandas • Plotly • Streamlit"
)
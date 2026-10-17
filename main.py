
import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Modiji Chai Sales | Before 2014",
    page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0y58XRiabfTpjd2GTS48UH7F0b19gWLOJwKdxLDXFVQ&s=10",
    layout="wide",
    initial_sidebar_state="expanded"
)



st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #FFF7ED;
    color: #431407;
}

/* Main content text */
[data-testid="stAppViewContainer"] .main p,
[data-testid="stAppViewContainer"] .main label,
[data-testid="stAppViewContainer"] .main span,
[data-testid="stAppViewContainer"] .main h1,
[data-testid="stAppViewContainer"] .main h2,
[data-testid="stAppViewContainer"] .main h3 {
    color: #431407;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #7C2D12;
}

[data-testid="stSidebar"] * {
    color: #FFF7ED;
}

/* KPI cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #FED7AA;
    border-radius: 12px;
    padding: 16px;
}

[data-testid="stMetric"] label,
[data-testid="stMetric"] [data-testid="stMetricValue"],
[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #7C2D12 !important;
}

/* Buttons */
.stButton > button {
    background-color: #EA580C;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
}

.stButton > button:hover {
    background-color: #C2410C;
    color: #FFFFFF;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #7C2D12 !important;
}

/* Dataframe borders */
[data-testid="stDataFrame"] {
    border: 1px solid #FED7AA;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_csv("modiji_chai_sales_satire_v2.csv")

    data.columns = data.columns.str.strip()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data["Revenue_INR"] = pd.to_numeric(
        data["Revenue_INR"], errors="coerce"
    ).fillna(0)
    data["Cups_Sold"] = pd.to_numeric(
        data["Cups_Sold"], errors="coerce"
    ).fillna(0)
    data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
    return data

st.title("Modiji Chai Sales")
st.subheader("Before 2014 — The Great Vishawguru")
st.subheader("ONLY TWO PAYMENT METHODS ACCEPTED   PM CARE FUNDS  &&  CHANDA CHORI FUND ")

st.markdown("""
<div style="
    background: linear-gradient(110deg, #7C2D12, #C2410C, #F97316);
    padding: 22px 26px;
    border-radius: 16px;
    color: white;
    margin: 18px 0 24px 0;
">
    <div style="font-size: 13px; opacity: 0.9;">
        CHAI FROM PM CARE FUNDS
    </div>
    <div style="font-size: 25px; font-weight: 800; margin: 8px 0;">
        MODIJI KI CHAI KE CHARCHE! 
    </div>
    <div style="font-size: 13px;">
        A political satire concept — names below are parody references,
        not verified funders, donors, or financial contributors.
    </div>
</div>
""", unsafe_allow_html=True)

funders = [
    ("Gautam Adani", "Wood producer for ignition"),
    ("Mukesh Ambani", "Real boss of chai tapri"),
    ("Amit Shah", "Milk producer"),
    ("Nitin Gadkari", "Ethanol dalo sugar nikalo"),
    ("Gyanesh Kumar", "Free leadership"),
]

cols = st.columns(5)

for col, (name, caption) in zip(cols, funders):
    with col:
        st.markdown(f"""
        <div style="
            background: #FFFFFF;
            border: 1px solid #FDBA74;
            border-top: 5px solid #EA580C;
            border-radius: 12px;
            padding: 16px 12px;
            min-height: 118px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(124,45,18,0.06);
        ">
            <div style="font-size: 15px; font-weight: 800; color: #7C2D12;">
                {name}
            </div>
            <div style="font-size: 12px; color: #9A3412; margin-top: 10px;">
                {caption}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.caption(
    "Satire only: no real funding, donations, or financial relationships are implied."
)

st.caption(
    "Political satire dashboard. All transactions, amounts and "
    "customer associations are synthetic, not historical records."
)

@st.cache_data
def load_data():
    return pd.read_csv("modiji_chai_sales.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("ERROR 404 ,FILE NOT FOUND.")
    st.stop()
try:
    df = load_data()
except FileNotFoundError:
    st.error("ERROR 404 ,FILE NOT FOUND.")
    st.stop()
except Exception as e:
    st.error(f"CSV Load krna pahle expired maggie ke fate hue wrapper: {e}")
    st.stop()

required = [
    "Year", "State", "City", "Customer_Name", "Customer_Category",
    "Chai_Type", "Cups_Sold", "Revenue_INR", "Payment_Method",
    "Order_ID", "Date"
]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"coloumn not founnd: {missing}")
    st.stop()


st.sidebar.title("Chai Control Room")
st.sidebar.caption("Choose filters to explore the fictional ledger.")

def options_for(column):
    return sorted(df[column].dropna().unique().tolist(), key=str)

year_options = ["All"] + options_for("Year")
state_options = ["All"] + options_for("State")
city_options = ["All"] + options_for("City")
customer_options = ["All"] + options_for("Customer_Name")
chai_options = ["All"] + options_for("Chai_Type")
payment_options = ["All"] + options_for("Payment_Method")
channel_options = (
    ["All"] + options_for("Order_Channel")
    if "Order_Channel" in df.columns else ["All"]
)

selected_year = st.sidebar.selectbox("Year", year_options)
selected_state = st.sidebar.selectbox("State", state_options)
selected_city = st.sidebar.selectbox("City", city_options)
selected_customer = st.sidebar.selectbox("Customer", customer_options)
selected_chai = st.sidebar.selectbox("Chai Type", chai_options)
selected_payment = st.sidebar.selectbox("Payment Method", payment_options)
selected_channel = st.sidebar.selectbox("Order Channel", channel_options)

search = st.sidebar.text_input("Search customer or Order ID")

if st.sidebar.button("Reset filters"):
    st.rerun()


filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]
if selected_state != "All":
    filtered_df = filtered_df[filtered_df["State"] == selected_state]
if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]
if selected_customer != "All":
    filtered_df = filtered_df[
        filtered_df["Customer_Name"] == selected_customer
    ]
if selected_chai != "All":
    filtered_df = filtered_df[filtered_df["Chai_Type"] == selected_chai]
if selected_payment != "All":
    filtered_df = filtered_df[
        filtered_df["Payment_Method"] == selected_payment
    ]
if selected_channel != "All" and "Order_Channel" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Order_Channel"] == selected_channel
    ]

if search.strip():
    term = search.strip()
    mask = (
        filtered_df["Customer_Name"].astype(str).str.contains(
            term, case=False, na=False
        )
        | filtered_df["Order_ID"].astype(str).str.contains(
            term, case=False, na=False
        )
    )
    filtered_df = filtered_df[mask]


total_revenue = filtered_df["Revenue_INR"].sum()
total_orders = filtered_df["Order_ID"].nunique()
total_cups = filtered_df["Cups_Sold"].sum()

top_city_series = filtered_df.groupby("City")["Revenue_INR"].sum()
top_city = (
    top_city_series.idxmax()
    if not top_city_series.empty else "N/A"
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("Total Orders", f"{total_orders:,}")
c3.metric("Cups Sold", f"{total_cups:,.0f}")
c4.metric("Top City", top_city)

st.caption(f"Showing {len(filtered_df):,} of {len(df):,} records.")

if filtered_df.empty:
    st.warning("No records match these filters. Change your selection.")
    st.stop()


overview, vip, payments, ledger, explorer = st.tabs([
    "Overview",
    "VIP Chai Board",
    "Payment Department",
    "Chai Ledger",
    "Data Explorer"
])

with overview:
    left, right = st.columns(2)

    with left:
        city_revenue = (
            filtered_df.groupby("City", as_index=False)["Revenue_INR"]
            .sum().sort_values("Revenue_INR", ascending=False)
        )
        fig = px.bar(
            city_revenue,
           x="City",
           y="Revenue_INR",
           title="City-wise Revenue",
           color="Revenue_INR",
           color_continuous_scale=["#FDBA74", "#C2410C"],
           template="plotly_white"
)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        yearly = (
            filtered_df.groupby("Year", as_index=False)["Revenue_INR"].sum()
        )
        fig = px.line(
            yearly, x="Year", y="Revenue_INR",
            markers=True, title="📈 Chai Revenue Over the Years",
            color_discrete_sequence=["#EA580C"]
        )
        st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        chai_sales = (
            filtered_df.groupby("Chai_Type", as_index=False)["Cups_Sold"].sum()
        )
        fig = px.pie(
            chai_sales, names="Chai_Type", values="Cups_Sold",
            title="Which Chai Rules the Kettle?",
            color_discrete_sequence=px.colors.sequential.Oranges
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Chai Counter")
        st.write("EK chai = Desh")
        st.write(f"**{len(filtered_df)}** fictional ledger entries match your filters.")
        st.write(f"**{filtered_df['Customer_Name'].nunique()}** customer names in this view.")
        st.info("These are synthetic records made for a satire project.")

with vip:
    st.subheader("VIP Kulhad League")
    st.caption("Satirical leaderboard — not verified customers or purchases.")

    leaderboard = (
        filtered_df.groupby("Customer_Name", as_index=False)
        .agg(
            Orders=("Order_ID", "nunique"),
            Cups=("Cups_Sold", "sum"),
            Revenue=("Revenue_INR", "sum")
        )
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    if not leaderboard.empty:
        leaderboard.insert(0, "Rank", range(1, len(leaderboard) + 1))
        st.dataframe(leaderboard, use_container_width=True, hide_index=True)

        fig = px.bar(
            leaderboard.sort_values("Revenue"),
            x="Revenue", y="Customer_Name", orientation="h",
            title="VIP Chai Ledger",
            color="Revenue",
            color_continuous_scale=["#FDBA74", "#C2410C"]
        )
        st.plotly_chart(fig, use_container_width=True)

with payments:
    st.subheader(" Payment Department")
    st.caption("Both labels are fictional parody categories, not actual transfers.")

    payment_summary = (
        filtered_df.groupby("Payment_Method", as_index=False)
        .agg(
            Transactions=("Order_ID", "nunique"),
            Revenue=("Revenue_INR", "sum")
        )
    )
    payment_summary["Share (%)"] = (
        payment_summary["Transactions"]
        / payment_summary["Transactions"].sum() * 100
    ).round(1)

    left, right = st.columns(2)
    with left:
        fig = px.pie(
            payment_summary, names="Payment_Method", values="Transactions",
            title="Transaction Category Split",
            color_discrete_sequence=["#EA580C", "#FDBA74"]
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.bar(
            payment_summary, x="Payment_Method", y="Revenue",
            title="Revenue by Satirical Category",
            color="Payment_Method",
            color_discrete_sequence=["#C2410C", "#FB923C"]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(payment_summary, use_container_width=True, hide_index=True)

with ledger:
    st.subheader("The Chai Ledger")
    st.caption("Search and inspect every matching synthetic transaction.")

    page_size = st.selectbox("Rows per page", [10, 25, 50, 100], index=1)
    total_pages = max(1, (len(filtered_df) + page_size - 1) // page_size)
    page = st.number_input(
        "Page", min_value=1, max_value=total_pages, value=1, step=1
    )
    start = (page - 1) * page_size
    page_df = filtered_df.iloc[start:start + page_size]

    st.dataframe(page_df, use_container_width=True, hide_index=True)
    st.caption(f"Page {page} of {total_pages}")

    st.download_button(
        "⬇Download filtered CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_chai_sales_satire.csv",
        mime="text/csv"
    )

with explorer:
    st.subheader("Data Explorer")
    st.write("Inspect columns, types and missing values.")

    selected_columns = st.multiselect(
        "Choose columns to display",
        options=filtered_df.columns.tolist(),
        default=filtered_df.columns.tolist()
    )

    if selected_columns:
        st.dataframe(
            filtered_df[selected_columns],
            use_container_width=True,
            hide_index=True
        )

    quality = pd.DataFrame({
        "Column": filtered_df.columns,
        "Data Type": [str(filtered_df[c].dtype) for c in filtered_df.columns],
        "Missing Values": [int(filtered_df[c].isna().sum()) for c in filtered_df.columns],
        "Unique Values": [int(filtered_df[c].nunique()) for c in filtered_df.columns]
    })

    with st.expander("View data quality report"):
        st.dataframe(quality, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇Download full original dataset",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="modiji_chai_sales.csv",
        mime="text/csv"
    )


st.divider()
st.caption(
     "YEH SAB SIRF FUN KE LIYE KIYA GYA HE"
     "KUCH FALTU BOL KE APNI MURKHATA KA PRAMANN NAH DE"
     "DHANYWAD"
    
)

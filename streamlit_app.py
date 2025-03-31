import streamlit as st
import pandas as pd
st.title("DSBA 5122 Data App Assignment - David Bayha")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")
st.bar_chart(df, x="Category", y="Sales")


# Load data
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Reset index for easier filtering
df_reset = df.reset_index()

st.write("### (Addition #1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
selected_category = st.selectbox(
    "Select a Category:",
    options=df_reset['Category'].unique()
)

st.write("### (Addition #2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
available_subcategories = df_reset[df_reset['Category'] == selected_category]['Sub_Category'].unique()
selected_subcategories = st.multiselect(
    "Select Sub-Categories:",
    options=available_subcategories,
    default=available_subcategories[:min(3, len(available_subcategories))]
)

# Filter data based on selections
if selected_subcategories:
    filtered_df = df_reset[
        (df_reset['Category'] == selected_category) & 
        (df_reset['Sub_Category'].isin(selected_subcategories))
    ]
else:
    filtered_df = pd.DataFrame()

st.write("### (Addition #3) show a line chart of sales for the selected items in (2)")
if not filtered_df.empty:
    sales_by_date_subcat = filtered_df.groupby(['Order_Date', 'Sub_Category'])['Sales'].sum().unstack()
    st.write("### Sales Over Time for Selected Sub-Categories")
    st.line_chart(sales_by_date_subcat)
else:
    st.write("Please select at least one sub-category to see the chart.")

# Overall average profit margin
overall_total_sales = df_reset['Sales'].sum()
overall_total_profit = df_reset['Profit'].sum()
overall_avg_margin = (overall_total_profit / overall_total_sales) * 100 if overall_total_sales != 0 else 0

st.write("### (Addition #4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")

if not filtered_df.empty:
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", f"${total_sales:,.2f}")
    with col2:
        st.metric("Total Profit", f"${total_profit:,.2f}")
    with col3:
        st.metric("Profit Margin (%)", f"{profit_margin:.2f}%")
else:
    st.write("Please select at least one sub-category to see the metrics.")

st.write("### (Addition #5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")

if not filtered_df.empty:
    # Recalculate metrics (same as above, but we'll show them again with delta)
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0
    
    # Calculate delta for requirement 5
    margin_delta = profit_margin - overall_avg_margin
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", f"${total_sales:,.2f}")
    with col2:
        st.metric("Total Profit", f"${total_profit:,.2f}")
    with col3:
        st.metric(
            "Profit Margin (%)", 
            f"{profit_margin:.2f}%", 
            delta=f"{margin_delta:.2f}%",
            help=f"Compared to overall average: {overall_avg_margin:.2f}%"
        )
    

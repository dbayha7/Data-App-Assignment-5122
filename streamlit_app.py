import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on March 17th")

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

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
### (1) Add a dropdown for Category
st.write("## Select a Category")
category_list = df['Category'].unique()
selected_category = st.selectbox("Select a Category", category_list)

st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
### (2) Add a multi-select for Sub_Category within the selected Category
st.write("## Select Sub-Category in the Selected Category")
sub_category_list = df[df['Category'] == selected_category]['Sub_Category'].unique()
selected_sub_categories = st.multiselect("Select Sub-Category", sub_category_list)

st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")

# Filter data based on Category and Sub-Category
filtered_data = df[(df['Category'] == selected_category) & (df['Sub_Category'].isin(selected_sub_categories))]

# Check if data is available
if not filtered_data.empty:
    ### (3) Show a line chart of sales for the selected items
    st.write("## Sales Trend for Selected Sub-Categories")
    sales_chart_data = filtered_data.resample('M').sum(numeric_only=True)['Sales'].reset_index()
    st.line_chart(sales_chart_data, x='Order_Date', y='Sales', use_container_width=True)

    ### (4) Show three metrics for selected items
    total_sales = filtered_data['Sales'].sum()
    total_profit = filtered_data['Profit'].sum()
    overall_profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    # Overall average profit margin for all products across all categories
    avg_profit_margin_all = (df['Profit'].sum() / df['Sales'].sum()) * 100 if df['Sales'].sum() != 0 else 0

    # Delta for overall profit margin
    profit_margin_delta = overall_profit_margin - avg_profit_margin_all

    st.write("## Key Metrics for Selected Sub-Categories")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Profit Margin (%)", f"{overall_profit_margin:.2f}%", delta=f"{profit_margin_delta:.2f}%")

    ### (5) Delta in Profit Margin Metric
    st.write("### Profit Margin Difference")
    st.write(f"The selected Sub-Categories have a profit margin difference of **{profit_margin_delta:.2f}%** compared to the overall average of **{avg_profit_margin_all:.2f}%**.")
else:
    st.write("No data available for the selected filters. Please select a valid combination.")

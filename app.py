# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


# Set the page config
st.set_page_config(page_title='Minecraft Economy Dashboard',
                   page_icon=':pick:',
                   layout='wide',
                   initial_sidebar_state='expanded')

# Set the title of the app and add a separator
st.title('Minecraft World Economy Dashboard')
st.markdown("---")

# Load the data
@st.cache_data
def load_data():
    transactions_data = pd.read_csv('transactions.csv')
    transactions_data['timestamp'] = pd.to_datetime(transactions_data['timestamp'])
    return transactions_data

transactions_data = load_data()

# Display the first few rows of the data
st.subheader('Data Overview')
st.dataframe(transactions_data.head())

# Overview Statistics
st.subheader('Overview Statistics')
st.divider()
total_transactions = transactions_data.shape[0]
total_items_bought = transactions_data['quantity'].sum()
total_amount_spent = transactions_data['price'].sum()
col1, col2, col3 = st.columns(3)
with col1:
    st.header('Total Transactions')
    st.subheader(total_transactions)
with col2:
    st.header('Total Items Bought')
    st.subheader(total_items_bought)
with col3:
    st.header('Total Amount Spent')
    st.subheader(total_amount_spent)

st.divider()

# User Statistics
st.subheader('User Statistics')
user_stats = transactions_data.groupby('username').agg({'action': 'count', 'quantity': 'sum', 'price': 'sum'}).rename(columns={'action': 'Transactions', 'quantity': 'Items Bought', 'price': 'Amount Spent'})
st.dataframe(user_stats)

# Item Statistics
st.divider()
st.subheader('Item Statistics')
item_stats = transactions_data.groupby('item_name').agg({'action': 'count', 'quantity': 'sum', 'price': 'sum'}).rename(columns={'action': 'Transactions', 'quantity': 'Items Sold', 'price': 'Amount Earned'})
st.dataframe(item_stats)

# Time Series Analysis
st.divider()
st.subheader('Time Series Analysis')
transactions_data['Month'] = transactions_data['timestamp'].dt.to_period('M').dt.to_timestamp()
time_series = transactions_data.groupby('Month').agg({'action': 'count', 'quantity': 'sum', 'price': 'sum'})
fig1 = px.line(time_series, x=time_series.index, y='action', title='Number of Transactions Over Time', template='plotly_dark')
fig2 = px.line(time_series, x=time_series.index, y='quantity', title='Quantity of Items Bought Over Time', template='plotly_dark')
fig3 = px.line(time_series, x=time_series.index, y='price', title='Amount Spent Over Time', template='plotly_dark')
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(fig1)
with col2:
    st.plotly_chart(fig2)
with col3:
    st.plotly_chart(fig3)

# Geographical Analysis
st.divider()
st.subheader('Geographical Analysis')
fig4 = px.scatter_3d(transactions_data, x='x', y='y', z='z', color='username', title='Geographical Distribution of Transactions', template='plotly_dark')
st.plotly_chart(fig4)

# Region Analysis
st.divider()
st.subheader('Region Analysis')
regions = {
    'Government Mall': {'min_point': {'x': 324, 'y': -62, 'z': 762}, 'max_point': {'x': 403, 'y': 319, 'z': 926}},
    # Add more regions as needed
}

for region_name, region_coords in regions.items():
    region_transactions = transactions_data[
        (transactions_data['x'] >= region_coords['min_point']['x']) & (transactions_data['x'] <= region_coords['max_point']['x']) &
        (transactions_data['y'] >= region_coords['min_point']['y']) & (transactions_data['y'] <= region_coords['max_point']['y']) &
        (transactions_data['z'] >= region_coords['min_point']['z']) & (transactions_data['z'] <= region_coords['max_point']['z'])
    ]
    region_transactions_percentage = (region_transactions.shape[0] / total_transactions) * 100
    region_profit_percentage = (region_transactions['price'].sum() / transactions_data['price'].sum()) * 100
    st.write(f'**{region_name}**')
    st.write(f'Number of transactions: {region_transactions.shape[0]}')
    st.write(f'Total items bought: {region_transactions["quantity"].sum()}')
    st.write(f'Total amount spent: {region_transactions["price"].sum()}')
    st.write(f'Most popular items: {region_transactions["item_name"].value_counts().head(5).to_dict()}')
    st.write(f'Percentage of total transactions: {region_transactions_percentage:.2f}%')
    st.write(f'Percentage of total profit: {region_profit_percentage:.2f}%')

# Define the size of the cuboids
cuboid_size = 50

# Create a grid of cuboids
x_bins = np.arange(transactions_data['x'].min(), transactions_data['x'].max(), cuboid_size)
y_bins = np.arange(transactions_data['y'].min(), transactions_data['y'].max(), cuboid_size)
z_bins = np.arange(transactions_data['z'].min(), transactions_data['z'].max(), cuboid_size)

# Assign each transaction to a cuboid
transactions_data['x_bin'] = pd.cut(transactions_data['x'], bins=x_bins)
transactions_data['y_bin'] = pd.cut(transactions_data['y'], bins=y_bins)
transactions_data['z_bin'] = pd.cut(transactions_data['z'], bins=z_bins)

# Count the number of transactions in each cuboid
cuboid_counts = transactions_data.groupby(['x_bin', 'y_bin', 'z_bin']).size()

# Find the cuboids with the most transactions
hot_cuboids = cuboid_counts.sort_values(ascending=False).head(10)

st.divider()
st.subheader('Other Hot Regions')
st.write(hot_cuboids)


# Player Ranking
st.divider()
st.subheader('Player Ranking')
buyer_scores = transactions_data.groupby('username').agg({'price': 'sum', 'action': 'count'}).sum(axis=1)
seller_scores = transactions_data.groupby('seller').agg({'price': 'sum', 'action': 'count'}).sum(axis=1)
scores = buyer_scores.add(seller_scores, fill_value=0).sort_values(ascending=False)
ranking = pd.DataFrame(scores, columns=['score'])
st.dataframe(ranking)

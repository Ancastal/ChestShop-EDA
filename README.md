# Minecraft Economy Dashboard

## Description

The Minecraft Economy Dashboard is a dashboard to automatically conduct and visualize an exploratory data analysis designed of Minecraft ChestShop transactions. Utilizing Streamlit for a dynamic web interface, this dashboard provides a detailed overview of economic activities within the Minecraft world.

This tool is an adaptation of the ChestShop Analyzer I have shared in a previous repository. The transactions.csv file can be obtained on your server's data using the logs-parser, available in the above-mentioned repository

## Features

- **Interactive Web Dashboard**: Built with Streamlit, offering a user-friendly and interactive experience.
- **Comprehensive Data Overview**: Displays key statistics about Minecraft transactions, including total transactions, items bought, and total amount spent.
- **Detailed User and Item Statistics**: Analyzes user-specific activities and item-specific sales trends.
- **Time Series Analysis**: Visualizes transaction data over time to uncover temporal trends.
- **Geographical and Region Analysis**: Provides insights into the geographical distribution of transactions and detailed analysis of specific regions.
- **Hot Regions Identification**: Identifies and highlights the most active transaction areas within the game.
- **Player Ranking System**: Ranks players based on their economic activities, such as total money spent and number of transactions.
- **Search Functionality**: Allows users to search for transactions based on usernames.

## Installation

1. Clone the repository.
2. Navigate to the main directory
3. Install the necessary dependancies
  ```git clone https://github.com/Ancastal/ChestShop-EDA
  cd ChestShop-EDA
  pip install -r requirements.txt
  ```
5. Run the dashboard with:
  ```bash
  streamlit run app.py
  ```

## License
This project is licensed under MIT. See LICENSE.md for more details.

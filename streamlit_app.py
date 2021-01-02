import streamlit as st
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px
import plotly.io as pio
import datetime

import pandas_datareader as pdr

# # List of symbols to grab
# symbols = ['FB', 'AAPL', 'GOOGL', 'AMZN', 'MSFT']
# data = {}
# for stock in symbols:
#     data[stock] = pdr.DataReader(stock, 'yahoo', '2012', '2021')['Adj Close']
# df = pd.DataFrame(data).reset_index().fillna(0)


def get_data(start_date='2012-02-01',end_date='2021', symbols=['FB','AAPL','GOOGL','AMZN','MSFT']):

    """Gets Stock Data from Pandas Data Reader Using Yahoo Finance.

    Args:
        start_date (str, optional): [description]. Defaults to '2012-02-01'.
        end_date (str, optional): [description]. Defaults to '2021'.
        symbols (list, optional): [description]. Defaults to ['FB','AAPL','GOOGL','AMZN','MSFT'].

    Returns:
        [type]: [description]
    """
    data = {}
    for stock in symbols:
        try:
            data[stock] = pdr.DataReader(stock, 'yahoo', start_date, end_date)['Adj Close']
        except Exception as e:
            print('Error with stock: '+stock)
    df = pd.DataFrame(data).reset_index()
    return df


def plot_stocks_df(df=None, stocks=['FB', 'AAPL']):
    stocks_exist = [s for s in stocks if s in df.columns]
    pfig = px.scatter(df, x='Date', y=stocks_exist,template='plotly_dark')
    return pfig



st.title('Example Streamlit App')


## Get Dates and Symbols to plot
start_date = st.date_input('Start Date', pd.to_datetime('2012-01-01'))
end_date = st.date_input('End Date', datetime.date.today())

stocks = st.text_input('Stock Symbols (separate with a ,)','AMZN,MSFT,FB')

df = get_data(start_date=start_date,end_date=end_date)
fig = plot_stocks_df(df, stocks=stocks.split(','))


# if start_date < end_date:
#     st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
# else:
#     st.error('Error: End date must fall after start date.')


st.plotly_chart(fig)
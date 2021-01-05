import datetime as dt
from datetime import date
import pandas_datareader as pdr

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State

import numpy as np
np.random.seed(321)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['figure.figsize'] = (12,4)

import plotly.express as px
import plotly.io as pio
pio.templates


today = dt.date.today().strftime("%Y-%m-%d")
def get_data(start_date='2012-02-01',end_date=today,symbols = ['FB','AAPL','GOOGL','AMZN','MSFT']):
    
    data = {}
    for stock in symbols:
        try:
            data[stock] = pdr.DataReader(stock,'yahoo',start_date,end_date)['Adj Close']
        except:
            print('Error with stock: '+stock)
    df = pd.DataFrame(data).reset_index()
    return df


def plot_stocks_df(df=None,stocks=['FB','AAPL']):
    if df is None:
        df = get_data(stocks)#.reset_index()
    stocks_exist = [s for s in stocks if s in df.columns]
    pfig = px.scatter(df,x='Date',y=stocks_exist)
    return pfig

from jupyter_plotly_dash import JupyterDash
app = dash.Dash(__name__)
defaults = ['MSFT','AMZN']
# df = get_data(date(2012, 1, 1))

app.layout = html.Div(children = [
    html.H1('Our AMAZING Dashboard'),
    
    html.Div(children=[
        html.Div(style={"border":'1px solid black','padding':'3px'},id='menu',children=[
            html.H3('Enter stock symbols, separated by a comma.\nPress Enter to update.'),

            dcc.Input(id='choose_stocks',value='MSFT,AMZN',
                      placeholder='MSFT,AAPL',#,
                         style={'width': '90%', 'height': 50}),           

            dcc.DatePickerRange( id='my-date-picker-range',
                                start_date=date(2012,1,1),
                                min_date_allowed=date(2010, 1, 1),
                                max_date_allowed=today,#date.today(),#date(2021),
                                end_date=today,style={'width':'50%'}),#date.today()), #date(2017, 8, 25)),
            html.Button('Submit',id='submit',style={'size':'40 px'})
    
        ]),
        
        dcc.Graph(id='line_plot')

    ])
])

@app.callback(Output('line_plot','figure'),
              [Input('submit','n_clicks')],
              [State('choose_stocks','value'),
               State('my-date-picker-range', 'start_date'),
               State('my-date-picker-range', 'end_date')])
def update_stocks(n_clicks, stocks,start_date,end_date):
    stocks = stocks.split(',')
    plot_df = get_data(start_date,end_date,symbols=stocks)
    return plot_stocks_df(df=plot_df,stocks=stocks)#,start_date,end_date)
    

if __name__=='__main__':
    app.run_server(debug=True)
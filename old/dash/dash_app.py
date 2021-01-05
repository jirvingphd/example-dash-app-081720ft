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
pio.templates.default = "seaborn"


import datetime as dt
import pandas_datareader as pdr

## List of symbols to grab
today = dt.date.today().strftime("%Y-%m-%d")
def get_data(start_date='2012-02-01',end_date=today,#'2021',
symbols = ['FB','AAPL','GOOGL','AMZN','MSFT']):
    """Uses pandas data reader to grab daily stock day for the symbols specifier from start_date to end_date

    Args:
        start_date (str, optional): Start Date to rerieve. Defaults to '2012-02-01'.
        end_date (str, optional): End Date to Retrive. Defaults to '2021'.
        symbols (list, optional): [description]. Defaults to ['FB','AAPL','GOOGL','AMZN','MSFT'].

    Returns:
        [type]: [description]
    """
    
    data = {}
    for stock in symbols:
        try:
            data[stock] = pdr.DataReader(stock,'yahoo',start_date,end_date)['Adj Close']
        except:
            print('Error with stock: '+stock)
    df = pd.DataFrame(data).reset_index()
    return df


def plot_stocks_df(df=None,stocks=['FB','AAPL']):
    """Plots an line plot of the specified stock columns

    Args:
        df ([type], optional): [description]. Defaults to None.
        stocks (list, optional): [description]. Defaults to ['FB','AAPL'].

    Returns:
        [type]: [description]
    """
    if df is None:
        df = get_data(stocks)#.reset_index()
    stocks_exist = [s for s in stocks if s in df.columns]
    pfig = px.scatter(df,x='Date',y=stocks_exist)
    return pfig


def make_options(menu_choices,ignore_cols=['Date']):
    """Returns list of dictionary with {'label':menu_choice,'value':menu_choice}"""
    options = []
    for choice in menu_choices:
        if choice not in ignore_cols:
            options.append({'label':choice,'value':choice})
    return options



## Default stocks
defaults = ['MSFT','AMZN']
df = get_data(symbols=defaults)

## DASH APP
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children = [
    html.H1('Our AMAZING Dashboard'),
    html.H2("Lets see if we can make something interesting..."),
    
    html.Div(children=[
        
        html.Div(id='menu',children=[
            
            
            dcc.Dropdown(id='choose_stocks',placeholder=defaults,multi=True,
                         options=make_options(df.columns)),
            dcc.DatePickerRange( id='my-date-picker-range',
                                min_date_allowed=dt.date(2012, 1, 1),
                                max_date_allowed=today,#dt.date.today(),#date(2021),
                                initial_visible_month=dt.date(2012, 1, 1),
                                end_date=today),#dt.date.today()), #date(2017, 8, 25)),
            html.Button(id='submit',)
    
        ]),
        
    
        dcc.Graph(id='line_plot',figure=plot_stocks_df(stocks=defaults))

    ])
])


@app.callback(Output('line_plot','figure'),
              [Input('choose_stocks','value'),
               Input('my-date-picker-range', 'start_date'),
               Input('my-date-picker-range', 'end_date')])
def update_stocks(stocks,start_date,end_date):
    plot_df = get_data(start_date,end_date,stocks)
    return plot_stocks_df(df=plot_df,stocks=stocks)#,start_date,end_date)
    

if __name__ == '__main__':
    app.run_server(debug=True)
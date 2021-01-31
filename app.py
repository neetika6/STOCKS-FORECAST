import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import yfinance as yf
import pandas as pd
import plotly.express as px
import yfinance as yf
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import model as m
def get_stock_price_fig(df):
      fig = px.line(df,x="Date",y=["Open","Close"],title="Closing and Openning Price vs Date")
      return fig
def get_more(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,x="Date",y= "EWA_20",title="Exponential Moving Average vs Date")

    fig.update_traces(mode="lines+markers")
    return fig
def fore(df, days):
      fig = px.scatter(df,title=("Predicted Close price of next {} days(forecast is {}% accurate)".format(days,m.model1.svm_confidence)))
      fig.update_traces(mode="lines+markers")
      return fig
app=dash.Dash(__name__)
server=app.server
app.layout=html.Div([
    html.Div([
            html.P("Welcome to the Stock Dash App!", className="start"),
            html.Div([
              html.P("Choose a Ticker to Start", className="code"),
              dcc.Dropdown(id="submit" ,options=[
              {"label":"Adobe", "value":"ADBE"},
              {"label":"Amazon", "value":"AMZN"},
              {"label":"AngioDynamics", "value":"ANGO"},
              {"label":"Agora", "value":"API"},
              {"label":"Apple", "value":"AAPL"},
              {"label":"Cisco", "value":"CSCO"},
              {"label":"Facebook", "value":"FB"},
              {"label":"Google", "value":"GOOGL"},
              {"label":"IBM", "value":"IBM"},
              {"label":"Microsoft", "value":"MSFT"},
              {"label":"Neogen", "value":"NEOG"},
              {"label":"Netflix", "value":"NFLX"},
              {"label":"Oracle", "value":"ORCL"},
              {"label":"PayPal", "value":"PYPL"},
              {"label":"Tesla", "value":"TSLA"},
              {"label":"Texas", "value":"TXN"},
              {"label":"Yelp", "value":"YELP"}]),
              html.Button('Submit', id='submit-val', n_clicks=0),
            ]),
            html.Div([
              dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt(1995, 8, 5),
        max_date_allowed=dt(2025, 9, 19),
        initial_visible_month=dt(2021, 1, 25),
        end_date=dt(2021, 1, 31)
    ),
            ]),
            html.Div([
              html.Div([
                  html.Button('Stock Price',id='stock-price', n_clicks=0),
                  html.Button('Indicators',id='indicators',n_clicks=0),
                  dcc.Input(id='no-of-days', type='text',placeholder='number of days'),
                  html.Button('Forecast',id='forecast')
            ]),])
          ],
        className="inputs"),
    html.Div([
            html.Div(
                  [  html.P(id="ticker"),
                      html.Img(id="logo")
                    # Company Name
                  ],
                className="header",),
            html.Div( #Description
              id="description", className="decription_ticker"),
            html.Div([
                # Stock price plot
            ], id="graphs-content"),
            html.Div([
                # Indicator plot
            ], id="main-content"),
            html.Div([
                # Forecast plot
            ], id="forecast-content")
          ],
        className="content") ],className="container")

@app.callback(
  [Output("description", "children"), Output("logo", "src"), Output("ticker", "children")],
  [Input("submit-val","n_clicks")],
  [State("submit","value")]
            )
def update_data(n_clicks,v):
      if v == None:
            raise PreventUpdate
      
      ticker = yf.Ticker(v)
      inf = ticker.info

      df = pd.DataFrame.from_dict(inf, orient="index").T
      df = df[["logo_url", "longBusinessSummary", "shortName"]]

      return  df["longBusinessSummary"].values[0], df["logo_url"].values[0], df["shortName"].values[0]

@app.callback(
  [Output('graphs-content', 'children')],
  [Input("stock-price","n_clicks")],
  [State('my-date-picker-range', 'start_date'),State('my-date-picker-range', 'end_date'),State("submit","value")])

def stock_prices(n_clicks,start_date, end_date,v):
      if v== None:
          raise PreventUpdate
      ticker = yf.Ticker(v)
      df = yf.download(v,start_date,end_date)
      df.reset_index(inplace=True)

      fig = get_stock_price_fig(df)
      

      return [dcc.Graph(figure=fig)]
@app.callback(
  [Output('main-content', 'children')],
  [Input("indicators","n_clicks")],
  [State('my-date-picker-range', 'start_date'),
  State('my-date-picker-range', 'end_date'),
  State("submit","value")])

def indicators(n_clicks,start_date, end_date,v):
      if v== None:
          raise PreventUpdate
      ticker = yf.Ticker(v)
      df = yf.download(v,start_date,end_date)
      df.reset_index(inplace=True)

      fig = get_more(df)
      return [dcc.Graph(figure=fig)]

@app.callback(
  [Output('forecast-content', 'children')],
  [Input("forecast","n_clicks")],
  [State('no-of-days', 'value'),State("submit","value")])

def forecasts(n_clicks,days,v):
      if v== None:
            raise PreventUpdate
      if days==None:
            raise PreventUpdate
      df = m.model1(v,days)
      fig = fore(df,days)
      return [dcc.Graph(figure=fig)]

if __name__ == '__main__':
    app.run_server(debug=True)

#importing plotly for graphing stocks
import plotly.express as px

#importing pandas to make csv a dataframe so i can work with it in python
import pandas as pd

#import numpy to access polyfit function which fits data into polynomial of n degree
import numpy as np

#import matplotlib.pyplot to plot all the data as scaatter and line and seeing the trend
import matplotlib.pyplot as plt

stocks_dataframe = pd.read_csv('stock_open_prices.csv', parse_dates=True)

#normalize our stock prices method
# df is dataframe, aspect of pandas
def normalize(df):
    x = df.copy()
    for i in x.columns[1:]:
        x[i] = x[i] / x[i][0]
    return x

def interactive_plot(df,title):
    fig = px.line(title = title)
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'], y = df[i], name = i)
    fig.show()

#interactive_plot(normalize(stocks_dataframe), 'Normalized Prices')

#Now we have to get daily returns of each stock
# Need to iterate through each stock and get the change from the day before
def daily_return(df):
    df_daily_return = df.copy()
    for i in df.columns[1:]:
        #iterating through each column (stock) and getting the percentage change
        for j in range(1, len(df)):
            df_daily_return[i][j] = ((df[i][j] - df[i][j-1]) / df[i][j-1]) * 100
        df_daily_return[i][0] = 0
    return df_daily_return

stocks_daily_return = daily_return(stocks_dataframe)
print(stocks_daily_return)

beta = {}
alpha = {}

#assigning the beta of each stock in the portfolio
for i in stocks_daily_return.columns:
    if (i!= 'Date' and i!='^GSPC'):
        stocks_daily_return.plot(kind="scatter", x='^GSPC', y=i)
        b,a = np.polyfit(stocks_daily_return['^GSPC'], stocks_daily_return[i], 1)
        plt.plot(stocks_daily_return['^GSPC'], b * stocks_daily_return['^GSPC'] + a, '-', color = 'r')
        beta[i] = b
        alpha[i] = a
    plt.show()

#get all stocks from the stock portfolio
keys = list(beta.keys())

#dictionary of all expected returns
ER= {}

#assuming the risk free return rate is 0%
rf = 0

#average daily return of the market determined from the S&P500
av_daily_return = stocks_daily_return['^GSPC'].mean()

#Annualize the return by multiply average return per day * number of days in a trading year (252)
rm = stocks_daily_return['^GSPC'].mean() * 252

#calculating expected return of each stock
for i in keys:
    ER[i] = rf + beta[i] * (rm-rf)

print(ER)

#assigning weight to each portfolio stock to calculate sum of expected returns

#returns array of 1/8
portfolio_weights = 1/7 * np.ones(7)

#multiplying weights of each stock by their expected returns and adding it
ER_portfolio = sum(list(ER.values()) * portfolio_weights)

print("Expected return of portfolio is ", ER_portfolio )

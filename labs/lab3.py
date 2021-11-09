import pandas as pd
import numpy as np
import yfinance as yf
from itertools import combinations

"""
You will see the stocks that form the Dow Jones Industrial Average. Your job is to create a data frame of size (30 choose 2) = 435 rows. 
That is, you will have a row for every combination of two stocks. The third column will be the correlation between the price of the two stocks in 2019. 
Specifically, you will use yfinance to read the data about the stock prices. Finally, compute the correlation of the price between each pair of socks 
and store the result in the data frame. You are free to use for loops, while loops, and so on. The resulting data frame should be sorted by the 
correlation value in descending order, that is, the first row should contain the two stocks with the highest correlation.
"""

stocks = ['MMM','AXP','AAPL','BA', 'CAT', 'CVX','CSCO', 'KO','DIS','XOM','GS','HD',
'IBM','INTC', 'JNJ','JPM','MCD','MRK','MSFT','NKE','PFE','PG','TRV','UNH','VZ','V','WMT','WBA', 'TSLA', 'GOOG']


# get a list of all the combinations of stocks
stockCombinations = list(combinations(stocks, 2))

# put that list into a dataframe which will be the output
# fill values with placeholders
correlations = [0.0] * 435
stockCombinationsSeries = pd.Series(correlations, index = pd.MultiIndex.from_tuples(stockCombinations))


# stockCombinationsSeries['AAPL','BA'] = 10
# print(stockCombinationsSeries)
# print(stockCombinationsSeries['AAPL','BA'])

# download all the data for each stock
# store in a dictionary with stock symbols as keys
stockDataFrames = {}
for stock in stocks:
    stockDF = yf.Ticker(stock).history(start="2019-01-01", end="2019-12-31")
    stockDataFrames[stock] = stockDF

# calculate the correlation of each stock closing price
# fill in corresponding place in stockCombinationsDF with resulting value
for combination in stockCombinations:
    corr = stockDataFrames[combination[0]]['Close'].corr(stockDataFrames[combination[1]]['Close'])
    stockCombinationsSeries[combination[0], combination[1]] = corr

print(stockCombinationsSeries.sort_values(ascending=False))




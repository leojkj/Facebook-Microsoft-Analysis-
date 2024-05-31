import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

ms = pd.read_csv("D:\downloads\microsoft.csv")

fb = pd.read_csv(r"D:\downloads\facebook.csv")

print(fb.shape)
print(ms.shape)

print(fb.head)
print(ms.head)

print(fb.describe())
print(ms.describe())

print(fb.info)
print(ms.info)

print(fb.dtypes)
print(ms.dtypes)

# Assuming 'Date' column is not the index
fb['Date'] = pd.to_datetime(fb['Date'])  # Convert 'Date' column to datetime
fb.set_index('Date', inplace=True)  # Set 'Date' column as index

# Selecting rows from 2015-01-01 to 2015-12-31
fb_2015 = fb.loc['2015-01-01':'2015-12-31']

# Now, you can use .loc to access rows by date
print(fb_2015.loc['2015-03-16'])

ms['Date'] = pd.to_datetime(ms['Date'])  # Convert 'Date' column to datetime
ms.set_index('Date', inplace=True)  # Set 'Date' column as index

# Selecting rows from 2015-01-01 to 2015-12-31
ms_2015 = ms.loc['2015-01-01':'2015-12-31']

# Now, you can use .loc to access rows by date
print(ms_2015.loc['2015-03-16'])

fb.loc['2015-01-01':'2015-12-31', 'Close'].plot(label='2015') #2015
fb.loc['2016-01-01':'2016-12-31', 'Close'].plot(label='2016') #2016
fb.loc['2017-01-01':'2017-12-31', 'Close'].plot(label='2017') #2017
plt.legend()

ms.loc['2015-01-01':'2015-12-31', 'Close'].plot(label='2015') #2015
ms.loc['2016-01-01':'2016-12-31', 'Close'].plot(label='2016') #2016
ms.loc['2017-01-01':'2017-12-31', 'Close'].plot(label='2017') #2017
plt.legend()

#Shifting collomn one row upwards to do
#To compare the price difference between 
fb['Price1'] = fb['Close'].shift(-1)

#Price diff = Future Close Price - Present Close Price
fb['PriceDiff'] = fb['Price1'] - fb['Close']
fb.head()

#Daily return = Price Difference/Present Close Price 
fb['DailyReturn'] = fb['PriceDiff']/fb['Close']
fb.head()

#Creating a Direction column must have the following rules:
#PriceDiff > 0  -> Up 1
#PriceDiff <= 0 -> Down -1
fb['Direction'] = [1 if fb.loc[ei, 'PriceDiff'] > 0 else -1
                   for ei in fb.index]

#Calculating moving average over the 3 days
#Due to random fluctuations taking an average price in a period can smooth out noise
fb['MovingAverage'] = (fb['Close'] + fb['Close'].shift(1) + fb['Close'].shift(2))/3
fb.head()

#I want to get the MA for 10,50,and 200 days
fb['MA10'] = fb['Close'].rolling(10).mean()
fb['MA50'] = fb['Close'].rolling(50).mean()
fb['MA200'] = fb['Close'].rolling(200).mean()
fb = fb.dropna()
fb.head()

#with what I have calculated I want to plot the MA
fb['Close'].plot(label='Close')
fb['MA50'].plot(label='MA50') #fast signal
fb['MA200'].plot(label='MA200') #slow signal
plt.legend()

#the MA50 > MA20 stock can be speculated the stock would have gone up for a limited time after 2018-1

fb['Shares'] = [ 1 if fb.loc[ei,'MA50']>fb.loc[ei,'MA10'] else 0
                for ei in fb.index]

fb.head()
fb.tail()
fb.describe()

#Daily Profit for Facebook
fb['Close1'] = fb['Close'].shift(-1)
fb.iloc[500:505,:]
fb['Profit'] = [fb.loc[ei,'Close1']-fb.loc[ei,'Close']
                if fb.loc[ei,'Shares']==1
                else 0 for ei in fb.index]
#graphing the profit showing when we lose and earn
fb['Profit'].plot()
plt.axhline(y=0, color='red')

plt.show()

#I want to calculate if this strat is able to generate profit
fb['Cummulative'] = fb['Profit'].cumsum()
fb.tail()
fb['Cummulative'].plot()
plt.show()
#this strat is profitable but this 

#Now I will do this with MS

ms['Price1'] = ms['Close'].shift(-1)
ms['PriceDiff'] = ms['Price1'] - ms['Close']
ms['DailyReturn'] = ms['PriceDiff']/ms['Close']
ms.head()

ms['Direction'] = [1 if ms.loc[ei, 'PriceDiff'] > 0 else -1
                   for ei in ms.index]
ms['MovingAverage'] = (ms['Close'] + ms['Close'].shift(1) + ms['Close'].shift(2))/3
ms.head()

ms['MA10'] = ms['Close'].rolling(10).mean()
ms['MA50'] = ms['Close'].rolling(50).mean()
ms['MA200'] = ms['Close'].rolling(200).mean()
ms = ms.dropna()
ms.head()

ms['Close'].plot(label='Close')
ms['MA50'].plot(label='MA50') #fast signal
ms['MA200'].plot(label='MA200') #slow signal
plt.legend()

ms['Shares'] = [ 1 if ms.loc[ei,'MA50']>ms.loc[ei,'MA10'] else 0
                for ei in ms.index]
ms.tail()

ms['Close1'] = ms['Close'].shift(-1)
ms.iloc[500:505,:]
ms['Profit'] = [ms.loc[ei,'Close1']-ms.loc[ei,'Close']
                if ms.loc[ei,'Shares']==1
                else 0 for ei in ms.index]
#graphing the profit showing when we lose and earn
ms['Profit'].plot()
plt.axhline(y=0, color='red')

plt.show()

ms['Cummulative'] = ms['Profit'].cumsum()
ms.tail()
ms['Cummulative'].plot()
plt.show()

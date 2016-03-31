# -*- coding: utf-8 -*-
"""
[Python 2.7 (Mayavi is not yet compatible with Python 3+)]
Created on Mon Feb 09 18:11:08 2015
@author: Ryan Stauffer
https://github.com/ryanpstauffer/market-vis

Market-vis test code v.001
Market Visualization Prototype
This will eventually be divided into modules (with this main module being the glue)
"""

import numpy as np
from mayavi import mlab
from datetime import datetime
import pandas as pd

from quotes import buildDailyPriceData
#from optimization import *

#from viz import picker_callback

#Assemble Test Data for temp use
timer = datetime.now()
    
#Select Dates for backtesting period    
startDate = datetime.strptime('20120101', '%Y%m%d')
endDate = datetime.strptime('20130101', '%Y%m%d')

#Get data for S&P500 Constituents
print('Pulling Market Data for S&P 500 from {0} to {1}'.format(startDate.strftime('%Y%m%d'), endDate.strftime('%Y%m%d')))
SP500Constituents = pd.read_csv('SP500_constituents.csv')
print(SP500Constituents)

#df = buildDailyPriceData(SP500Constituents['Symbol'])


##Load dataset from .csv
print("Pulling Market Data from .csv")
df = pd.read_csv('SP500_daily_price_data.csv')

# Convert strings to Datetime format
df[df.columns[0]] = df[df.columns[0]].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
df.index = df[df.columns[0]]
df.drop(df.columns[0], axis=1, inplace=True)

#Build Price Table
stockPrices = df.loc[startDate:endDate]
#FIX THIS
#SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame
stockPrices.dropna(axis=1, how='any', inplace=True)
#print(stockPrices.head())

stockList = list(set(stockPrices.columns))
print('Pulled data for {0} stocks from {1} to {2}'.format(len(stockList), startDate.strftime('%Y%m%d'), endDate.strftime('%Y%m%d')))

#Build Returns Table
stockReturns = stockPrices.pct_change(1)
print(stockReturns.head())


#Build Indexed Price Table (indexed to 100)
indexedPrices = stockReturns + 1
indexedPrices.iloc[0] = 100
indexedPrices = indexedPrices.cumprod(axis=0)
print(indexedPrices.head())

dates = list(set(stockReturns.index))
dates.sort()

#ret_matrix = stockReturns
x_length, y_length = stockReturns.shape
xTime = np.array([list(xrange(x_length)),] * y_length).transpose()
yCompanies = np.array([list(xrange(y_length)),] * x_length)

#tot_ret_matrix = ret_matrix + 1
#tot_ret_matrix.iloc[0] = 100
#z = tot_ret_matrix.cumprod(axis=0)
#print(z.head())

#sort indexed prices by total return on last date
lastDatePrices = indexedPrices.iloc[-1]
lastDatePrices.sort_values(inplace=True)
sort_order = lastDatePrices.index
indexedPrices = indexedPrices[sort_order]

#print(indexedPrices.tail())

#Create mayavi2 object
dims = xTime.shape
fig = mlab.figure(bgcolor=(.4,.4,.4))
vis = mlab.surf(xTime, yCompanies, indexedPrices, warp_scale='auto')
mlab.outline(vis)
mlab.orientation_axes(vis)
#mlab.title('S&P 500 Market Data Visualization', size = .25)
mlab.axes(vis, nb_labels=0, xlabel = 'Time', ylabel = 'Company', zlabel = 'Price')
#    cursor3d = mlab.points3d(0., 0., 0., mode='axes',
#                                color=(0, 0, 0),
#                                scale_factor=20)
#picker = fig.on_mouse_pick(picker_callback)

print('Total time: ', (datetime.now() - timer))
mlab.show()

print('End')
    
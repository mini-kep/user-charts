import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# %matplotlib inline

import requests

def get_frame(freq: str):
    """Return pandas dataframe with annual, quarterly, monthly or daily data.       
       Arg:
           freq - 'a', 'q', 'm' or 'd' literal         
       Returns:
           pandas DataFrame
    """
    url = 'http://minikep-db.herokuapp.com/api/frame?freq={}'.format(freq)
    return pd.read_csv(url, converters={0: pd.to_datetime}, index_col=0)

dfq = get_frame('q')    
print(dfq.columns)


selected_cols = ['GDP_bln_rub', 
       'GOV_EXPENSE_CONSOLIDATED_bln_rub',
       'GOV_REVENUE_CONSOLIDATED_bln_rub',
       # TODO: need rub rate
       #'EXPORT_GOODS_bln_usd',
       #'IMPORT_GOODS_bln_usd',
       'INVESTMENT_bln_rub', 
       'RETAIL_SALES_bln_rub']

# ERROR:
# TODO: need last observation to be NaN, not 0.

dfq = dfq[selected_cols]

print(dfq.head())
print(dfq.tail())

## index not set?
#index = pd.DatetimeIndex(start='1999Q1', end='2017Q3', freq='Q')
#dfq.set_index(index, inplace = True)

#In [9]:
#
#dfq.head()
#
#Out[9]:
#	EXPORT_GOODS_bln_usd 	GDP_bln_rub 	GOV_EXPENSE_ACCUM_CONSOLIDATED_bln_rub 	GOV_REVENUE_ACCUM_CONSOLIDATED_bln_rub 	IMPORT_GOODS_bln_usd 	INVESTMENT_bln_rub 	RETAIL_SALES_bln_rub
#1999-03-31 	15.3 	901.0 	189.0 	171.9 	9.1 	96.8 	379.0
#1999-06-30 	17.1 	1102.0 	486.8 	448.6 	10.1 	131.1 	416.5
#1999-09-30 	18.9 	1373.0 	795.8 	759.3 	9.5 	185.6 	464.6
#1999-12-31 	24.3 	1447.0 	1258.0 	1213.6 	10.8 	256.9 	537.3
#2000-03-31 	23.9 	1527.0 	330.2 	366.5 	10.0 	165.8 	517.7
#In [43]:
#
#dfq.tail()
#
#Out[43]:
#	EXPORT_GOODS_bln_usd 	GDP_bln_rub 	GOV_EXPENSE_ACCUM_CONSOLIDATED_bln_rub 	GOV_REVENUE_ACCUM_CONSOLIDATED_bln_rub 	IMPORT_GOODS_bln_usd 	INVESTMENT_bln_rub 	RETAIL_SALES_bln_rub
#2016-06-30 	67.9 	20430.0 	13582.9 	12521.5 	45.6 	3153.3 	6764.0
#2016-09-30 	70.9 	22721.0 	20493.6 	19374.5 	52.6 	3666.5 	7258.1
#2016-12-31 	82.6 	24077.0 	31323.7 	28181.5 	55.3 	5726.5 	7798.9
#2017-03-31 	82.4 	20091.0 	6892.4 	7036.6 	48.0 	2202.2 	6746.9
#2017-06-30 	83.8 	NaN 	14443.0 	14507.5 	58.6 	3521.5 	7129.1
#
#drop last observation (nan value)
#In [10]:
#
gdp = dfq.GDP_bln_rub[:-1]
#
#In [11]:
#
import statsmodels.api as sm
#
#C:\Users\User3\Anaconda3\lib\site-packages\statsmodels\compat\pandas.py:56: FutureWarning: The pandas.core.datetools module is deprecated and will be removed in a future version. Please use the pandas.tseries module instead.
#  from pandas.core import datetools
#
#decomposing series using HP filter
#In [12]:
#
#cycle, trend = sm.tsa.filters.hpfilter(gdp, 1600)
#
#calculating average deviation from trend
#In [13]:
#
#import numpy as np
#std_ = np.mean(abs(100 - trend/gdp * 100))
#
#plotting std_ and real valu
#In [14]:
#
#%matplotlib inline
#fig, ax = plt.subplots()
#
#gdp.plot(ax=ax, fontsize=16)
#trend.plot(ax=ax, fontsize=16)
#
#Out[14]:
#
#<matplotlib.axes._subplots.AxesSubplot at 0x1bfb59b0>
#
#function for crosscorrelation with lags
#In [41]:
#
#def crosscorr(datax, datay):
#    
#    return "{0:.2f}".format(datax.corr(datay.shift(-1))), "{0:.2f}".format(datax.corr(datay)), "{0:.2f}".format(datax.corr(datay.shift(1)))
#
#In [42]:
#
#crosscorr(gdp, gdp)
#
#Out[42]:
#
#('0.98', '1.00', '0.98')
#
#function to calculate deviation from trend
#In [44]:
#
#def deviation(var):
#    cycle, trend = sm.tsa.filters.hpfilter(var, 1600)
#    std_ = np.mean(abs(100 - trend/var * 100))
#    return "{0:.1f}".format(std_)
#
#In [45]:
#
#deviation(gdp)
#
#Out[45]:
#
#'7.4'
#

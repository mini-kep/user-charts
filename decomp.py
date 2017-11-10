
# coding: utf-8

# In[2]:

import datetime
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
import datetime
warnings.filterwarnings('ignore')


def read_from_url(source_url):
	"""Read pandas time series from *source_url*."""
	return pd.read_csv(source_url, 
                       converters={0: pd.to_datetime}, 
                       index_col=0,
                       squeeze=True)

def decompose(url):
    decomposition = seasonal_decompose(read_from_url(url))
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    
    return trend, seasonal, residual



if __name__ == '__main__':
    url = 'http://minikep-db.herokuapp.com/all/series/INVESTMENT_bln_rub/m'
    series_trend, series_seasonal, series_residual = decompose(url)


# In[ ]:




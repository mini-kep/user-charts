# -*- coding: utf-8 -*-

import datetime
import matplotlib.pyplot as plt
import pandas as pd


def make_url(freq, name):    
    return ('https://minikep-db.herokuapp.com/api/'
           f'datapoints?name={name}&freq={freq}')


def read_from_url(source_url):
	"""Read pandas time series from *source_url*."""
	return pd.read_csv(source_url, 
                       converters={0: pd.to_datetime}, 
                       index_col=0,
                       squeeze=True)

def get_ts(freq, name):
    url = make_url(freq, name)
    return read_from_url(url)

def get_df(freq, *names):
    df_list = [get_ts(freq, name).to_frame() for name in names]
    df = df_list[0]
    for right_df in df_list[1:]:
       df = df.merge(right_df, right_index=True, left_index=True)
    return df  

df = get_df('a', 'GDP_yoy', 'CPI_rog')  
assert isinstance(df, pd.DataFrame

"""Access code for Russian macroeconomic time series dataset."""

import os
import requests
import pandas as pd
from time import time


def get_frame(freq: str):
    """Return pandas dataframe with annual, quarterly, monthly or daily data.       
       Arg:
           freq - 'a', 'q', 'm' or 'd' literal         
       Returns:
           pandas DataFrame
    """
    url = 'http://minikep-db.herokuapp.com/api/frame?freq={}'.format(freq)
    return pd.read_csv(url, converters={0: pd.to_datetime}, index_col=0)

    
def make_url(backend, freq, name=None):    
    url = f'http://minikep-db.herokuapp.com/api/{backend}?freq={freq}'
    if name:
        url += f'&name={name}'    
    return url

# TODO: сonvert to tests
assert make_url('series', 'a', 'GDP_yoy')
assert make_url('frame', 'a')

def fetch_json(url):
    return requests.get(url).json()    

def read_ts(url):
    """Read pandas time series from *url*."""
    return read_df(url, squeeze=True)

def read_df(url, squeeze=False):
    """Read pandas dataframe from *file_or_url*."""
    formatter = dict(converters={0: pd.to_datetime}, index_col=0)  
    return pd.read_csv(url, **formatter, squeeze=squeeze)

def get_freq():
    # FIXME: this is redundant, must use make_url()
    url = 'http://minikep-db.herokuapp.com/api/freq'
    return fetch_json(url)

def get_names(freq):
    # TODO: change API to parameterЖ
    #       'http://minikep-db.herokuapp.com/api/names?freq={}' 
    # FIXME: this is redundant, must use make_url()
    url = 'http://minikep-db.herokuapp.com/api/names/{}'.format(freq)
    return fetch_json(url)

def get_datapoints(freq, name):
    url = make_url('datapoints', freq, name) 
    return fetch_json(url)

assert get_datapoints('a', 'GDP_yoy')

def get_ts(freq, name):  
    url = make_url('series', freq, name)
    return read_ts(url)

assert not get_ts('a', 'GDP_yoy').empty
    
def get_df(freq, names=[]):    
    url = make_url(backend='frame', freq=freq, name=','.join(names))
    return read_df(url)

dfa = get_df('a')
assert isinstance(dfa, pd.DataFrame)
assert not get_df('a', ['GDP_yoy', 'CPI_rog']).empty

def make_filename(freq):
    return os.path.join('data', f'df{freq}.csv')

def save_local(freq):
    df = get_df(freq) 
    df.to_csv(make_filename(freq)) 

def read_local(freq):  
    path = make_filename(freq)
    try:
       return read_df(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"No data file: {path}")        

if __name__ == '__main__':
    # get variable list for frequency 'q' (quarterly)
    variable_names_quarterly = get_names('q')
    assert 'GDP_yoy' in variable_names_quarterly 
    
    # read one variable as pd.Series
    ts = get_ts('q', 'GDP_yoy')

    # read all variables for frequency 'q' as pd.DataFrame 
    dfq = get_df('q')    
    # check dataframe columns are exactly the ones we retrieved earlier
    assert variable_names_quarterly == dfq.columns.tolist()    

    # update local files (about one minute on my machine) 
    start = time()
    for freq in 'aqmd':
        save_local(freq) 
    print("Read full dataset:", round(time() - start, 1), "sec")
    
    # reading a local version  
    dfa = read_local('a')
    
    # TODO: compare time for series / frame query
    
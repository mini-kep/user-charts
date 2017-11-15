import os
import requests
import pandas as pd
from time import time
    

def fetch_json(url):
    return requests.get(url).json()    

def get_freq():
    url = 'http://minikep-db.herokuapp.com/api/freq'
    return fetch_json(url)

def get_names(freq):
    url = 'http://minikep-db.herokuapp.com/api/names/{}'.format(freq)
    return fetch_json(url)

def make_url(freq, name, format):    
    return ('https://minikep-db.herokuapp.com/api/datapoints'
            '?name={}&freq={}&format={}'.format(name, freq, format))

def get_datapoints(freq, name):
    url = make_url(freq, name, 'json') 
    return fetch_json(url)

set_index = dict(converters={0: pd.to_datetime}, index_col=0)  

def read_ts(file_or_url):
    """Read pandas time series from *file_or_url*."""
    return pd.read_csv(file_or_url, **set_index, squeeze=True)

def read_df(file_or_url):
    """Read pandas dataframe from *file_or_url*."""
    return pd.read_csv(file_or_url, **set_index)
 
def get_ts(freq, name):  
    url = make_url(freq, name, 'csv')
    return read_ts(url)
    
def get_df_by_names(freq, names):
    df_list = [get_ts(freq, name).to_frame() for name in names]
    df = df_list[0]
    for right_df in df_list[1:]:
       df = df.join(right_df, how='outer')
    return df  

def get_df(freq):
    names = get_names(freq)
    return get_df_by_names(freq, names)

def make_filename(freq):
    return os.path.join('data', f'df{freq}.csv')

def save_local(freq):
    df = get_df(freq) 
    fn = make_filename(freq)
    df.to_csv(fn) 

def get_df_local(freq):  
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
    # runs about 20-40 sec
    dfq = get_df('q')    
    # check dataframe columns are exactly the ones we retrieved earlier
    assert variable_names_quarterly == dfq.columns.tolist()    

    # update local files (about one minute on my machine) 
    start = time()
    for freq in 'aqmd':
        save_local(freq) 
    print("Read full dataset:", round(time() - start, 1), "sec")
    
    # reading a local version  
    dfa = get_df_local('a')
    
    # TODO: compare time for series / frame query
    
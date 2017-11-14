import requests
import pandas as pd

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
    
def read_from_url(url):
    """Read pandas time series from *source_url*."""
    return pd.read_csv(url, converters={0: pd.to_datetime}, index_col=0, squeeze=True)
 
def get_ts(freq, name):  
    url = make_url(freq, name, 'csv')
    return read_from_url(url)
    
def get_df_by_names(freq, names):
    df_list = [get_ts(freq, name).to_frame() for name in names]
    df = df_list[0]
    for right_df in df_list[1:]:
       df = df.join(right_df, how='outer')
    return df  

def get_df(freq):
    names = get_names(freq)
    return get_df_by_names(freq, names)

# TODO: save data in csv file as backups, similar as kep parser does it. 

if __name__ == '__main__':
    # get variable list for frequency 'q' (quarterly)
    variable_names_quarterly = get_names('q')
    # read one variable as pd.Series
    ts = get_ts('q', 'GDP_yoy')
    # read all variables for frequency 'q' as pd.DataFrame 
    # runs about 20-40 sec
    dfq = get_df('q')    
    # check dataframe columns are exaactly the ones we retrieved earlier
    assert variable_names_quarterly == dfq.columns.tolist()    
    
    # can also get monthly data
    # commented because it slows down code, uncomment if you need monthly data
    # dfm = get_df('m')    

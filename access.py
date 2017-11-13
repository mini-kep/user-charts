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

if __name__ == '__main__':
    variable_names_quarterly = get_names('q')
    ts = get_ts('q', 'GDP_yoy')
    dfq = get_df('q')    
    print(dfq.columns)
    
#        Index(['CPI_ALCOHOL_rog', 'CPI_FOOD_rog', 'CPI_NONFOOD_rog', 'CPI_rog',
#               'CPI_SERVICES_rog', 'EXPORT_GOODS_bln_usd', 'GDP_bln_rub', 'GDP_yoy',
#               'GOV_EXPENSE_ACCUM_CONSOLIDATED_bln_rub',
#               'GOV_EXPENSE_ACCUM_FEDERAL_bln_rub',
#               'GOV_EXPENSE_ACCUM_SUBFEDERAL_bln_rub',
#               'GOV_REVENUE_ACCUM_CONSOLIDATED_bln_rub',
#               'GOV_REVENUE_ACCUM_FEDERAL_bln_rub',
#               'GOV_REVENUE_ACCUM_SUBFEDERAL_bln_rub',
#               'GOV_SURPLUS_ACCUM_FEDERAL_bln_rub',
#               'GOV_SURPLUS_ACCUM_SUBFEDERAL_bln_rub', 'IMPORT_GOODS_bln_usd',
#               'INDPRO_rog', 'INDPRO_yoy', 'INVESTMENT_bln_rub', 'INVESTMENT_rog',
#               'INVESTMENT_yoy', 'RETAIL_SALES_bln_rub', 'RETAIL_SALES_FOOD_bln_rub',
#               'RETAIL_SALES_FOOD_rog', 'RETAIL_SALES_FOOD_yoy',
#               'RETAIL_SALES_NONFOOD_bln_rub', 'RETAIL_SALES_NONFOOD_rog',
#               'RETAIL_SALES_NONFOOD_yoy', 'RETAIL_SALES_rog', 'RETAIL_SALES_yoy',
#               'TRANSPORT_FREIGHT_bln_tkm', 'UNEMPL_pct', 'WAGE_NOMINAL_rub',
#               'WAGE_REAL_rog', 'WAGE_REAL_yoy'],
#              dtype='object')

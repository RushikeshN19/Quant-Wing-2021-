import pandas as pd
import pandas_datareader as web
import statsmodels.api as smf
import urllib.request
import zipfile

def get_fama_french():
    ff_url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip"

    
    urllib.request.urlretrieve(ff_url,'fama_french.zip')
    zip_file = zipfile.ZipFile('fama_french.zip', 'r')
    
    zip_file.extractall()
        
    zip_file.close()
    
    ff_factors = pd.read_csv('F-F_Research_Data_Factors.csv', skiprows = 3, index_col = 0)
    
    ff_row = ff_factors.isnull().any(1).nonzero()[0][0]
    
    ff_factors = pd.read_csv('F-F_Research_Data_Factors.csv', skiprows = 3, nrows = ff_row, index_col = 0)
    
    ff_factors.index = pd.to_datetime(ff_factors.index, format= '%Y%m')
    
    ff_factors.index = ff_factors.index + pd.offsets.MonthEnd()
    
    ff_factors = ff_factors.apply(lambda x: x/ 100)
    return ff_factors

ff_data = get_fama_french()
print(ff_data.tail())

ff_last = ff_data.index[ff_data.shape[0] - 1].date()

def get_price_data(ticker, start, end):
    price = web.get_data_yahoo(ticker, start, end)
    price = price['Adj Close'] 
    return price

price_data = get_price_data("FCNTX", "1980-01-01", "2019-06-30")
price_data = price_data.loc[:ff_last]
print(price_data.tail())

def get_return_data(price_data, period = "M"):
    
    price = price_data.resample(period).last()
    ret_data = price.pct_change()[1:]
    ret_data = pd.DataFrame(ret_data)
    ret_data.columns = ['portfolio']
    return ret_data
    
ret_data = get_return_data(price_data, "M")
print(ret_data.tail())

all_data = pd.merge(pd.DataFrame(ret_data),ff_data, how = 'inner', left_index= True, right_index= True)
all_data.rename(columns={"Mkt-RF":"mkt_excess"}, inplace=True)
all_data['port_excess'] = all_data['portfolio'] - all_data['RF']
print(all_data.tail())

model = smf.formula.ols(formula = "port_excess ~ mkt_excess + SMB + HML", data = all_data).fit()
print(model.params)

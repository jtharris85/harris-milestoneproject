import simplejson as json
import requests
import pandas as pd

#Quandl stocks api
url='https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=y_KmmxPPeu75fEHcbEg2'

#Print check to determine if it works
def jprint(obj):
    text=json.dumps(obj,sort_keys=True,indent=4)
    print(text)

#Define parameters for filtering. Need to make them selectable!
parameter={'qopts.columns':"ticker,date,open,adj_open,close,adj_close","ticker":"F"}
r=requests.get(url,params=parameter)

#Drop the excess framework
data=json.dumps(r.json()['datatable'])
#Convert back to dictionary and edit columns
data2=json.loads(data)
data2['columns']=['Ticker','Date','Open','Adj Open','Close','Adj Close']
#Convert to string
prep=json.dumps(data2)
#Create dataframe
df=pd.read_json(prep,orient='split')

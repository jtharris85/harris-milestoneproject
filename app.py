from flask import Flask, render_template, request, redirect

#Modified for Day4 jtharris85 ownership

app = Flask(__name__)

import simplejson as json
import requests
import pandas as pd

app.vars={}
#Quandl stocks api
def stockrequest():
    import simplejson as json
    import requests
    import pandas as pd
    url='https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=y_KmmxPPeu75fEHcbEg2'

#Print check to determine if it works
    def jprint(obj):
        text=json.dumps(obj,sort_keys=True,indent=4)
        print(text)

#Define parameters for filtering. Need to make them selectable!
    parameter={'qopts.columns':"ticker,date,open,adj_open,close,adj_close","ticker":app.vars['ticker'],"date.gte":app.vars['startdate'],"date.lte":app.vars['enddate']}
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

    def stockplot():

        import numpy as np

        from bokeh.plotting import figure, output_file, show

# prepare some data
        if app.vars['close']==0:
            close=0
        else:
            close=df[app.vars['close']]
        if app.vars['open']==0:
            open=0
        else:
            open=df[app.vars['open']]
        if app.vars['adjclose']==0:
            adjclose=0
        else:
            adjclose=df[app.vars['adjclose']]
        if app.vars['adjopen']==0:
            adjopen=0
        else:
            adjopen=df[app.vars['adjopen']]
        dates = df['Date']


# output to static HTML file
        output_file("templates/stocktest.html", title="stock test example")

# create a new plot with a datetime axis type
        p = figure(plot_width=800, plot_height=350, x_axis_type="datetime")

# add renderers
        p.line(dates, close, color='blue', legend='Close')
        p.line(dates, open, color='red', legend='Open')
        p.line(dates, adjclose, color='black', legend='Adj Close')
        p.line(dates, adjopen, color='green', legend='Adj Open')

# NEW: customize by setting attributes
        p.title.text = "Stock Prices"
        p.legend.location = "top_left"
        p.grid.grid_line_alpha = 0
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Price'
        p.ygrid.band_fill_color = "olive"
        p.ygrid.band_fill_alpha = 0.1
        show(p)
    stockplot()

@app.route('/',methods=['GET','POST'])
def stockeselector():
    if request.method=='GET':
        return render_template('stockselector.html')
    else:
        return redirect('/stocks')

@app.route('/stocks',methods=['POST'])
def stocks():
    import datetime
    app.vars['ticker']=request.form['ticker']
    app.vars['open']=request.form.get('Open',0)
    app.vars['close']=request.form.get('Close',0)
    app.vars['adjclose']=request.form.get('Adj Close',0)
    app.vars['adjopen']=request.form.get('Adj Open',0)
    startdate=request.form['daterange'][:10]
    app.vars['startdate']=datetime.datetime.strptime(startdate,"%m/%d/%Y").strftime("%Y-%m-%d")
    enddate=request.form['daterange'][-10:]
    app.vars['enddate']=datetime.datetime.strptime(enddate,"%m/%d/%Y").strftime("%Y-%m-%d")
    stockrequest()
    return render_template('stocktest.html')

if __name__ == '__main__':
  app.run(port=33507,debug=True)

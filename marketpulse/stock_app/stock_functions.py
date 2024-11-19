import requests
from datetime import datetime, timedelta
import pandas as pd
from bokeh.plotting import figure,show,output_notebook
from bokeh.embed import components
API_URL="https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?apikey=1anPitqreO42ExDOKVBcKpzy6h7ZRtc9"

def fetch_stock_data(company,years):
    start_date=(datetime.now()-timedelta(days=years*365)).strftime('%Y-%m-%d')
    print(start_date)
    response=requests.get(API_URL,params={"from":start_date})
    return response.json()

def stock_data_computation(data):
    df=pd.DataFrame(data['historical'])
    print(df)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    monthly = df.resample('ME').agg({'open': 'first', 'close': 'last'})
    monthly['change_percent'] = ((monthly['close'] - monthly['open']) / monthly['open']) * 100
    monthly['month'] = monthly.index.month
    monthly['year'] = monthly.index.year
    print("resampled data")
    print(monthly)
    top_months = monthly.groupby('year').apply(lambda x: x.loc[x['change_percent'].idxmax()]['month'])
    print("top performing month of each year")
    print(top_months)
    top_months = top_months.value_counts().sort_index()
    print("top performing month and its frequency in the given number of years")
    print(top_months)
    return top_months.to_dict()


def create_bokeh_plot(data):
    p = figure(x_range=[str(i) for i in range(1, 13)], title="Frequency of Highest Growth Months",
               x_axis_label="Month", y_axis_label="Frequency")
    p.vbar(x=[str(k) for k in data.index], top=data.values, width=0.8)
    return components(p)

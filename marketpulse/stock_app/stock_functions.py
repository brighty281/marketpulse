import requests
from datetime import datetime, timedelta
import pandas as pd
from bokeh.plotting import figure,show,output_notebook
from bokeh.embed import components
from django.conf import settings
API_URL=settings.API_URL

def fetch_stock_data(company,years):
    start_date=(datetime.now()-timedelta(days=years*365)).strftime('%Y-%m-%d')
    print(start_date)
    response=requests.get(API_URL,params={"from":start_date})
    return response.json()

def stock_data_computation(data):
    df=pd.DataFrame(data['historical'])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    monthly = df.resample('ME').agg({'open': 'first', 'close': 'last'})
    monthly['change_percent'] = ((monthly['close'] - monthly['open']) / monthly['open']) * 100
    monthly['month'] = monthly.index.month
    monthly['year'] = monthly.index.year
    top_months = monthly.groupby('year').apply(lambda x: x.loc[x['change_percent'].idxmax()]['month'])
    top_months = top_months.value_counts().sort_index()
    return top_months.to_dict()


def create_bokeh_plot(data):
    p = figure(x_range=[str(i) for i in range(1, 13)], title="Frequency of Highest Growth Months",
               x_axis_label="Month", y_axis_label="Frequency")
    p.vbar(x=[str(k) for k in data.index], top=data.values, width=0.8)
    return components(p)

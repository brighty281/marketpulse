from django.shortcuts import render
from .stock_functions import fetch_stock_data, stock_data_computation, create_bokeh_plot
import json
from .models import StockCache
from django.conf import settings



# Create your views here.
def sample_view(request):
    return render(request,'home.html')

def stock_details(request):
    company=request.GET.get('company')
    years=int(request.GET.get('years'))
    cached_stock = StockCache.objects.filter(company=company, duration=years).first()
    if cached_stock:
        data = cached_stock.result
    else:
        json_data=fetch_stock_data(company,years)
        data=stock_data_computation(json_data)
        StockCache.objects.create(company=company,duration=years,result=data)
        
    months = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    table_data = [
        {'month': months[i], 'count': data.get(f'{i}.0', 0)}
        for i in range(1, 13)
    ]
    return render(request,'stock_plot.html',{'table_data': table_data},{'base_url':settings.BASE_URL})


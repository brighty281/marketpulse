from .views import *
from django.urls import path
urlpatterns=[
    path('',sample_view,name='home-page'),
    path('stock_plot',stock_details,name='stock-plot')
]